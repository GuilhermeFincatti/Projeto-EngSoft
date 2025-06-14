from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.usuario_controller import (
    UsuarioController, 
    UsuarioCreate, 
    UsuarioUpdate, 
    UsuarioResponse
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
