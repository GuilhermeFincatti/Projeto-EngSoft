from typing import Dict, Any, List
from config.database import get_database

class TrocaModel:
    def __init__(self):
        self.db = get_database()
    
    def criar_proposta_troca(self, solicitante: str, destinatario: str, 
                            carta_oferecida: str, carta_solicitada: str) -> Dict[str, Any]:
        """Criar uma nova proposta de troca"""
        try:
            # Verificar se o solicitante possui a carta oferecida
            coleta_result = self.db.table("coleta").select("quantidade").eq("usuario", solicitante).eq("qrcode", carta_oferecida).execute()
            
            if not coleta_result.data or coleta_result.data[0]["quantidade"] < 1:
                return {"success": False, "error": "Você não possui esta carta para trocar"}
            
            # Verificar se o destinatário possui a carta solicitada
            coleta_destinatario = self.db.table("coleta").select("quantidade").eq("usuario", destinatario).eq("qrcode", carta_solicitada).execute()
            
            if not coleta_destinatario.data or coleta_destinatario.data[0]["quantidade"] < 1:
                return {"success": False, "error": "O destinatário não possui a carta solicitada"}
            
            # Criar proposta de troca
            troca_data = {
                "solicitante": solicitante,
                "destinatario": destinatario,
                "cartaoferecida": carta_oferecida,
                "cartasolicitada": carta_solicitada,
                "status": "pendente",
                "datasolicitacao": "now()"
            }
            
            result = self.db.table("trocacarta").insert(troca_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar proposta de troca: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def responder_troca(self, troca_id: int, resposta: str, usuario: str) -> Dict[str, Any]:
        """Aceitar ou rejeitar uma proposta de troca"""
        try:
            if resposta not in ["aceita", "rejeitada"]:
                return {"success": False, "error": "Resposta deve ser 'aceita' ou 'rejeitada'"}
            
            # Buscar detalhes da troca
            troca_result = self.db.table("trocacarta").select("*").eq("id", troca_id).single().execute()
            
            if not troca_result.data:
                return {"success": False, "error": "Proposta de troca não encontrada"}
            
            troca = troca_result.data
            
            # Verificar se o usuário é o destinatário
            if troca["destinatario"] != usuario:
                return {"success": False, "error": "Apenas o destinatário pode responder à troca"}
            
            # Verificar se a troca ainda está pendente
            if troca["status"] != "pendente":
                return {"success": False, "error": "Esta troca já foi respondida"}
            
            # Atualizar status da troca
            update_result = self.db.table("trocacarta").update({
                "status": resposta,
                "dataresposta": "now()"
            }).eq("id", troca_id).execute()
            
            if hasattr(update_result, 'error') and update_result.error:
                raise Exception(f"Erro ao atualizar troca: {update_result.error}")
            
            # Se aceita, executar a troca
            if resposta == "aceita":
                return self._executar_troca(troca)
            
            return {"success": True, "data": update_result.data[0] if update_result.data else None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _executar_troca(self, troca: Dict[str, Any]) -> Dict[str, Any]:
        """Executar a troca das cartas entre os usuários"""
        try:
            solicitante = troca["solicitante"]
            destinatario = troca["destinatario"]
            carta_oferecida = troca["cartaoferecida"]
            carta_solicitada = troca["cartasolicitada"]
            
            # Remover carta oferecida do solicitante
            self.db.table("coleta").update({
                "quantidade": "quantidade - 1"
            }).eq("usuario", solicitante).eq("qrcode", carta_oferecida).execute()
            
            # Remover carta solicitada do destinatário
            self.db.table("coleta").update({
                "quantidade": "quantidade - 1"
            }).eq("usuario", destinatario).eq("qrcode", carta_solicitada).execute()
            
            # Adicionar carta solicitada ao solicitante
            coleta_solicitante = self.db.table("coleta").select("quantidade").eq("usuario", solicitante).eq("qrcode", carta_solicitada).execute()
            
            if coleta_solicitante.data:
                # Já possui, incrementar quantidade
                self.db.table("coleta").update({
                    "quantidade": "quantidade + 1"
                }).eq("usuario", solicitante).eq("qrcode", carta_solicitada).execute()
            else:
                # Não possui, criar nova entrada
                self.db.table("coleta").insert({
                    "usuario": solicitante,
                    "qrcode": carta_solicitada,
                    "quantidade": 1
                }).execute()
            
            # Adicionar carta oferecida ao destinatário
            coleta_destinatario = self.db.table("coleta").select("quantidade").eq("usuario", destinatario).eq("qrcode", carta_oferecida).execute()
            
            if coleta_destinatario.data:
                # Já possui, incrementar quantidade
                self.db.table("coleta").update({
                    "quantidade": "quantidade + 1"
                }).eq("usuario", destinatario).eq("qrcode", carta_oferecida).execute()
            else:
                # Não possui, criar nova entrada
                self.db.table("coleta").insert({
                    "usuario": destinatario,
                    "qrcode": carta_oferecida,
                    "quantidade": 1
                }).execute()
            
            return {"success": True, "message": "Troca executada com sucesso"}
            
        except Exception as e:
            return {"success": False, "error": f"Erro ao executar troca: {str(e)}"}
    
    def listar_trocas_pendentes(self, usuario: str) -> Dict[str, Any]:
        """Listar trocas pendentes para um usuário"""
        try:
            result = self.db.table("trocacarta").select("""
                *,
                carta_oferecida:cartaoferecida(qrcode, raridade, imagem, localizacao),
                carta_solicitada:cartasolicitada(qrcode, raridade, imagem, localizacao),
                solicitante_info:solicitante(nickname, ranking, xp, nivel, fotoperfil),
                destinatario_info:destinatario(nickname, ranking, xp, nivel, fotoperfil)
            """).or_(
                f"solicitante.eq.{usuario},destinatario.eq.{usuario}"
            ).eq("status", "pendente").execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar trocas: {result.error}")
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def cancelar_troca(self, troca_id: int, usuario: str) -> Dict[str, Any]:
        """Cancelar uma proposta de troca"""
        try:
            # Buscar detalhes da troca
            troca_result = self.db.table("trocacarta").select("*").eq("id", troca_id).single().execute()
            
            if not troca_result.data:
                return {"success": False, "error": "Proposta de troca não encontrada"}
            
            troca = troca_result.data
            
            # Verificar se o usuário é o solicitante
            if troca["solicitante"] != usuario:
                return {"success": False, "error": "Apenas o solicitante pode cancelar a troca"}
            
            # Verificar se a troca ainda está pendente
            if troca["status"] != "pendente":
                return {"success": False, "error": "Esta troca não pode ser cancelada"}
            
            # Atualizar status para cancelada
            result = self.db.table("trocacarta").update({
                "status": "cancelada",
                "dataresposta": "now()"
            }).eq("id", troca_id).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao cancelar troca: {result.error}")
            
            return {"success": True, "message": "Troca cancelada com sucesso"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def historico_trocas(self, usuario: str, limite: int = 20) -> Dict[str, Any]:
        """Buscar histórico de trocas de um usuário"""
        try:
            result = self.db.table("trocacarta").select("""
                *,
                carta_oferecida:cartaoferecida(qrcode, raridade, imagem, localizacao),
                carta_solicitada:cartasolicitada(qrcode, raridade, imagem, localizacao),
                solicitante_info:solicitante(nickname, ranking, xp, nivel, fotoperfil),
                destinatario_info:destinatario(nickname, ranking, xp, nivel, fotoperfil)
            """).or_(
                f"solicitante.eq.{usuario},destinatario.eq.{usuario}"
            ).order("datasolicitacao", desc=True).limit(limite).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar histórico: {result.error}")
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
