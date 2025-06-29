from typing import Dict, Any
from config.database import get_database

class ParticipaRaridadeModel:
    def __init__(self):
        self.db = get_database()

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova participação"""
        try:
            result = self.db.table("participararidade").insert(data).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar participação: {result.error}")
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_usuario_codigo(self, usuario: str, codigo: int) -> Dict[str, Any]:
        """Buscar participação por usuário e código"""
        try:
            result = self.db.table("participararidade").select("*") \
                .eq("usuario", usuario).eq("codigo", codigo).single().execute()
            if not result.data:
                return {"success": False, "error": "Participação não encontrada"}
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_all(self) -> Dict[str, Any]:
        """Buscar todas as participações"""
        try:
            result = self.db.table("participararidade").select("*").execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, usuario: str, codigo: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar participação"""
        try:
            result = self.db.table("participararidade").update(update_data) \
                .eq("usuario", usuario).eq("codigo", codigo).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar participação: {result.error}")
            if not result.data:
                return {"success": False, "error": "Participação não encontrada"}
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, usuario: str, codigo: int) -> Dict[str, Any]:
        """Deletar participação"""
        try:
            result = self.db.table("participararidade").delete() \
                .eq("usuario", usuario).eq("codigo", codigo).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar participação: {result.error}")
            return {"success": True, "message": "Participação deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
