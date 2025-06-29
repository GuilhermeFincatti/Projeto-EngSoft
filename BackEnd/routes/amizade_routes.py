from fastapi import APIRouter, Query, Depends, HTTPException, Path
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.amizade_controller import (
    AmizadeController,
    SolicitacaoAmizadeRequest,
    AmizadeResponse,
    SolicitacaoResponse
)

router = APIRouter(prefix="/amizades", tags=["Amizades"])
controller = AmizadeController()

@router.post(
    "/solicitar",
    response_model=Dict[str, Any],
    summary="Enviar solicitação de amizade",
    description="Envia uma solicitação de amizade para outro usuário",
    responses={
        200: {"description": "Solicitação enviada com sucesso"},
        400: {"description": "Erro na solicitação"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário destinatário não encontrado"}
    }
)
def enviar_solicitacao(
    solicitacao_data: SolicitacaoAmizadeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Enviar solicitação de amizade**
    
    - **destinatario**: Nickname do usuário para quem enviar a solicitação
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    solicitante_nickname = nickname_result["data"]
    result = controller.enviar_solicitacao(solicitante_nickname, solicitacao_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.post(
    "/aceitar/{solicitacao_id}",
    response_model=Dict[str, Any],
    summary="Aceitar solicitação de amizade",
    description="Aceita uma solicitação de amizade recebida",
    responses={
        200: {"description": "Solicitação aceita com sucesso"},
        400: {"description": "Erro ao aceitar solicitação"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def aceitar_solicitacao(
    solicitacao_id: int = Path(..., description="ID da solicitação de amizade"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Aceitar solicitação de amizade**
    
    - **solicitacao_id**: ID da solicitação a ser aceita
    """
    result = controller.aceitar_solicitacao(solicitacao_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.post(
    "/recusar/{solicitacao_id}",
    response_model=Dict[str, Any],
    summary="Recusar solicitação de amizade",
    description="Recusa uma solicitação de amizade recebida",
    responses={
        200: {"description": "Solicitação recusada com sucesso"},
        400: {"description": "Erro ao recusar solicitação"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def recusar_solicitacao(
    solicitacao_id: int = Path(..., description="ID da solicitação de amizade"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Recusar solicitação de amizade**
    
    - **solicitacao_id**: ID da solicitação a ser recusada
    """
    result = controller.recusar_solicitacao(solicitacao_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/remover/{nickname}",
    response_model=Dict[str, Any],
    summary="Remover amizade",
    description="Remove uma amizade existente",
    responses={
        200: {"description": "Amizade removida com sucesso"},
        400: {"description": "Erro ao remover amizade"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def remover_amizade(
    nickname: str = Path(..., description="Nickname do amigo a ser removido"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Remover amizade**
    
    - **nickname**: Nickname do usuário a ser removido da lista de amigos
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    usuario_atual = nickname_result["data"]
    result = controller.remover_amizade(usuario_atual, nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/meus-amigos",
    response_model=Dict[str, Any],
    summary="Listar meus amigos",
    description="Lista todos os amigos do usuário atual",
    responses={
        200: {"description": "Lista de amigos retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def listar_meus_amigos(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Listar meus amigos**
    
    Retorna a lista completa de amigos do usuário atual
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    usuario_atual = nickname_result["data"]
    result = controller.listar_amigos(usuario_atual)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/solicitacoes-pendentes",
    response_model=Dict[str, Any],
    summary="Listar solicitações pendentes",
    description="Lista todas as solicitações de amizade pendentes recebidas",
    responses={
        200: {"description": "Lista de solicitações retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def listar_solicitacoes_pendentes(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Listar solicitações pendentes**
    
    Retorna todas as solicitações de amizade que foram enviadas para o usuário atual
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    usuario_atual = nickname_result["data"]
    result = controller.listar_solicitacoes_pendentes(usuario_atual)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/buscar",
    response_model=Dict[str, Any],
    summary="Buscar usuários",
    description="Busca usuários por nickname para adicionar como amigos",
    responses={
        200: {"description": "Lista de usuários encontrados"},
        400: {"description": "Termo de busca inválido"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def buscar_usuarios(
    q: str = Query(..., description="Termo de busca (nickname)", min_length=2),
    limit: int = Query(20, description="Limite de resultados", ge=1, le=50),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar usuários**
    
    - **q**: Termo de busca (deve ter pelo menos 2 caracteres)
    - **limit**: Número máximo de resultados (1-50)
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    usuario_atual = nickname_result["data"]
    result = controller.buscar_usuarios(q, usuario_atual, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/status/{nickname}",
    response_model=Dict[str, Any],
    summary="Verificar status de amizade",
    description="Verifica o status de amizade com um usuário específico",
    responses={
        200: {"description": "Status de amizade retornado"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def verificar_status_amizade(
    nickname: str = Path(..., description="Nickname do usuário"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Verificar status de amizade**
    
    - **nickname**: Nickname do usuário para verificar o status
    
    Retorna possíveis status: "nenhum", "pendente", "aceito", "recusado"
    """
    # Buscar nickname do usuário atual pelo email
    nickname_result = controller._get_nickname_from_email(current_user.email)
    if not nickname_result["success"]:
        raise HTTPException(
            status_code=nickname_result.get("status_code", 404),
            detail=nickname_result["error"]
        )
    
    usuario_atual = nickname_result["data"]
    result = controller.verificar_status_amizade(usuario_atual, nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result
