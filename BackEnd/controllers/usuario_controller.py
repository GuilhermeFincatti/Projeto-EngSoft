from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel

class UsuarioCreate(BaseModel):
    nickname: str
    ranking: str = "Iniciante"
    qtdcartas: int = 0

class UsuarioUpdate(BaseModel):
    ranking: Optional[str] = None
    qtdcartas: Optional[int] = None

class UsuarioResponse(BaseModel):
    nickname: str
    ranking: str
    qtdcartas: int

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()
        self.pessoa_model = PessoaModel()
    
    def get_user_nickname_by_email(self, email: str) -> Dict[str, Any]:
        """Buscar nickname do usuário por email"""
        return self.pessoa_model.find_by_email(email)
    
    def create_usuario(self, usuario_data: UsuarioCreate) -> Dict[str, Any]:
        """Criar um novo usuário"""
        # Verificar se pessoa existe
        pessoa_result = self.pessoa_model.find_by_nickname(usuario_data.nickname)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Pessoa não encontrada. Crie primeiro uma pessoa antes de criar o usuário.",
                "status_code": 404
            }
        
        # Verificar se pessoa é do tipo usuario
        if pessoa_result["data"]["tipo"].lower() != "usuario":
            return {
                "success": False,
                "error": "Pessoa deve ser do tipo 'usuario'",
                "status_code": 400
            }
        
        # Verificar se usuário já existe
        existing = self.model.find_by_nickname(usuario_data.nickname)
        if existing["success"]:
            return {
                "success": False,
                "error": "Usuário já existe",
                "status_code": 400
            }
        
        # Criar usuário
        result = self.model.create(usuario_data.dict())
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_usuario_by_nickname(self, nickname: str) -> Dict[str, Any]:
        """Buscar usuário por nickname"""
        result = self.model.find_by_nickname(nickname)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result
    
    def get_all_usuarios(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todos os usuários"""
        result = self.model.find_all(limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def update_usuario(self, nickname: str, update_data: UsuarioUpdate) -> Dict[str, Any]:
        """Atualizar usuário"""
        # Verificar se usuário existe
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
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
        
        result = self.model.update(nickname, update_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def delete_usuario(self, nickname: str) -> Dict[str, Any]:
        """Deletar usuário"""
        # Verificar se usuário existe
        existing = self.model.find_by_nickname(nickname)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        result = self.model.delete(nickname)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
