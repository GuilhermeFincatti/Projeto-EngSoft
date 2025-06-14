from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.adiciona_controller import (
    AdicionaController, 
    AdicionaCreate, 
    AdicionaUpdate, 
    AdicionaResponse
)

router = APIRouter(prefix="/adiciona", tags=["Solicitações de Amizade"])
controller = AdicionaController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Enviar solicitação de amizade",
    description="Envia uma solicitação de amizade para outro usuário. O remetente é automaticamente o usuário autenticado.",
    responses={
        201: {"description": "Solicitação enviada com sucesso"},
        400: {"description": "Dados inválidos ou solicitação já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"}
    }
)
def create_solicitacao(
    adiciona_data: AdicionaCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Enviar solicitação de amizade**
    
    - **usuario2**: Nickname do usuário que receberá a solicitação
    - **status**: Status inicial da solicitação (padrão: "pendente")
    """
    # Buscar o nickname do usuário atual
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario1_nickname = result["data"]["nickname"]
    
    result = controller.create_solicitacao(adiciona_data, usuario1_nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/enviadas", 
    response_model=Dict[str, Any],
    summary="Listar solicitações enviadas",
    description="Busca todas as solicitações de amizade enviadas pelo usuário autenticado.",
    responses={
        200: {"description": "Lista de solicitações retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_solicitacoes_enviadas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar solicitações enviadas**
    
    Retorna todas as solicitações de amizade enviadas pelo usuário autenticado.
    """
    # Buscar o nickname do usuário atual
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario_nickname = result["data"]["nickname"]
    
    result = controller.get_solicitacoes_enviadas(usuario_nickname, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/recebidas", 
    response_model=Dict[str, Any],
    summary="Listar solicitações recebidas",
    description="Busca todas as solicitações de amizade recebidas pelo usuário autenticado.",
    responses={
        200: {"description": "Lista de solicitações retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_solicitacoes_recebidas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar solicitações recebidas**
    
    Retorna todas as solicitações de amizade recebidas pelo usuário autenticado.
    """
    # Buscar o nickname do usuário atual
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario_nickname = result["data"]["nickname"]
    
    result = controller.get_solicitacoes_recebidas(usuario_nickname, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.put(
    "/{usuario1}/{usuario2}", 
    response_model=Dict[str, Any],
    summary="Atualizar status da solicitação",
    description="Atualiza o status de uma solicitação de amizade. Requer autenticação.",
    responses={
        200: {"description": "Status atualizado com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Solicitação não encontrada"}
    }
)
def update_status_solicitacao(
    usuario1: str,
    usuario2: str,
    status_data: AdicionaUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar status da solicitação**
    
    - **usuario1**: Nickname do usuário que enviou a solicitação
    - **usuario2**: Nickname do usuário que recebeu a solicitação
    - **status**: Novo status ("pendente", "aceita", "rejeitada")
    """
    result = controller.update_status_solicitacao(usuario1, usuario2, status_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{usuario1}/{usuario2}", 
    response_model=Dict[str, Any],
    summary="Deletar solicitação",
    description="Remove uma solicitação de amizade. Requer autenticação.",
    responses={
        200: {"description": "Solicitação deletada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Solicitação não encontrada"}
    }
)
def delete_solicitacao(
    usuario1: str,
    usuario2: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar solicitação**
    
    - **usuario1**: Nickname do usuário que enviou a solicitação
    - **usuario2**: Nickname do usuário que recebeu a solicitação
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_solicitacao(usuario1, usuario2)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
