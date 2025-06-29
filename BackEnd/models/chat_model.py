from typing import Optional, Dict, Any
from config.database import get_database

class ChatModel:
    def __init__(self):
        self.db = get_database()
    
    def create(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar novo chat"""
        try:
            result = self.db.table("chat").insert(chat_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar chat: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_usuarios(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Buscar chat entre dois usuários"""
        try:
            result = (self.db.table("chat")
                     .select("*")
                     .or_(f"and(usuario1.eq.{usuario1},usuario2.eq.{usuario2}),and(usuario1.eq.{usuario2},usuario2.eq.{usuario1})")
                     .single()
                     .execute())
            
            if not result.data:
                return {"success": False, "error": "Chat não encontrado"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_usuario(self, usuario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todos os chats de um usuário"""
        try:
            query = (self.db.table("chat")
                    .select("*")
                    .or_(f"usuario1.eq.{usuario},usuario2.eq.{usuario}"))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todos os chats"""
        try:
            query = self.db.table("chat").select("*")
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Deletar chat"""
        try:
            result = (self.db.table("chat")
                     .delete()
                     .or_(f"and(usuario1.eq.{usuario1},usuario2.eq.{usuario2}),and(usuario1.eq.{usuario2},usuario2.eq.{usuario1})")
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar chat: {result.error}")
            
            return {"success": True, "message": "Chat deletado com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
