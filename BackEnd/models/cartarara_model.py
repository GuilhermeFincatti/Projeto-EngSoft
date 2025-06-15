from typing import Optional, Dict, Any
from config.database import get_database

class CartaRaraModel:
    def __init__(self):
        self.db = get_database()

    def create(self, cartarara_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova CartaRara"""
        try:
            result = self.db.table("cartarara").insert(cartarara_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar CartaRara: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_by_qrcode(self, qrcode: str) -> Dict[str, Any]:
        """Buscar CartaRara por QRCode"""
        try:
            result = self.db.table("cartarara").select("*").eq("qrcode", qrcode).single().execute()
            
            if not result.data:
                return {"success": False, "error": "CartaRara não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as CartasRaras"""
        try:
            query = self.db.table("cartarara").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, qrcode: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar uma CartaRara"""
        try:
            result = self.db.table("cartarara").update(update_data).eq("qrcode", qrcode).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar CartaRara: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "CartaRara não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, qrcode: str) -> Dict[str, Any]:
        """Deletar uma CartaRara"""
        try:
            result = self.db.table("cartarara").delete().eq("qrcode", qrcode).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar CartaRara: {result.error}")
            
            return {"success": True, "message": "CartaRara deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
