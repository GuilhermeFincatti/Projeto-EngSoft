from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.educador_model import EducadorModel
from models.pessoa_model import PessoaModel

class EducadorCreate(BaseModel):
    nickname: str
    cargo: str

class EducadorUpdate(BaseModel):
    cargo: Optional[str] = None

class EducadorResponse(BaseModel):
    nickname: str
    cargo: str

class EducadorController:
    def __init__(self):
        self.model = EducadorModel()
        self.pessoa_model = PessoaModel()

    def create_educador(self, educador_data: EducadorCreate) -> Dict[str, Any]:
        # Verifica se a pessoa existe e é do tipo educador
        pessoa = self.pessoa_model.find_by_nickname(educador_data.nickname)
        if not pessoa["success"]:
            return {"success": False, "error": "Pessoa não encontrada", "status_code": 404}

        if pessoa["data"]["tipo"].lower() != "educador":
            return {"success": False, "error": "A pessoa não é do tipo educador", "status_code": 400}

        result = self.model.create(educador_data.dict())
        if not result["success"]:
            result["status_code"] = 400
        return result

    def get_educador_by_nickname(self, nickname: str) -> Dict[str, Any]:
        result = self.model.find_by_nickname(nickname)
        if not result["success"]:
            result["status_code"] = 404
        return result

    def get_all_educadores(self, limit: Optional[int] = None, cargo: Optional[str] = None) -> Dict[str, Any]:
        """Buscar todos os educadores com filtros opcionais"""
        if cargo:
            result = self.model.find_by_cargo(cargo)
        else:
            result = self.model.find_all(limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result

    def update_educador(self, nickname: str, update_data: EducadorUpdate) -> Dict[str, Any]:
        # Verifica se educador existe
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {"success": False, "error": "Educador não encontrado", "status_code": 404}

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if not update_dict:
            return {"success": False, "error": "Nenhum campo para atualizar", "status_code": 400}

        result = self.model.update(nickname, update_dict)
        if not result["success"]:
            result["status_code"] = 400
        return result

    def delete_educador(self, nickname: str) -> Dict[str, Any]:
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {"success": False, "error": "Educador não encontrado", "status_code": 404}

        result = self.model.delete(nickname)
        if not result["success"]:
            result["status_code"] = 400
        return result
