from typing import List, Optional, Dict, Any
from config.database import get_database

class CartaModel:
    def __init__(self):
        self.db = get_database()
    
    def create(self, carta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova carta"""
        try:
            result = self.db.table("carta").insert(carta_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar carta: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_qrcode(self, qrcode: str) -> Dict[str, Any]:
        """Buscar carta por QRCode"""
        try:
            result = self.db.table("carta").select("*").eq("qrcode", qrcode).single().execute()
            
            if not result.data:
                return {"success": False, "error": "Carta não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as cartas"""
        try:
            query = self.db.table("carta").select("*")
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_raridade(self, raridade: str) -> Dict[str, Any]:
        """Buscar cartas por raridade"""
        try:
            result = self.db.table("carta").select("*").eq("raridade", raridade).execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_localizacao(self, localizacao: str) -> Dict[str, Any]:
        """Buscar cartas por localização"""
        try:
            result = self.db.table("carta").select("*").ilike("localizacao", f"%{localizacao}%").execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update(self, qrcode: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar carta"""
        try:
            result = self.db.table("carta").update(update_data).eq("qrcode", qrcode).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar carta: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "Carta não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, qrcode: str) -> Dict[str, Any]:
        """Deletar carta"""
        try:
            result = self.db.table("carta").delete().eq("qrcode", qrcode).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar carta: {result.error}")
            
            return {"success": True, "message": "Carta deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_cartas_raras(self) -> Dict[str, Any]:
        """Buscar cartas raras com história"""
        try:
            result = (self.db.table("carta")
                     .select("*, cartarara(historia)")
                     .join("cartarara", "carta.qrcode", "cartarara.qrcode")
                     .execute())
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
