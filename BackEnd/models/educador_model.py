from typing import Dict, Any, Optional
from config.database import get_database

class EducadorModel:
    def __init__(self):
        self.db = get_database()

    def create(self, educador_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar um novo educador"""
        try:
            result = self.db.table("educador").insert(educador_data).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar educador: {result.error}")
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_nickname(self, nickname: str) -> Dict[str, Any]:
        """Buscar educador por nickname"""
        try:
            result = self.db.table("educador").select("*").eq("nickname", nickname).single().execute()
            if not result.data:
                return {"success": False, "error": "Educador não encontrado"}
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def find_by_cargo(self, cargo: str) -> Dict[str, Any]:
        """Buscar educador por cargo"""
        try:
            result = self.db.table("educador").select("*").eq("cargo", cargo).single().execute()
            if not result.data:
                return {"success": False, "error": "Educador não encontrado"}
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todos os educadores"""
        try:
            query = self.db.table("educador").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, nickname: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar educador"""
        try:
            result = self.db.table("educador").update(update_data).eq("nickname", nickname).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar educador: {result.error}")
            if not result.data:
                return {"success": False, "error": "Educador não encontrado"}
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, nickname: str) -> Dict[str, Any]:
        """Deletar educador"""
        try:
            result = self.db.table("educador").delete().eq("nickname", nickname).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar educador: {result.error}")
            return {"success": True, "message": "Educador deletado com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
