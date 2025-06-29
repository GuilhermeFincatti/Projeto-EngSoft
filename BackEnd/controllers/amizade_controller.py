from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from models.amizade_model import AmizadeModel
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel

class SolicitacaoAmizadeRequest(BaseModel):
    destinatario: str

class AmizadeResponse(BaseModel):
    amizade_id: int
    nickname: str
    ranking: str
    xp: int
    nivel: int
    fotoperfil: Optional[str] = None
    data_amizade: Optional[str] = None

class SolicitacaoResponse(BaseModel):
    solicitacao_id: int
    nickname: str
    ranking: str
    xp: int
    nivel: int
    fotoperfil: Optional[str] = None
    data_solicitacao: Optional[str] = None

class AmizadeController:
    def __init__(self):
        self.model = AmizadeModel()
        self.usuario_model = UsuarioModel()
        self.pessoa_model = PessoaModel()
    
    def _get_nickname_from_email(self, email: str) -> Dict[str, Any]:
        """Buscar nickname do usuário pelo email"""
        pessoa_result = self.pessoa_model.find_by_email(email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        return {
            "success": True,
            "data": pessoa_result["data"]["nickname"]
        }
    
    def enviar_solicitacao(self, solicitante: str, solicitacao_data: SolicitacaoAmizadeRequest) -> Dict[str, Any]:
        """Enviar solicitação de amizade"""
        try:
            # Verificar se solicitante existe na tabela usuario
            solicitante_result = self.usuario_model.find_by_nickname(solicitante)
            if not solicitante_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário solicitante não encontrado na tabela de usuários",
                    "status_code": 404
                }
            
            # Verificar se destinatário existe
            destinatario_result = self.usuario_model.find_by_nickname(solicitacao_data.destinatario)
            if not destinatario_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário destinatário não encontrado",
                    "status_code": 404
                }
            
            # Verificar se não está tentando adicionar a si mesmo
            if solicitante == solicitacao_data.destinatario:
                return {
                    "success": False,
                    "error": "Não é possível enviar solicitação para si mesmo",
                    "status_code": 400
                }
            
            result = self.model.enviar_solicitacao(solicitante, solicitacao_data.destinatario)
            
            if not result["success"]:
                result["status_code"] = 400
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def aceitar_solicitacao(self, solicitacao_id: int) -> Dict[str, Any]:
        """Aceitar solicitação de amizade"""
        try:
            result = self.model.aceitar_solicitacao(solicitacao_id)
            
            if not result["success"]:
                result["status_code"] = 400
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def recusar_solicitacao(self, solicitacao_id: int) -> Dict[str, Any]:
        """Recusar solicitação de amizade"""
        try:
            result = self.model.recusar_solicitacao(solicitacao_id)
            
            if not result["success"]:
                result["status_code"] = 400
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def remover_amizade(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Remover amizade"""
        try:
            result = self.model.remover_amizade(usuario1, usuario2)
            
            if not result["success"]:
                result["status_code"] = 400
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def listar_amigos(self, nickname: str) -> Dict[str, Any]:
        """Listar amigos de um usuário"""
        try:
            result = self.model.listar_amigos(nickname)
            
            if not result["success"]:
                result["status_code"] = 500
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def listar_solicitacoes_pendentes(self, nickname: str) -> Dict[str, Any]:
        """Listar solicitações pendentes recebidas"""
        try:
            result = self.model.listar_solicitacoes_pendentes(nickname)
            
            if not result["success"]:
                result["status_code"] = 500
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def buscar_usuarios(self, termo_busca: str, usuario_atual: str, limit: int = 20) -> Dict[str, Any]:
        """Buscar usuários por nickname"""
        try:
            if len(termo_busca.strip()) < 2:
                return {
                    "success": False,
                    "error": "Termo de busca deve ter pelo menos 2 caracteres",
                    "status_code": 400
                }
            
            result = self.model.buscar_usuarios(termo_busca, usuario_atual, limit)
            
            if not result["success"]:
                result["status_code"] = 500
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def verificar_status_amizade(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Verificar status de amizade entre dois usuários"""
        try:
            result = self.model.verificar_status_amizade(usuario1, usuario2)
            
            if not result["success"]:
                result["status_code"] = 500
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
