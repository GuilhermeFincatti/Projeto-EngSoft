from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.usuario_controller import (
    UsuarioController, 
    UsuarioCreate, 
    UsuarioUpdate, 
    UsuarioResponse,
    ProfileStatsResponse,
    PhotoUploadRequest,
    XpRequest
)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])
controller = UsuarioController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Criar novo usuário",
    description="Cria um novo usuário no sistema. Requer autenticação.",
    responses={
        201: {"description": "Usuário criado com sucesso"},
        400: {"description": "Dados inválidos ou usuário já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Pessoa não encontrada"}
    }
)
def create_usuario(
    usuario_data: UsuarioCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar um novo usuário**
    
    - **nickname**: Nome único do usuário (deve existir na tabela pessoa)
    - **ranking**: Ranking inicial do usuário (padrão: "Iniciante")
    - **qtdcartas**: Quantidade inicial de cartas (padrão: 0)
    """
    result = controller.create_usuario(usuario_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/", 
    response_model=Dict[str, Any],
    summary="Listar usuários",
    description="Busca todos os usuários. Requer autenticação.",
    responses={
        200: {"description": "Lista de usuários retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_all_usuarios(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar todos os usuários**
    
    Parâmetros opcionais:
    - **limit**: Limita o número de resultados (1-100)
    """
    result = controller.get_all_usuarios(limit=limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Buscar usuário por nickname",
    description="Busca um usuário específico pelo nickname. Requer autenticação.",
    responses={
        200: {"description": "Usuário encontrado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"}
    }
)
def get_usuario_by_nickname(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar usuário por nickname**
    
    - **nickname**: Nome único do usuário a ser buscado
    """
    result = controller.get_usuario_by_nickname(nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.put(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Atualizar usuário",
    description="Atualiza os dados de um usuário existente. Requer autenticação.",
    responses={
        200: {"description": "Usuário atualizado com sucesso"},
        400: {"description": "Dados inválidos ou nenhum campo para atualizar"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"}
    }
)
def update_usuario(
    nickname: str, 
    update_data: UsuarioUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar dados de um usuário**
    
    - **nickname**: Nome único do usuário a ser atualizado
    - Campos opcionais para atualização:
      - **ranking**: Novo ranking do usuário
      - **qtdcartas**: Nova quantidade de cartas
    """
    result = controller.update_usuario(nickname, update_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Deletar usuário",
    description="Remove um usuário do sistema. Requer autenticação.",
    responses={
        200: {"description": "Usuário deletado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"}
    }
)
def delete_usuario(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar um usuário**
    
    - **nickname**: Nome único do usuário a ser deletado
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_usuario(nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.post(
    "/{nickname}/upload-photo",
    response_model=Dict[str, Any],
    summary="Upload de foto de perfil",
    description="Faz upload de uma foto de perfil para o Supabase Storage",
    responses={
        200: {"description": "Foto de perfil atualizada com sucesso"},
        400: {"description": "Dados da imagem inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro no upload da imagem"}
    }
)
def upload_profile_photo(
    nickname: str,
    photo_request: PhotoUploadRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Upload de foto de perfil**
    
    - **nickname**: Nome único do usuário
    - **photo_data**: Dados da imagem em base64
    """
    result = controller.upload_profile_photo(nickname, photo_request)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.post(
    "/{nickname}/add-xp",
    response_model=Dict[str, Any],
    summary="Adicionar XP ao usuário",
    description="Adiciona XP ao usuário e calcula automaticamente o novo nível e ranking",
    responses={
        200: {"description": "XP adicionado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
def add_xp(
    nickname: str,
    xp_request: XpRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Adicionar XP ao usuário**
    
    - **nickname**: Nome único do usuário
    - **xp_amount**: Quantidade de XP a ser adicionada
    """
    result = controller.add_xp(nickname, xp_request)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{nickname}/profile-stats",
    response_model=Dict[str, Any],
    summary="Obter estatísticas completas do perfil",
    description="Retorna estatísticas detalhadas do perfil, incluindo dados de coleção e ranking",
    responses={
        200: {"description": "Estatísticas do perfil retornadas com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_profile_stats(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Obter estatísticas completas do perfil**
    
    - **nickname**: Nome único do usuário
    
    Retorna:
    - Dados básicos do usuário (XP, nível, ranking)
    - Estatísticas da coleção de cartas
    - Posição no ranking geral
    - XP necessário para o próximo nível
    """
    result = controller.get_profile_stats(nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/leaderboard",
    response_model=Dict[str, Any],
    summary="Obter ranking dos usuários",
    description="Retorna o ranking dos usuários ordenados por XP",
    responses={
        200: {"description": "Ranking retornado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_leaderboard(
    limit: Optional[int] = Query(10, description="Limite de usuários no ranking", ge=1, le=100)
):
    """
    **Obter ranking dos usuários**
    
    Parâmetros opcionais:
    - **limit**: Limite de usuários a retornar (1-100, padrão: 10)
    """
    print(f"Fetching leaderboard with limit: {limit}")
    result = controller.get_leaderboard(limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result
