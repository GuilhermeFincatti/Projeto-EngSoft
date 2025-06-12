from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from models.pessoa_model import PessoaModel

class PessoaCreate(BaseModel):
    nickname: str
    email: EmailStr
    tipo: str

class PessoaUpdate(BaseModel):
    email: Optional[EmailStr] = None
    tipo: Optional[str] = None

class PessoaResponse(BaseModel):
    nickname: str
    email: str
    tipo: str

class PessoaController:
    def __init__(self):
        self.model = PessoaModel()
    
    def create_pessoa(self, pessoa_data: PessoaCreate) -> Dict[str, Any]:
        """Criar uma nova pessoa"""
        # Validar tipo
        valid_tipos = ["usuario", "educador"]
        if pessoa_data.tipo.lower() not in valid_tipos:
            return {
                "success": False,
                "error": f"Tipo deve ser um dos seguintes: {', '.join(valid_tipos)}",
                "status_code": 400
            }
        
        # Verificar se nickname já existe
        existing = self.model.find_by_nickname(pessoa_data.nickname)
        if existing["success"]:
            return {
                "success": False,
                "error": "Nickname já existe",
                "status_code": 400
            }
        
        # Verificar se email já existe
        existing_email = self.model.find_by_email(pessoa_data.email)
        if existing_email["success"]:
            return {
                "success": False,
                "error": "Email já está em uso",
                "status_code": 400
            }
        
        # Criar pessoa
        result = self.model.create(pessoa_data.dict())
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_pessoa_by_nickname(self, nickname: str) -> Dict[str, Any]:
        """Buscar pessoa por nickname"""
        result = self.model.find_by_nickname(nickname)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result
    
    def get_all_pessoas(self, limit: Optional[int] = None, tipo: Optional[str] = None) -> Dict[str, Any]:
        """Buscar todas as pessoas com filtros opcionais"""
        if tipo:
            result = self.model.find_by_tipo(tipo)
        else:
            result = self.model.find_all(limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def update_pessoa(self, nickname: str, update_data: PessoaUpdate) -> Dict[str, Any]:
        """Atualizar pessoa"""
        # Verificar se pessoa existe
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Pessoa não encontrada",
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
        
        # Verificar se email já existe (se está sendo atualizado)
        if "email" in update_dict:
            existing_email = self.model.find_by_email(update_dict["email"])
            if existing_email["success"] and existing_email["data"]["nickname"] != nickname:
                return {
                    "success": False,
                    "error": "Email já está em uso",
                    "status_code": 400
                }
        
        result = self.model.update(nickname, update_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def delete_pessoa(self, nickname: str) -> Dict[str, Any]:
        """Deletar pessoa"""
        # Verificar se pessoa existe
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Pessoa não encontrada",
                "status_code": 404
            }
        
        result = self.model.delete(nickname)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
