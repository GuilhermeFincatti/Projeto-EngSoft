from typing import List, Optional, Dict, Any
from config.database import get_database

class UsuarioModel:
    def __init__(self):
        self.db = get_database()
    
    def create(self, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova pessoa"""
        try:
            result = self.db.table("usuario").insert(usuario_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar pessoa: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_nickname(self, nickname: str) -> Dict[str, Any]:
        """Buscar pessoa por nickname"""
        try:
            result = self.db.table("usuario").select("*").eq("nickname", nickname).single().execute()
            
            if not result.data:
                return {"success": False, "error": "Pessoa não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as pessoas"""
        try:
            query = self.db.table("usuario").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_email(self, email: str) -> Dict[str, Any]:
        """Buscar pessoa por email"""
        try:
            result = self.db.table("usuario").select("*").eq("email", email).single().execute()
            
            if not result.data:
                return {"success": False, "error": "Pessoa não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_tipo(self, tipo: str) -> Dict[str, Any]:
        """Buscar pessoas por tipo"""
        try:
            result = self.db.table("usuario").select("*").eq("tipo", tipo).execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update(self, nickname: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar pessoa"""
        try:
            result = self.db.table("usuario").update(update_data).eq("nickname", nickname).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar pessoa: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "Pessoa não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, nickname: str) -> Dict[str, Any]:
        """Deletar pessoa"""
        try:
            result = self.db.table("usuario").delete().eq("nickname", nickname).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar pessoa: {result.error}")
            
            return {"success": True, "message": "Pessoa deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
