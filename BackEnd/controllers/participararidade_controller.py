from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.participararidade_model import ParticipaRaridadeModel

class ParticipaRaridadeCreate(BaseModel):
    usuario: str
    codigo: int
    status: str

class ParticipaRaridadeUpdate(BaseModel):
    status: Optional[str] = None

class ParticipaRaridadeResponse(BaseModel):
    usuario: str
    codigo: int
    status: str

class ParticipaRaridadeController:
    def __init__(self):
        self.model = ParticipaRaridadeModel()
    
    def create_participacao(self, data: ParticipaRaridadeCreate) -> Dict[str, Any]:
        """Criar nova participação"""
        existing = self.model.find_by_usuario_codigo(data.usuario, data.codigo)
        if existing["success"]:
            return {
                "success": False,
                "error": "Participação já existe",
                "status_code": 400
            }
        
        result = self.model.create(data.dict())
        if not result["success"]:
            result["status_code"] = 400
        
        return result

    def get_participacao(self, usuario: str, codigo: int) -> Dict[str, Any]:
        """Buscar participação por chave primária composta"""
        result = self.model.find_by_usuario_codigo(usuario, codigo)
        if not result["success"]:
            result["status_code"] = 404
        return result

    def get_all_participacoes(self) -> Dict[str, Any]:
        """Buscar todas as participações"""
        result = self.model.find_all()
        if not result["success"]:
            result["status_code"] = 500
        return result

    def update_participacao(self, usuario: str, codigo: int, update_data: ParticipaRaridadeUpdate) -> Dict[str, Any]:
        """Atualizar participação"""
        existing = self.model.find_by_usuario_codigo(usuario, codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Participação não encontrada",
                "status_code": 404
            }

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if not update_dict:
            return {
                "success": False,
                "error": "Nenhum campo para atualizar",
                "status_code": 400
            }

        result = self.model.update(usuario, codigo, update_dict)
        if not result["success"]:
            result["status_code"] = 400

        return result

    def delete_participacao(self, usuario: str, codigo: int) -> Dict[str, Any]:
        """Deletar participação"""
        existing = self.model.find_by_usuario_codigo(usuario, codigo)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Participação não encontrada",
                "status_code": 404
            }

        result = self.model.delete(usuario, codigo)
        if not result["success"]:
            result["status_code"] = 400
        return result
