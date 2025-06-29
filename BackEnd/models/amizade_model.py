from typing import Dict, Any, List
from config.database import get_database

class AmizadeModel:
    def __init__(self):
        self.db = get_database()
    
    def enviar_solicitacao(self, solicitante: str, destinatario: str) -> Dict[str, Any]:
        """Enviar solicitação de amizade"""
        try:
            # Verificar se ambos os usuários existem
            solicitante_exists = self.db.table("usuario").select("nickname").eq("nickname", solicitante).execute()
            destinatario_exists = self.db.table("usuario").select("nickname").eq("nickname", destinatario).execute()
            
            if not solicitante_exists.data:
                return {"success": False, "error": f"Usuário solicitante '{solicitante}' não encontrado"}
            
            if not destinatario_exists.data:
                return {"success": False, "error": f"Usuário destinatário '{destinatario}' não encontrado"}
            
            # Verificar se já existe solicitação ou amizade (duas consultas separadas)
            existing1 = self.db.table("amizade").select("*").eq("solicitante", solicitante).eq("destinatario", destinatario).execute()
            existing2 = self.db.table("amizade").select("*").eq("solicitante", destinatario).eq("destinatario", solicitante).execute()
            
            if existing1.data or existing2.data:
                return {"success": False, "error": "Já existe uma solicitação ou amizade entre estes usuários"}
            
            # Criar nova solicitação
            result = self.db.table("amizade").insert({
                "solicitante": solicitante,
                "destinatario": destinatario,
                "status": "pendente",
                "data_solicitacao": "now()"
            }).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao enviar solicitação: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def aceitar_solicitacao(self, solicitacao_id: int) -> Dict[str, Any]:
        """Aceitar solicitação de amizade"""
        try:
            result = self.db.table("amizade").update({
                "status": "aceito",
                "data_aceite": "now()"
            }).eq("id", solicitacao_id).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao aceitar solicitação: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def recusar_solicitacao(self, solicitacao_id: int) -> Dict[str, Any]:
        """Recusar solicitação de amizade"""
        try:
            result = self.db.table("amizade").update({
                "status": "recusado"
            }).eq("id", solicitacao_id).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao recusar solicitação: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remover_amizade(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Remover amizade"""
        try:
            # Tentar remover em ambas as direções
            result1 = self.db.table("amizade").delete().eq("solicitante", usuario1).eq("destinatario", usuario2).execute()
            result2 = self.db.table("amizade").delete().eq("solicitante", usuario2).eq("destinatario", usuario1).execute()
            
            if (hasattr(result1, 'error') and result1.error) or (hasattr(result2, 'error') and result2.error):
                raise Exception(f"Erro ao remover amizade")
            
            return {"success": True, "message": "Amizade removida com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_amigos(self, nickname: str) -> Dict[str, Any]:
        """Listar amigos de um usuário"""
        try:
            result = self.db.table("amizade").select(
                "*, solicitante:usuario!solicitante(nickname,ranking,xp,nivel,fotoperfil), destinatario:usuario!destinatario(nickname,ranking,xp,nivel,fotoperfil)"
            ).or_(
                f"solicitante.eq.{nickname},destinatario.eq.{nickname}"
            ).eq("status", "aceito").execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar amigos: {result.error}")
            
            # Processar lista de amigos
            amigos = []
            for amizade in result.data:
                if amizade["solicitante"] == nickname:
                    amigo = amizade["destinatario"]
                else:
                    amigo = amizade["solicitante"]
                
                if amigo:
                    amigos.append({
                        "amizade_id": amizade["id"],
                        "nickname": amigo["nickname"],
                        "ranking": amigo["ranking"],
                        "xp": amigo["xp"],
                        "nivel": amigo["nivel"],
                        "fotoperfil": amigo.get("fotoperfil"),
                        "data_amizade": amizade.get("data_aceite")
                    })
            
            return {"success": True, "data": amigos}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_solicitacoes_pendentes(self, nickname: str) -> Dict[str, Any]:
        """Listar solicitações pendentes recebidas"""
        try:
            result = self.db.table("amizade").select(
                "*, solicitante:usuario!solicitante(nickname,ranking,xp,nivel,fotoperfil)"
            ).eq("destinatario", nickname).eq("status", "pendente").execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar solicitações: {result.error}")
            
            # Processar solicitações
            solicitacoes = []
            for solicitacao in result.data:
                solicitante = solicitacao["solicitante"]
                if solicitante:
                    solicitacoes.append({
                        "solicitacao_id": solicitacao["id"],
                        "nickname": solicitante["nickname"],
                        "ranking": solicitante["ranking"],
                        "xp": solicitante["xp"],
                        "nivel": solicitante["nivel"],
                        "fotoperfil": solicitante.get("fotoperfil"),
                        "data_solicitacao": solicitacao.get("data_solicitacao")
                    })
            
            return {"success": True, "data": solicitacoes}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def buscar_usuarios(self, termo_busca: str, usuario_atual: str, limit: int = 20) -> Dict[str, Any]:
        """Buscar usuários por nickname"""
        try:
            result = self.db.table("usuario").select(
                "nickname, ranking, xp, nivel, fotoperfil"
            ).ilike("nickname", f"%{termo_busca}%").neq("nickname", usuario_atual).limit(limit).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar usuários: {result.error}")
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verificar_status_amizade(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Verificar status de amizade entre dois usuários"""
        try:
            # Verificar em ambas as direções
            result1 = self.db.table("amizade").select("*").eq("solicitante", usuario1).eq("destinatario", usuario2).execute()
            result2 = self.db.table("amizade").select("*").eq("solicitante", usuario2).eq("destinatario", usuario1).execute()
            
            if hasattr(result1, 'error') and result1.error:
                raise Exception(f"Erro ao verificar amizade: {result1.error}")
            if hasattr(result2, 'error') and result2.error:
                raise Exception(f"Erro ao verificar amizade: {result2.error}")
            
            # Se não encontrou nada em nenhuma direção
            if not result1.data and not result2.data:
                return {"success": True, "data": {"status": "nenhum"}}
            
            # Retornar o primeiro resultado encontrado
            amizade = result1.data[0] if result1.data else result2.data[0]
            return {"success": True, "data": {
                "id": amizade["id"],
                "status": amizade["status"],
                "solicitante": amizade["solicitante"],
                "destinatario": amizade["destinatario"]
            }}
        except Exception as e:
            return {"success": False, "error": str(e)}
