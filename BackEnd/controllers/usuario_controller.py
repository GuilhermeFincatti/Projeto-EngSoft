from pydantic import BaseModel
from typing import Optional, Dict, Any
import base64
import uuid
from models.usuario_model import UsuarioModel
from models.pessoa_model import PessoaModel
from models.colecao_model import ColecaoModel
from config.database import get_database

class UsuarioCreate(BaseModel):
    nickname: str
    ranking: str = "Iniciante"
    qtdcartas: int = 0
    xp: int = 0
    fotoperfil: Optional[str] = None
    nivel: int = 1

class UsuarioUpdate(BaseModel):
    ranking: Optional[str] = None
    qtdcartas: Optional[int] = None
    xp: Optional[int] = None
    fotoperfil: Optional[str] = None
    nivel: Optional[int] = None

class UsuarioResponse(BaseModel):
    nickname: str
    ranking: str
    qtdcartas: int
    xp: int
    fotoperfil: Optional[str] = None
    nivel: int

class PhotoUploadRequest(BaseModel):
    photo_data: str  # Base64 encoded image data
    
class XpRequest(BaseModel):
    xp_amount: int

class ProfileStatsResponse(BaseModel):
    nickname: str
    ranking: str
    xp: int
    nivel: int
    qtdcartas: int
    fotoperfil: Optional[str] = None
    colecao_stats: Dict[str, Any]
    ranking_position: Optional[int] = None

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()
        self.pessoa_model = PessoaModel()
        self.colecao_model = ColecaoModel()
        self.db = get_database()
    
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
    
    def upload_profile_photo(self, nickname: str, photo_request: PhotoUploadRequest) -> Dict[str, Any]:
        """Upload de foto de perfil para o Supabase Storage"""
        try:
            # Verificar se usuário existe
            user_result = self.model.find_by_nickname(nickname)
            if not user_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário não encontrado",
                    "status_code": 404
                }
            
            # Decodificar base64
            try:
                photo_data = base64.b64decode(photo_request.photo_data)
            except Exception as e:
                return {
                    "success": False,
                    "error": "Dados da imagem inválidos",
                    "status_code": 400
                }
            
            # Gerar nome único para o arquivo
            file_extension = "jpg"  # Por padrão, pode ser melhorado para detectar o tipo
            filename = f"{nickname}_{uuid.uuid4()}.{file_extension}"
            
            # Para desenvolvimento local, usar fallback com data URL diretamente
            # Em produção, o bucket deve ser criado manualmente no Supabase Dashboard
            data_url = f"data:image/jpeg;base64,{photo_request.photo_data}"
            
            # Atualizar URL da foto no perfil do usuário com data URL
            update_result = self.model.update(nickname, {"fotoperfil": data_url})
            
            if not update_result["success"]:
                return {
                    "success": False,
                    "error": "Erro ao atualizar perfil com nova foto",
                    "status_code": 500
                }
            
            return {
                "success": True,
                "data": {
                    "fotoperfil": data_url,
                    "foto_url": data_url,
                    "message": "Foto de perfil atualizada com sucesso"
                }
            }
            
            # Código comentado para upload no Supabase Storage (requer configuração manual do bucket)
            """
            # Upload para Supabase Storage
            try:
                # Primeiro, tentar criar o bucket se não existir
                try:
                    self.db.storage.create_bucket("profile-photos", {"public": True})
                except Exception as bucket_error:
                    # Bucket já existe ou erro de permissão, continuar
                    print(f"Info: {bucket_error}")
                
                storage_result = self.db.storage.from_("profile-photos").upload(
                    filename, 
                    photo_data,
                    file_options={"content-type": "image/jpeg"}
                )
                
                # Verificar se houve erro no upload
                if hasattr(storage_result, 'error') and storage_result.error:
                    error_msg = str(storage_result.error)
                    if "row-level security policy" in error_msg.lower():
                        # Tentar upload com política diferente
                        raise Exception("Erro de permissão no storage. Verifique as políticas RLS do bucket.")
                    else:
                        raise Exception(f"Erro no upload: {storage_result.error}")
                
                # Obter URL pública da imagem
                public_url = self.db.storage.from_("profile-photos").get_public_url(filename)
                
                # Atualizar URL da foto no perfil do usuário
                update_result = self.model.update(nickname, {"fotoperfil": public_url})
                
                if not update_result["success"]:
                    return {
                        "success": False,
                        "error": "Erro ao atualizar perfil com nova foto",
                        "status_code": 500
                    }
                
                return {
                    "success": True,
                    "data": {
                        "fotoperfil": public_url,
                        "foto_url": public_url,
                        "message": "Foto de perfil atualizada com sucesso"
                    }
                }
                
            except Exception as e:
                # Se o upload para o Storage falhar, usar fallback com data URL
                error_msg = str(e)
                if "row-level security policy" in error_msg.lower() or "Unauthorized" in error_msg:
                    # Fallback: salvar como data URL na base64
                    data_url = f"data:image/jpeg;base64,{photo_request.photo_data}"
                    
                    # Atualizar URL da foto no perfil do usuário com data URL
                    update_result = self.model.update(nickname, {"fotoperfil": data_url})
                    
                    if not update_result["success"]:
                        return {
                            "success": False,
                            "error": "Erro ao atualizar perfil com nova foto",
                            "status_code": 500
                        }
                    
                    return {
                        "success": True,
                        "data": {
                            "fotoperfil": data_url,
                            "foto_url": data_url,
                            "message": "Foto de perfil atualizada com sucesso (modo local)"
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erro no upload da imagem: {str(e)}",
                        "status_code": 500
                    }
            """
                
        except Exception as e:
            import traceback
            traceback.print_exc()  # Logar o erro completo para depuração

            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def add_xp(self, nickname: str, xp_request: XpRequest) -> Dict[str, Any]:
        """Adicionar XP ao usuário e calcular novo nível"""
        try:
            # Verificar se usuário existe
            user_result = self.model.find_by_nickname(nickname)
            if not user_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário não encontrado",
                    "status_code": 404
                }
            
            current_user = user_result["data"]
            current_xp = current_user.get("xp", 0)
            current_level = current_user.get("nivel", 1)
            
            # Calcular novo XP
            new_xp = current_xp + xp_request.xp_amount
            
            # Calcular novo nível (exemplo: cada 1000 XP = 1 nível)
            new_level = (new_xp // 1000) + 1
            
            # Determinar novo ranking baseado no nível
            new_ranking = self._calculate_ranking(new_level, new_xp)
            
            # Atualizar dados do usuário
            update_data = {
                "xp": new_xp,
                "nivel": new_level,
                "ranking": new_ranking
            }
            
            update_result = self.model.update(nickname, update_data)
            
            if not update_result["success"]:
                return {
                    "success": False,
                    "error": "Erro ao atualizar XP do usuário",
                    "status_code": 500
                }
            
            level_up = new_level > current_level
            
            return {
                "success": True,
                "data": {
                    "xp_anterior": current_xp,
                    "xp_atual": new_xp,
                    "xp_adicionado": xp_request.xp_amount,
                    "nivel_anterior": current_level,
                    "nivel_atual": new_level,
                    "ranking": new_ranking,
                    "level_up": level_up
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def get_profile_stats(self, nickname: str) -> Dict[str, Any]:
        """Obter estatísticas completas do perfil do usuário"""
        try:
            # Buscar dados básicos do usuário
            user_result = self.model.find_by_nickname(nickname)
            if not user_result["success"]:
                return {
                    "success": False,
                    "error": "Usuário não encontrado",
                    "status_code": 404
                }
            
            user_data = user_result["data"]
            
            # Buscar estatísticas da coleção
            colecao_result = self.colecao_model.get_colecao_usuario(nickname)
            colecao_stats = self._calculate_collection_stats(colecao_result.get("data", []))
            
            # Buscar posição no ranking
            ranking_position = self._get_user_ranking_position(nickname)
            
            # Construir resposta completa
            profile_stats = {
                "nickname": user_data["nickname"],
                "ranking": user_data["ranking"],
                "xp": user_data["xp"],
                "nivel": user_data["nivel"],
                "qtdcartas": user_data["qtdcartas"],
                "fotoperfil": user_data.get("fotoperfil"),
                "colecao_stats": colecao_stats,
                "ranking_position": ranking_position,
                "xp_para_proximo_nivel": self._xp_for_next_level(user_data["xp"])
            }
            
            return {
                "success": True,
                "data": profile_stats
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def get_leaderboard(self, limit: int = 10) -> Dict[str, Any]:
        """Obter ranking dos usuários por XP"""
        try:
            # Buscar todos os usuários ordenados por XP
            result = self.db.table("usuario").select("nickname, ranking, xp, nivel, qtdcartas").order('xp', desc=True).limit(limit).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar ranking: {result.error}")
            
            # Adicionar posição no ranking
            leaderboard = []
            for i, user in enumerate(result.data, 1):
                user["posicao"] = i
                leaderboard.append(user)
            
            return {
                "success": True,
                "data": leaderboard
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "status_code": 500
            }
    
    def calculate_xp_by_rarity(self, raridade: str) -> int:
        """Calcular XP baseado na raridade da carta"""
        xp_values = {
            "comum": 10,
            "incomum": 25,
            "rara": 50,
            "épica": 100,
            "lendária": 200
        }
        return xp_values.get(raridade.lower(), 10)
    
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
    
    def _calculate_collection_stats(self, colecao_data: list) -> Dict[str, Any]:
        """Calcular estatísticas da coleção"""
        if not colecao_data:
            return {
                "total_cartas": 0,
                "cartas_unicas": 0,
                "raridades": {},
                "carta_mais_comum": None,
                "progresso_colecao": 0.0
            }
        
        total_cartas = sum(item["quantidade"] for item in colecao_data)
        cartas_unicas = len(colecao_data)
        
        # Contar por raridade
        raridades = {}
        for item in colecao_data:
            if item.get("carta") and item["carta"].get("raridade"):
                raridade = item["carta"]["raridade"]
                if raridade not in raridades:
                    raridades[raridade] = {"quantidade": 0, "unicas": 0}
                raridades[raridade]["quantidade"] += item["quantidade"]
                raridades[raridade]["unicas"] += 1
        
        # Encontrar carta mais comum
        carta_mais_comum = max(colecao_data, key=lambda x: x["quantidade"]) if colecao_data else None
        
        # Calcular progresso (assumindo 100 cartas totais disponíveis)
        total_cartas_disponivel = 100  # Isso pode ser obtido da tabela carta
        progresso_colecao = (cartas_unicas / total_cartas_disponivel) * 100
        
        return {
            "total_cartas": total_cartas,
            "cartas_unicas": cartas_unicas,
            "raridades": raridades,
            "carta_mais_comum": carta_mais_comum,
            "progresso_colecao": round(progresso_colecao, 2)
        }
    
    def _get_user_ranking_position(self, nickname: str) -> Optional[int]:
        """Obter posição do usuário no ranking geral"""
        try:
            result = self.db.table("usuario").select("nickname").order("xp", desc=True).execute()
            
            if result.data:
                for i, user in enumerate(result.data, 1):
                    if user["nickname"] == nickname:
                        return i
            
            return None
            
        except Exception:
            return None
    
    def _xp_for_next_level(self, current_xp: int) -> int:
        """Calcular XP necessário para o próximo nível"""
        current_level = (current_xp // 1000) + 1
        next_level_xp = current_level * 1000
        return next_level_xp - current_xp
