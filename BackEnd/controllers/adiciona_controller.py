from pydantic import BaseModel
from typing import Optional, Dict, Any
from models.adiciona_model import AdicionaModel
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel

class AdicionaCreate(BaseModel):
    usuario2: str
    status: str = "pendente"

class AdicionaUpdate(BaseModel):
    status: str

class AdicionaResponse(BaseModel):
    usuario1: str
    usuario2: str
    datahora: str
    status: str

class AdicionaController:
    def __init__(self):
        self.model = AdicionaModel()
        self.usuario_model = UsuarioModel()
        self.pessoa_model = PessoaModel()
    
    def get_user_nickname_by_email(self, email: str) -> Dict[str, Any]:
        """Buscar nickname do usuário por email"""
        return self.pessoa_model.find_by_email(email)
    
    def create_solicitacao(self, adiciona_data: AdicionaCreate, usuario1: str) -> Dict[str, Any]:
        """Criar nova solicitação de amizade"""
        # Verificar se usuário1 existe
        usuario1_result = self.usuario_model.find_by_nickname(usuario1)
        if not usuario1_result["success"]:
            return {
                "success": False,
                "error": "Usuário solicitante não encontrado",
                "status_code": 404
            }
        
        # Verificar se usuário2 existe
        usuario2_result = self.usuario_model.find_by_nickname(adiciona_data.usuario2)
        if not usuario2_result["success"]:
            return {
                "success": False,
                "error": "Usuário destinatário não encontrado",
                "status_code": 404
            }
        
        # Verificar se não é o mesmo usuário
        if usuario1 == adiciona_data.usuario2:
            return {
                "success": False,
                "error": "Não é possível adicionar a si mesmo",
                "status_code": 400
            }
        
        # Verificar se já existe solicitação
        existing = self.model.find_by_usuarios(usuario1, adiciona_data.usuario2)
        if existing["success"]:
            return {
                "success": False,
                "error": "Solicitação já existe entre estes usuários",
                "status_code": 400
            }
        
        # Validar status
        valid_status = ["pendente", "aceita", "rejeitada"]
        if adiciona_data.status.lower() not in valid_status:
            return {
                "success": False,
                "error": f"Status deve ser um dos seguintes: {', '.join(valid_status)}",
                "status_code": 400
            }
        
        # Criar solicitação
        solicitacao_dict = {
            "usuario1": usuario1,
            "usuario2": adiciona_data.usuario2,
            "status": adiciona_data.status
        }
        
        result = self.model.create(solicitacao_dict)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def get_solicitacoes_enviadas(self, usuario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar solicitações enviadas"""
        result = self.model.find_by_usuario1(usuario, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def get_solicitacoes_recebidas(self, usuario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar solicitações recebidas"""
        result = self.model.find_by_usuario2(usuario, limit)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def update_status_solicitacao(self, usuario1: str, usuario2: str, status_data: AdicionaUpdate) -> Dict[str, Any]:
        """Atualizar status da solicitação"""
        # Verificar se solicitação existe
        existing = self.model.find_by_usuarios(usuario1, usuario2)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Solicitação não encontrada",
                "status_code": 404
            }
        
        # Validar status
        valid_status = ["pendente", "aceita", "rejeitada"]
        if status_data.status.lower() not in valid_status:
            return {
                "success": False,
                "error": f"Status deve ser um dos seguintes: {', '.join(valid_status)}",
                "status_code": 400
            }
        
        result = self.model.update_status(usuario1, usuario2, status_data.status)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
    
    def delete_solicitacao(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Deletar solicitação"""
        # Verificar se solicitação existe
        existing = self.model.find_by_usuarios(usuario1, usuario2)
        if not existing["success"]:
            return {
                "success": False,
                "error": "Solicitação não encontrada",
                "status_code": 404
            }
        
        result = self.model.delete(usuario1, usuario2)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
