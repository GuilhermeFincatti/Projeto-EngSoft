from typing import Dict, Any, Optional
from config.database import get_database

class MissaoQtdModel:
    def __init__(self):
        self.db = get_database()

    def create(self, missaoqtd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova entrada de missaoqtd"""
        try:
            result = self.db.table("missaoqtd").insert(missaoqtd_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar missaoqtd: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_codigo(self, codigo: int) -> Dict[str, Any]:
        """Buscar missaoqtd por Código"""
        try:
            result = self.db.table("missaoqtd").select("*").eq("codigo", codigo).single().execute()
            
            if not result.data:
                return {"success": False, "error": "missaoqtd não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR missaoqtdModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as entradas de missaoqtd"""
        try:
            query = self.db.table("missaoqtd").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR missaoqtdModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def update(self, codigo: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar uma missaoqtd"""
        try:
            result = self.db.table("missaoqtd").update(update_data).eq("codigo", codigo).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar missaoqtd: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "missaoqtd não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            print(f"ERROR missaoqtdModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def delete(self, codigo: int) -> Dict[str, Any]:
        """Deletar uma missaoqtd"""
        try:
            result = self.db.table("missaoqtd").delete().eq("codigo", codigo).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar missaoqtd: {result.error}")
            
            return {"success": True, "message": "missaoqtd deletada com sucesso"}
        except Exception as e:
            print(f"ERROR missaoqtdModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
