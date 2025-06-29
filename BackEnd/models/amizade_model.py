from typing import Dict, Any, List
from config.database import get_database

class AmizadeModel:
    def __init__(self):
        self.db = get_database()
    
    def enviar_solicitacao(self, solicitante: str, destinatario: str) -> Dict[str, Any]:
        """Enviar solicitação de amizade"""
        try:
            # Verificar se já existe solicitação ou amizade
            existing = self.db.table("amizade").select("*").or_(
                f"and(solicitante.eq.{solicitante},destinatario.eq.{destinatario})",
                f"and(solicitante.eq.{destinatario},destinatario.eq.{solicitante})"
            ).execute()
            
            if existing.data:
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
            result = self.db.table("amizade").delete().or_(
                f"and(solicitante.eq.{usuario1},destinatario.eq.{usuario2})",
                f"and(solicitante.eq.{usuario2},destinatario.eq.{usuario1})"
            ).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao remover amizade: {result.error}")
            
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
            result = self.db.table("amizade").select("*").or_(
                f"and(solicitante.eq.{usuario1},destinatario.eq.{usuario2})",
                f"and(solicitante.eq.{usuario2},destinatario.eq.{usuario1})"
            ).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao verificar amizade: {result.error}")
            
            if not result.data:
                return {"success": True, "data": {"status": "nenhum"}}
            
            amizade = result.data[0]
            return {"success": True, "data": {
                "id": amizade["id"],
                "status": amizade["status"],
                "solicitante": amizade["solicitante"],
                "destinatario": amizade["destinatario"]
            }}
        except Exception as e:
            return {"success": False, "error": str(e)}
