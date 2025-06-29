from typing import Dict, Any
from config.database import get_database

class MissaoRaridadeModel:
    def __init__(self):
        self.db = get_database()

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova missão-raridade"""
        try:
            result = self.db.table("missaoraridade").insert(data).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar missão-raridade: {result.error}")
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_codigo_qrcode(self, codigo: int, cartarara: str) -> Dict[str, Any]:
        """Buscar missão-raridade por código e QRCode"""
        try:
            result = self.db.table("missaoraridade").select("*") \
                .eq("codigo", codigo).eq("cartarara", cartarara).single().execute()
            if not result.data:
                return {"success": False, "error": "Relação não encontrada"}
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_all(self) -> Dict[str, Any]:
        """Buscar todas as relações missão-raridade"""
        try:
            result = self.db.table("missaoraridade").select("*").execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, codigo: int, cartarara: str) -> Dict[str, Any]:
        """Deletar missão-raridade"""
        try:
            result = self.db.table("missaoraridade").delete() \
                .eq("codigo", codigo).eq("cartarara", cartarara).execute()
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar relação: {result.error}")
            return {"success": True, "message": "Relação deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
