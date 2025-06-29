from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from models.pessoa_model import PessoaModel
from models.colecao_model import ColecaoModel
from models.carta_model import CartaModel
from models.usuario_model import UsuarioModel

class AdicionarCartaRequest(BaseModel):
    carta_id: str  # QRCode da carta
    quantidade: Optional[int] = 1
    
    @validator('quantidade')
    def validate_quantidade(cls, v):
        if v < 1:
            raise ValueError('Quantidade deve ser maior que 0')
        return v

class RemoverCartaRequest(BaseModel):
    carta_id: str  # QRCode da carta
    quantidade: Optional[int] = 1
    
    @validator('quantidade')
    def validate_quantidade(cls, v):
        if v < 1:
            raise ValueError('Quantidade deve ser maior que 0')
        return v

class ColecaoController:
    def __init__(self):
        self.model = ColecaoModel()
        self.carta_model = CartaModel()
        self.pessoa_model = PessoaModel()
        self.usuario_model = UsuarioModel()
    
    def _calculate_xp_by_rarity(self, raridade: str) -> int:
        """Calcular XP baseado na raridade da carta"""
        xp_values = {
            "comum": 10,
            "incomum": 25,
            "rara": 50,
            "épica": 100,
            "lendária": 200
        }
        return xp_values.get(raridade.lower(), 10)
    
    def get_minha_colecao(self, current_user) -> Dict[str, Any]:
        """Buscar coleção do usuário"""
        # Buscar nickname do usuário pelo email
        pessoa_result = self.pessoa_model.find_by_email(current_user.email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        nickname = pessoa_result["data"]["nickname"]
        result = self.model.get_colecao_usuario(nickname)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def adicionar_carta(self, current_user, request: AdicionarCartaRequest) -> Dict[str, Any]:
        """Adicionar carta à coleção do usuário"""
        try:
            print(f"DEBUG: Recebendo request para adicionar carta")
            print(f"DEBUG: current_user = {current_user}")
            print(f"DEBUG: request.carta_id = {request.carta_id}")
            print(f"DEBUG: request.quantidade = {request.quantidade}")
            
            # Buscar nickname do usuário pelo email
            pessoa_result = self.pessoa_model.find_by_email(current_user.email)
            print(f"DEBUG: pessoa_result = {pessoa_result}")
            
            if not pessoa_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário não encontrado",
                    "status_code": 404
                }
            
            nickname = pessoa_result["data"]["nickname"]
            print(f"DEBUG: nickname encontrado = {nickname}")
            
            # Verificar se a carta existe
            carta_result = self.carta_model.find_by_qrcode(request.carta_id)
            print(f"DEBUG: carta_result = {carta_result}")
            
            if not carta_result["success"]:
                return {
                    "success": False,
                    "error": "Carta não encontrada",
                    "status_code": 404
                }
            
            # Verificar se o usuário já possui esta carta
            carta_existente = self.model.get_carta_usuario(nickname, request.carta_id)
            is_new_card = not carta_existente["success"]
            
            result = self.model.adicionar_carta(nickname, request.carta_id, request.quantidade)
            print(f"DEBUG: result adicionar_carta = {result}")
            
            if not result["success"]:
                result["status_code"] = 400
                return result
            
            # Se é uma carta nova, adicionar XP baseado na raridade
            if is_new_card:
                carta_data = carta_result["data"]
                raridade = carta_data.get("raridade", "comum")
                xp_ganho = self._calculate_xp_by_rarity(raridade)
                
                print(f"DEBUG: Carta nova coletada! Raridade: {raridade}, XP: {xp_ganho}")
                
                # Verificar se o usuário existe na tabela usuario
                usuario_result = self.usuario_model.find_by_nickname(nickname)
                if usuario_result["success"]:
                    # Adicionar XP ao usuário
                    current_xp = usuario_result["data"].get("xp", 0)
                    current_level = usuario_result["data"].get("nivel", 1)
                    current_qtdcartas = usuario_result["data"].get("qtdcartas", 0)
                    
                    new_xp = current_xp + xp_ganho
                    new_level = (new_xp // 1000) + 1
                    new_qtdcartas = current_qtdcartas + 1
                    
                    # Determinar novo ranking baseado no nível
                    new_ranking = self._calculate_ranking(new_level, new_xp)
                    
                    # Atualizar dados do usuário
                    update_data = {
                        "xp": new_xp,
                        "nivel": new_level,
                        "ranking": new_ranking,
                        "qtdcartas": new_qtdcartas
                    }
                    
                    update_result = self.usuario_model.update(nickname, update_data)
                    print(f"DEBUG: update_result usuario = {update_result}")
                    
                    if update_result["success"]:
                        level_up = new_level > current_level
                        result["xp_info"] = {
                            "xp_ganho": xp_ganho,
                            "xp_total": new_xp,
                            "nivel_atual": new_level,
                            "ranking": new_ranking,
                            "level_up": level_up,
                            "raridade": raridade
                        }
                else:
                    print(f"DEBUG: Usuário {nickname} não encontrado na tabela usuario, XP não adicionado")
            
            return result
            
        except Exception as e:
            print(f"ERROR: Erro inesperado em adicionar_carta: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def _calculate_ranking(self, level: int, xp: int) -> str:
        """Calcular ranking baseado no nível e XP"""
        if level >= 50:
            return "Lendário"
        elif level >= 30:
            return "Mestre"
        elif level >= 20:
            return "Especialista"
        elif level >= 10:
            return "Avançado"
        elif level >= 5:
            return "Intermediário"
        else:
            return "Iniciante"
    
    def remover_carta(self, current_user, request: RemoverCartaRequest) -> Dict[str, Any]:
        """Remover carta da coleção do usuário"""
        # Buscar nickname do usuário pelo email
        pessoa_result = self.pessoa_model.find_by_email(current_user.email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        nickname = pessoa_result["data"]["nickname"]
        result = self.model.remover_carta(nickname, request.carta_id, request.quantidade)
        
        if not result["success"]:
            if "não encontrada" in result["error"]:
                result["status_code"] = 404
            else:
                result["status_code"] = 400
        
        return result
    
    def get_estatisticas(self, current_user) -> Dict[str, Any]:
        """Buscar estatísticas da coleção do usuário"""
        # Buscar nickname do usuário pelo email
        pessoa_result = self.pessoa_model.find_by_email(current_user.email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        nickname = pessoa_result["data"]["nickname"]
        result = self.model.get_estatisticas_colecao(nickname)
        
        if not result["success"]:
            result["status_code"] = 500
        
        return result
    
    def verificar_carta(self, current_user, carta_id: str) -> Dict[str, Any]:
        """Verificar se usuário possui uma carta específica"""
        # Buscar nickname do usuário pelo email
        pessoa_result = self.pessoa_model.find_by_email(current_user.email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        nickname = pessoa_result["data"]["nickname"]
        result = self.model.get_carta_usuario(nickname, carta_id)
        
        if not result["success"]:
            if "não encontrada" in result["error"]:
                result["status_code"] = 404
            else:
                result["status_code"] = 500
        
        return result
    
    def limpar_colecao(self, current_user) -> Dict[str, Any]:
        """Limpar toda a coleção do usuário"""
        # Buscar nickname do usuário pelo email
        pessoa_result = self.pessoa_model.find_by_email(current_user.email)
        if not pessoa_result["success"]:
            return {
                "success": False,
                "error": "Usuário não encontrado",
                "status_code": 404
            }
        
        nickname = pessoa_result["data"]["nickname"]
        result = self.model.limpar_colecao(nickname)
        
        if not result["success"]:
            result["status_code"] = 400
        
        return result
