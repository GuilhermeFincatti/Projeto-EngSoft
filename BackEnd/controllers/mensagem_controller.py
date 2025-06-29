from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from models.mensagem_model import MensagemModel
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel

class MensagemCreate(BaseModel):
    remetente: str
    texto: str
    carta: Optional[str] = None

class MensagemResponse(BaseModel):
    remetente: str
    destinatario: str
    datahora: str
    texto: str
    carta: Optional[str] = None

class PessoaUpdate(BaseModel):
    email: Optional[EmailStr] = None
    tipo: Optional[str] = None

class PessoaResponse(BaseModel):
    nickname: str
    email: str
    tipo: str

class MensagemController:
    def __init__(self):
        self.model = MensagemModel()
        self.usuario_model = UsuarioModel()
        self.pessoa_model = PessoaModel()
    
    def get_user_nickname_by_email(self, email: str) -> Dict[str, Any]:
        """Buscar nickname do usuário por email"""
        return self.pessoa_model.find_by_email(email)
    
    def create_mensagem(self, mensagem_data: MensagemCreate, destinatario: str) -> Dict[str, Any]:
        """Criar uma nova mensagem"""
        # Verificar se remetente existe
        remetente_result = self.pessoa_model.find_by_nickname(mensagem_data.remetente)
        if not remetente_result["success"]:
            return {
                "success": False,
                "error": "Remetente não encontrado",
                "status_code": 404
            }
        
        # Verificar se destinatário existe
        destinatario_result = self.pessoa_model.find_by_nickname(destinatario)
        if not destinatario_result["success"]:
            return {
                "success": False,
                "error": "Destinatário não encontrado",
                "status_code": 404
            }
        
        # Verificar se carta existe (se fornecida)
        if mensagem_data.carta:
            # Aqui você pode adicionar validação da carta se necessário
            pass
        
        # Criar mensagem
        mensagem_dict = {
            "remetente": mensagem_data.remetente,
            "destinatario": destinatario,
            "texto": mensagem_data.texto,
            "carta": mensagem_data.carta
        }
        
        result = self.model.create(mensagem_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_mensagens_by_destinatario(self, destinatario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar mensagens por destinatário"""
        result = self.model.find_by_destinatario(destinatario, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def get_mensagens_by_remetente(self, remetente: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar mensagens por remetente"""
        result = self.model.find_by_remetente(remetente, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def get_conversa(self, usuario1: str, usuario2: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar conversa entre dois usuários"""
        result = self.model.find_conversa(usuario1, usuario2, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
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
