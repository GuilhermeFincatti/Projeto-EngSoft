from typing import Dict, Any, List
from config.database import get_database

class TrocaCartaModel:
    def __init__(self):
        self.db = get_database()
    
    def criar_solicitacao_troca(self, solicitante: str, destinatario: str, 
                               carta_oferecida: str, carta_solicitada: str) -> Dict[str, Any]:
        """Criar uma nova solicitação de troca de cartas"""
        try:
            # Verificar se o solicitante possui a carta oferecida
            coleta_check = (self.db.table("coleta")
                          .select("quantidade")
                          .eq("usuario", solicitante)
                          .eq("qrcode", carta_oferecida)
                          .execute())
            
            if not coleta_check.data or coleta_check.data[0]["quantidade"] < 1:
                return {"success": False, "error": "Você não possui esta carta para trocar"}
            
            # Verificar se o destinatário possui a carta solicitada
            destinatario_check = (self.db.table("coleta")
                                 .select("quantidade")
                                 .eq("usuario", destinatario)
                                 .eq("qrcode", carta_solicitada)
                                 .execute())
            
            if not destinatario_check.data or destinatario_check.data[0]["quantidade"] < 1:
                return {"success": False, "error": "O usuário não possui esta carta"}
            
            # Criar a solicitação de troca
            troca_data = {
                "solicitante": solicitante,
                "destinatario": destinatario,
                "cartaoferecida": carta_oferecida,
                "cartasolicitada": carta_solicitada,
                "status": "pendente"
            }
            
            result = self.db.table("trocacarta").insert(troca_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar solicitação: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def aceitar_troca(self, troca_id: int, usuario: str) -> Dict[str, Any]:
        """Aceitar uma solicitação de troca"""
        try:
            # Buscar detalhes da troca
            troca_result = (self.db.table("trocacarta")
                          .select("*")
                          .eq("id", troca_id)
                          .eq("destinatario", usuario)
                          .eq("status", "pendente")
                          .single()
                          .execute())
            
            if not troca_result.data:
                return {"success": False, "error": "Troca não encontrada ou não autorizada"}
            
            troca = troca_result.data
            solicitante = troca["solicitante"]
            destinatario = troca["destinatario"]
            carta_oferecida = troca["cartaoferecida"]
            carta_solicitada = troca["cartasolicitada"]
            
            # Verificar se ambos ainda possuem as cartas
            solicitante_check = (self.db.table("coleta")
                               .select("quantidade")
                               .eq("usuario", solicitante)
                               .eq("qrcode", carta_oferecida)
                               .execute())
            
            destinatario_check = (self.db.table("coleta")
                                .select("quantidade")
                                .eq("usuario", destinatario)
                                .eq("qrcode", carta_solicitada)
                                .execute())
            
            if (not solicitante_check.data or solicitante_check.data[0]["quantidade"] < 1 or
                not destinatario_check.data or destinatario_check.data[0]["quantidade"] < 1):
                # Cancelar troca se algum não tem mais a carta
                self.db.table("trocacarta").update({
                    "status": "cancelada",
                    "dataresposta": "now()"
                }).eq("id", troca_id).execute()
                return {"success": False, "error": "Uma das cartas não está mais disponível"}
            
            # Realizar a troca
            # Remover carta do solicitante
            nova_qtd_solicitante = solicitante_check.data[0]["quantidade"] - 1
            if nova_qtd_solicitante > 0:
                self.db.table("coleta").update({
                    "quantidade": nova_qtd_solicitante
                }).eq("usuario", solicitante).eq("qrcode", carta_oferecida).execute()
            else:
                self.db.table("coleta").delete().eq("usuario", solicitante).eq("qrcode", carta_oferecida).execute()
            
            # Remover carta do destinatário
            nova_qtd_destinatario = destinatario_check.data[0]["quantidade"] - 1
            if nova_qtd_destinatario > 0:
                self.db.table("coleta").update({
                    "quantidade": nova_qtd_destinatario
                }).eq("usuario", destinatario).eq("qrcode", carta_solicitada).execute()
            else:
                self.db.table("coleta").delete().eq("usuario", destinatario).eq("qrcode", carta_solicitada).execute()
            
            # Adicionar cartas aos novos donos
            # Carta oferecida vai para o destinatário
            destinatario_tem_oferecida = (self.db.table("coleta")
                                        .select("quantidade")
                                        .eq("usuario", destinatario)
                                        .eq("qrcode", carta_oferecida)
                                        .execute())
            
            if destinatario_tem_oferecida.data:
                nova_qtd = destinatario_tem_oferecida.data[0]["quantidade"] + 1
                self.db.table("coleta").update({
                    "quantidade": nova_qtd
                }).eq("usuario", destinatario).eq("qrcode", carta_oferecida).execute()
            else:
                self.db.table("coleta").insert({
                    "usuario": destinatario,
                    "qrcode": carta_oferecida,
                    "quantidade": 1
                }).execute()
            
            # Carta solicitada vai para o solicitante
            solicitante_tem_solicitada = (self.db.table("coleta")
                                        .select("quantidade")
                                        .eq("usuario", solicitante)
                                        .eq("qrcode", carta_solicitada)
                                        .execute())
            
            if solicitante_tem_solicitada.data:
                nova_qtd = solicitante_tem_solicitada.data[0]["quantidade"] + 1
                self.db.table("coleta").update({
                    "quantidade": nova_qtd
                }).eq("usuario", solicitante).eq("qrcode", carta_solicitada).execute()
            else:
                self.db.table("coleta").insert({
                    "usuario": solicitante,
                    "qrcode": carta_solicitada,
                    "quantidade": 1
                }).execute()
            
            # Atualizar status da troca
            self.db.table("trocacarta").update({
                "status": "aceita",
                "dataresposta": "now()"
            }).eq("id", troca_id).execute()
            
            return {"success": True, "message": "Troca realizada com sucesso!"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def rejeitar_troca(self, troca_id: int, usuario: str) -> Dict[str, Any]:
        """Rejeitar uma solicitação de troca"""
        try:
            result = (self.db.table("trocacarta")
                     .update({
                         "status": "rejeitada",
                         "dataresposta": "now()"
                     })
                     .eq("id", troca_id)
                     .eq("destinatario", usuario)
                     .eq("status", "pendente")
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao rejeitar troca: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "Troca não encontrada ou não autorizada"}
            
            return {"success": True, "message": "Troca rejeitada"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_trocas_usuario(self, usuario: str) -> Dict[str, Any]:
        """Listar todas as trocas relacionadas ao usuário"""
        try:
            result = (self.db.table("trocacarta")
                     .select("""
                         *,
                         carta_oferecida:cartaoferecida(qrcode, raridade, imagem, localizacao),
                         carta_solicitada:cartasolicitada(qrcode, raridade, imagem, localizacao),
                         usuario_solicitante:solicitante(nickname, fotoperfil),
                         usuario_destinatario:destinatario(nickname, fotoperfil)
                     """)
                     .or_(f"solicitante.eq.{usuario},destinatario.eq.{usuario}")
                     .order("datasolicitacao", desc=True)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar trocas: {result.error}")
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
