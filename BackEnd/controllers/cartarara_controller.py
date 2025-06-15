from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.cartarara_model import CartaRaraModel

class CartaRaraCreate(BaseModel):
    qrcode: str
    historia: str

class CartaRaraUpdate(BaseModel):
    historia: Optional[str] = None

class CartaRaraResponse(BaseModel):
    qrcode: str
    historia: str

class CartaRaraController:
    def __init__(self):
        self.model = CartaRaraModel()
    
    def create_cartarara(self, cartarara_data: CartaRaraCreate) -> Dict[str, Any]:
        """Criar uma nova CartaRara"""
        # Verificar se já existe uma CartaRara com o mesmo QRCode
        existing = self.model.find_by_qrcode(cartarara_data.qrcode)
        if existing["success"]:
            return {
                "success": False,
                "error": "Já existe uma CartaRara com este QRCode",
                "status_code": 400
            }
        
        result = self.model.create(cartarara_data.dict())

        if not result["success"]:
            result["status_code"] = 400

        return result

    def get_cartarara_by_qrcode(self, qrcode: str) -> Dict[str, Any]:
        """Buscar CartaRara por QRCode"""
        result = self.model.find_by_qrcode(qrcode)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result

    def get_all_cartararas(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as CartasRaras"""
        result = self.model.find_all(limit)

        if not result["success"]:
            result["status_code"] = 500

        return result

    def update_cartarara(self, qrcode: str, update_data: CartaRaraUpdate) -> Dict[str, Any]:
        """Atualizar CartaRara"""
        # Verificar se a CartaRara existe
        existing = self.model.find_by_qrcode(qrcode)
        if not existing["success"]:
            return {
                "success": False,
                "error": "CartaRara não encontrada",
                "status_code": 404
            }
        
        # Filtrar apenas campos não nulos
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_dict:
            return {
                "success": False,
                "error": "Nenhum campo para atualizar",
                "status_code": 400
            }
        
        result = self.model.update(qrcode, update_dict)

        if not result["success"]:
            result["status_code"] = 400

        return result

    def delete_cartarara(self, qrcode: str) -> Dict[str, Any]:
        """Deletar CartaRara"""
        # Verificar se existe
        existing = self.model.find_by_qrcode(qrcode)
        if not existing["success"]:
            return {
                "success": False,
                "error": "CartaRara não encontrada",
                "status_code": 404
            }
        
        result = self.model.delete(qrcode)

        if not result["success"]:
            result["status_code"] = 400

        return result
