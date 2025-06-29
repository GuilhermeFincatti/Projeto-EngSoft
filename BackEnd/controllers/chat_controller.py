from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.chat_model import ChatModel
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel

class ChatCreate(BaseModel):
    usuario2: str

class ChatResponse(BaseModel):
    usuario1: str
    usuario2: str

class ChatController:
    def __init__(self):
        self.model = ChatModel()
        self.usuario_model = UsuarioModel()
        self.pessoa_model = PessoaModel()
    
    def get_user_nickname_by_email(self, email: str) -> Dict[str, Any]:
        """Buscar nickname do usuário por email"""
        return self.pessoa_model.find_by_email(email)
    
    def create_chat(self, chat_data: ChatCreate, usuario1: str) -> Dict[str, Any]:
        """Criar novo chat"""
        # Verificar se usuário1 existe
        usuario1_result = self.usuario_model.find_by_nickname(usuario1)
        if not usuario1_result["success"]:
            return {
                "success": False,
                "error": "Usuário 1 não encontrado",
                "status_code": 404
            }
        
        # Verificar se usuário2 existe
        usuario2_result = self.usuario_model.find_by_nickname(chat_data.usuario2)
        if not usuario2_result["success"]:
            return {
                "success": False,
                "error": "Usuário 2 não encontrado",
                "status_code": 404
            }
        
        # Verificar se não é o mesmo usuário
        if usuario1 == chat_data.usuario2:
            return {
                "success": False,
                "error": "Não é possível criar chat consigo mesmo",
                "status_code": 400
            }
        
        # Verificar se chat já existe
        existing = self.model.find_by_usuarios(usuario1, chat_data.usuario2)
        if existing["success"]:
            return {
                "success": False,
                "error": "Chat já existe entre estes usuários",
                "status_code": 400
            }
        
        # Criar chat (sempre com usuario1 sendo o menor lexicograficamente)
        usuarios_ordenados = sorted([usuario1, chat_data.usuario2])
        chat_dict = {
            "usuario1": usuarios_ordenados[0],
            "usuario2": usuarios_ordenados[1]
        }
        
        result = self.model.create(chat_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_chat_by_usuarios(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Buscar chat entre dois usuários"""
        result = self.model.find_by_usuarios(usuario1, usuario2)
        
        if not result["success"]:
            result["status_code"] = 404
        
        return result
    
    def get_chats_by_usuario(self, usuario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todos os chats de um usuário"""
        result = self.model.find_by_usuario(usuario, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def delete_chat(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Deletar chat"""
        # Verificar se chat existe
        existing = self.model.find_by_usuarios(usuario1, usuario2)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Chat não encontrado",
                "status_code": 404
            }
        
        result = self.model.delete(usuario1, usuario2)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
