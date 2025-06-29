from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.missaoqtd_model import MissaoQtdModel

class MissaoQtdCreate(BaseModel):
    Codigo: int
    QuantidadeTotal: int

class MissaoQtdUpdate(BaseModel):
    QuantidadeTotal: Optional[int] = None

class MissaoQtdResponse(BaseModel):
    Codigo: int
    QuantidadeTotal: int

class MissaoQtdController:
    def __init__(self):
        self.model = MissaoQtdModel()
    
    def create_missaoqtd(self, missaoqtd_data: MissaoQtdCreate) -> Dict[str, Any]:
        """Criar uma nova MissaoQtd"""
        # Verificar se já existe MissaoQtd para o Código
        existing = self.model.find_by_codigo(missaoqtd_data.Codigo)
        if existing["success"]:
            return {
                "success": False,
                "error": "MissaoQtd com este Código já existe",
                "status_code": 400
            }
        
        result = self.model.create(missaoqtd_data.dict())

        if not result["success"]:
            result["status_code"] = 400
        
        return result

    def get_missaoqtd_by_codigo(self, codigo: int) -> Dict[str, Any]:
        """Buscar MissaoQtd por Código"""
        result = self.model.find_by_codigo(codigo)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result

    def get_all_missaoqtd(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as MissaoQtd"""
        result = self.model.find_all(limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result

    def update_missaoqtd(self, codigo: int, update_data: MissaoQtdUpdate) -> Dict[str, Any]:
        """Atualizar MissaoQtd"""
        # Verificar se MissaoQtd existe
        existing = self.model.find_by_codigo(codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "MissaoQtd não encontrada",
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
        
        result = self.model.update(codigo, update_dict)

        if not result["success"]:
            result["status_code"] = 400

        return result

    def delete_missaoqtd(self, codigo: int) -> Dict[str, Any]:
        """Deletar MissaoQtd"""
        # Verificar se existe
        existing = self.model.find_by_codigo(codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "MissaoQtd não encontrada",
                "status_code": 404
            }

        result = self.model.delete(codigo)

        if not result["success"]:
            result["status_code"] = 400

        return result
