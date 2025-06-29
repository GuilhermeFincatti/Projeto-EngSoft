from typing import Dict, Any, Optional
from config.database import get_database

class MissaoQtdModel:
    def __init__(self):
        self.db = get_database()

    def create(self, missaoqtd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova entrada de MissaoQtd"""
        try:
            result = self.db.table("MissaoQtd").insert(missaoqtd_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar MissaoQtd: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_codigo(self, codigo: int) -> Dict[str, Any]:
        """Buscar MissaoQtd por Código"""
        try:
            result = self.db.table("MissaoQtd").select("*").eq("Codigo", codigo).single().execute()
            
            if not result.data:
                return {"success": False, "error": "MissaoQtd não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as entradas de MissaoQtd"""
        try:
            query = self.db.table("MissaoQtd").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, codigo: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar uma MissaoQtd"""
        try:
            result = self.db.table("MissaoQtd").update(update_data).eq("Codigo", codigo).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar MissaoQtd: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "MissaoQtd não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, codigo: int) -> Dict[str, Any]:
        """Deletar uma MissaoQtd"""
        try:
            result = self.db.table("MissaoQtd").delete().eq("Codigo", codigo).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar MissaoQtd: {result.error}")
            
            return {"success": True, "message": "MissaoQtd deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
