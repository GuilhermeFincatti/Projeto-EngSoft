from pydantic import BaseModel
from typing import Dict, Any
from models.missaoraridade_model import MissaoRaridadeModel

class MissaoRaridadeCreate(BaseModel):
    Codigo: int
    CartaRara: str

class MissaoRaridadeResponse(BaseModel):
    Codigo: int
    CartaRara: str

class MissaoRaridadeController:
    def __init__(self):
        self.model = MissaoRaridadeModel()
    
    def create_relacao(self, data: MissaoRaridadeCreate) -> Dict[str, Any]:
        """Criar nova relação missão-raridade"""
        existing = self.model.find_by_codigo_qrcode(data.Codigo, data.CartaRara)
        if existing["success"]:
            return {
                "success": False,
                "error": "Relação já existe",
                "status_code": 400
            }

        result = self.model.create(data.dict())
        if not result["success"]:
            result["status_code"] = 400
        return result

    def get_relacao(self, codigo: int, cartarara: str) -> Dict[str, Any]:
        """Buscar relação missão-raridade"""
        result = self.model.find_by_codigo_qrcode(codigo, cartarara)
        if not result["success"]:
            result["status_code"] = 404
        return result

    def get_all_relacoes(self) -> Dict[str, Any]:
        """Buscar todas as relações"""
        result = self.model.find_all()
        if not result["success"]:
            result["status_code"] = 500
        return result

    def delete_relacao(self, codigo: int, cartarara: str) -> Dict[str, Any]:
        """Deletar relação missão-raridade"""
        existing = self.model.find_by_codigo_qrcode(codigo, cartarara)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Relação não encontrada",
                "status_code": 404
            }

        result = self.model.delete(codigo, cartarara)
        if not result["success"]:
            result["status_code"] = 400
        return result
