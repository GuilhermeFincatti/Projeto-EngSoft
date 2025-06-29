from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.chat_controller import (
    ChatController, 
    ChatCreate, 
    ChatResponse
)

router = APIRouter(prefix="/chats", tags=["Chats"])
controller = ChatController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Criar novo chat",
    description="Cria um novo chat entre o usuário autenticado e outro usuário.",
    responses={
        201: {"description": "Chat criado com sucesso"},
        400: {"description": "Dados inválidos ou chat já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"}
    }
)
def create_chat(
    chat_data: ChatCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar novo chat**
    
    - **usuario2**: Nickname do usuário com quem criar o chat
    """
    # Buscar o nickname do usuário atual
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario1_nickname = result["data"]["nickname"]
    
    result = controller.create_chat(chat_data, usuario1_nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/", 
    response_model=Dict[str, Any],
    summary="Listar meus chats",
    description="Busca todos os chats do usuário autenticado.",
    responses={
        200: {"description": "Lista de chats retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_meus_chats(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar meus chats**
    
    Retorna todos os chats onde o usuário autenticado participa.
    """
    # Buscar o nickname do usuário atual
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario_nickname = result["data"]["nickname"]
    
    result = controller.get_chats_by_usuario(usuario_nickname, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{usuario1}/{usuario2}", 
    response_model=Dict[str, Any],
    summary="Buscar chat específico",
    description="Busca um chat específico entre dois usuários. Requer autenticação.",
    responses={
        200: {"description": "Chat encontrado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Chat não encontrado"}
    }
)
def get_chat_by_usuarios(
    usuario1: str,
    usuario2: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar chat entre dois usuários**
    
    - **usuario1**: Nickname do primeiro usuário
    - **usuario2**: Nickname do segundo usuário
    """
    result = controller.get_chat_by_usuarios(usuario1, usuario2)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{usuario1}/{usuario2}", 
    response_model=Dict[str, Any],
    summary="Deletar chat",
    description="Remove um chat entre dois usuários. Requer autenticação.",
    responses={
        200: {"description": "Chat deletado com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Chat não encontrado"}
    }
)
def delete_chat(
    usuario1: str,
    usuario2: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar chat**
    
    - **usuario1**: Nickname do primeiro usuário
    - **usuario2**: Nickname do segundo usuário
    
    ⚠️ **Atenção**: Esta operação é irreversível e apagará todas as mensagens do chat!
    """
    result = controller.delete_chat(usuario1, usuario2)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
