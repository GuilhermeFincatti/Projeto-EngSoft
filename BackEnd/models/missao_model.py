from typing import Dict, Any
from config.database import get_database
import json

class MissaoModel:
    def __init__(self):
        self.db = get_database()

    def create(self, data: Any) -> Dict[str, Any]:
        """
        Criar nova missão.

        `data` deve ser uma instância de MissaoCreate (pydantic)
        """
        try:
            # Garantir que datetime será serializado corretamente
            data_serializado = json.loads(data.json())

            result = self.db.table("missao").insert(data_serializado).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar missão: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}

        except Exception as e:
            print(f"ERROR MissaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}


    def find_by_codigo(self, codigo: int) -> Dict[str, Any]:
        """Buscar missão por código"""
        try:
            result = self.db.table("missao").select("*").eq("codigo", codigo).single().execute()
            if not result.data:
                return {"success": False, "error": "Missão não encontrada"}
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR MissaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def find_all(self) -> Dict[str, Any]:
        """Buscar todas as missões"""
        try:
            result = self.db.table("missao").select("*").execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR MissaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def update(self, codigo: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar missão"""
        try:
            result = self.db.table("missao").update(update_data).eq("codigo", codigo).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar missão: {result.error}")
            if not result.data:
                return {"success": False, "error": "Missão não encontrada"}
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, codigo: int) -> Dict[str, Any]:
        """Deletar missão"""
        try:
            result = self.db.table("missao").delete().eq("codigo", codigo).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar missão: {result.error}")
            return {"success": True, "message": "Missão deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
