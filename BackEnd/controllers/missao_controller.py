from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from models.missao_model import MissaoModel

class MissaoCreate(BaseModel):
    DataFim: Optional[datetime] = None
    Tipo: str
    Educador: str

class MissaoUpdate(BaseModel):
    DataFim: Optional[datetime] = None
    Tipo: Optional[str] = None
    Educador: Optional[str] = None

class MissaoResponse(BaseModel):
    Codigo: int
    DataInicio: datetime
    DataFim: Optional[datetime]
    Tipo: str
    Educador: str

class MissaoController:
    def __init__(self):
        self.model = MissaoModel()
    
    def create_missao(self, data: MissaoCreate) -> Dict[str, Any]:
        """Criar nova missão"""
        result = self.model.create(data)
        if not result["success"]:
            result["status_code"] = 400
        return result

    def get_missao_by_codigo(self, codigo: int) -> Dict[str, Any]:
        """Buscar missão por código"""
        result = self.model.find_by_codigo(codigo)
        if not result["success"]:
            result["status_code"] = 404
        return result

    def get_all_missoes(self) -> Dict[str, Any]:
        """Buscar todas as missões"""
        result = self.model.find_all()
        if not result["success"]:
            result["status_code"] = 500
        return result

    def update_missao(self, codigo: int, update_data: MissaoUpdate) -> Dict[str, Any]:
        """Atualizar missão"""
        existing = self.model.find_by_codigo(codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Missão não encontrada",
                "status_code": 404
            }

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if not update_dict:
            return {
                "success": False,
                "error": "Nenhum campo para atualizar",
                "status_code": 400
            }

        result = self.model.update(codigo, update_dict)
        if not result["success"]:
            result["status_code"] = 400

        return result

    def delete_missao(self, codigo: int) -> Dict[str, Any]:
        """Deletar missão"""
        existing = self.model.find_by_codigo(codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Missão não encontrada",
                "status_code": 404
            }

        result = self.model.delete(codigo)
        if not result["success"]:
            result["status_code"] = 400
        return result
