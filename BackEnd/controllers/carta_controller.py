from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from models.carta_model import CartaModel

class CartaCreate(BaseModel):
    qrcode: str
    raridade: str
    imagem: Optional[str] = None
    audio: Optional[str] = None
    localizacao: Optional[str] = None

class CartaUpdate(BaseModel):
    raridade: Optional[str] = None
    imagem: Optional[str] = None
    audio: Optional[str] = None
    localizacao: Optional[str] = None

class CartaResponse(BaseModel):
    qrcode: str
    raridade: Optional[str]
    imagem: Optional[str]
    audio: Optional[str]
    localizacao: Optional[str]

class CartaController:
    def __init__(self):
        self.model = CartaModel()
    
    def create_carta(self, carta_data: CartaCreate) -> Dict[str, Any]:
        """Criar uma nova carta"""
        # Validar raridade
        valid_raridades = ["comum", "rara", "épica", "lendária"]
        if carta_data.raridade.lower() not in valid_raridades:
            return {
                "success": False,
                "error": f"Raridade deve ser uma das seguintes: {', '.join(valid_raridades)}",
                "status_code": 400
            }
        
        # Verificar se QRCode já existe
        existing = self.model.find_by_qrcode(carta_data.qrcode)
        if existing["success"]:
            return {
                "success": False,
                "error": "QRCode já existe",
                "status_code": 400
            }
        
        # Criar carta
        result = self.model.create(carta_data.dict())
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_carta_by_qrcode(self, qrcode: str) -> Dict[str, Any]:
        """Buscar carta por QRCode"""
        result = self.model.find_by_qrcode(qrcode)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result
    
    def get_all_cartas(self, 
                      limit: Optional[int] = None, 
                      raridade: Optional[str] = None,
                      localizacao: Optional[str] = None) -> Dict[str, Any]:
        """Buscar todas as cartas com filtros opcionais"""
        if raridade:
            result = self.model.find_by_raridade(raridade)
        elif localizacao:
            result = self.model.find_by_localizacao(localizacao)
        else:
            result = self.model.find_all(limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def get_cartas_raras(self) -> Dict[str, Any]:
        """Buscar cartas raras com história"""
        result = self.model.get_cartas_raras()
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def update_carta(self, qrcode: str, update_data: CartaUpdate) -> Dict[str, Any]:
        """Atualizar carta"""
        # Verificar se carta existe
        existing = self.model.find_by_qrcode(qrcode)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Carta não encontrada",
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
        
        # Validar raridade se está sendo atualizada
        if "raridade" in update_dict:
            valid_raridades = ["comum", "rara", "épica", "lendária"]
            if update_dict["raridade"].lower() not in valid_raridades:
                return {
                    "success": False,
                    "error": f"Raridade deve ser uma das seguintes: {', '.join(valid_raridades)}",
                    "status_code": 400
                }
        
        result = self.model.update(qrcode, update_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def delete_carta(self, qrcode: str) -> Dict[str, Any]:
        """Deletar carta"""
        # Verificar se carta existe
        existing = self.model.find_by_qrcode(qrcode)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Carta não encontrada",
                "status_code": 404
            }
        
        result = self.model.delete(qrcode)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
