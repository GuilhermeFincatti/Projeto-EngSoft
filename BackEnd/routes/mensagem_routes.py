from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.mensagem_controller import (
    MensagemController, 
    MensagemCreate, 
)

router = APIRouter(prefix="/mensagens", tags=["Mensagens"])
controller = MensagemController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Criar nova mensagem",
    description="Cria uma nova mensagem no sistema. O destinatário será automaticamente o usuário autenticado.",
    responses={
        201: {"description": "Mensagem criada com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado na tabela pessoa"}
    }
)
def create_mensagem(
    mensagem_data: MensagemCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar uma nova mensagem**
    
    O destinatário é automaticamente definido como o usuário autenticado.
    
    - **remetente**: Nickname do remetente (obrigatório)
    - **texto**: Conteúdo da mensagem (obrigatório)
    - **carta**: QRCode da carta anexada (opcional)
    """
    # Buscar o nickname do usuário atual na tabela pessoa
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    destinatario_nickname = result["data"]["nickname"]
    
    # Criar mensagem com o destinatário sendo o usuário atual
    result = controller.create_mensagem(mensagem_data, destinatario_nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/", 
    response_model=Dict[str, Any],
    summary="Listar mensagens recebidas",
    description="Busca todas as mensagens recebidas pelo usuário autenticado.",
    responses={
        200: {"description": "Lista de mensagens retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado na tabela pessoa"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_mensagens_recebidas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar mensagens recebidas**
    
    Retorna todas as mensagens onde o usuário autenticado é o destinatário.
    
    Parâmetros opcionais:
    - **limit**: Limita o número de resultados (1-100)
    """
    # Buscar o nickname do usuário atual na tabela pessoa
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    destinatario_nickname = result["data"]["nickname"]
    
    # Buscar mensagens recebidas
    result = controller.get_mensagens_by_destinatario(destinatario_nickname, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/enviadas", 
    response_model=Dict[str, Any],
    summary="Listar mensagens enviadas",
    description="Busca todas as mensagens enviadas pelo usuário autenticado.",
    responses={
        200: {"description": "Lista de mensagens retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado na tabela pessoa"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_mensagens_enviadas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar mensagens enviadas**
    
    Retorna todas as mensagens onde o usuário autenticado é o remetente.
    
    Parâmetros opcionais:
    - **limit**: Limita o número de resultados (1-100)
    """
    # Buscar o nickname do usuário atual na tabela pessoa
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    remetente_nickname = result["data"]["nickname"]
    
    # Buscar mensagens enviadas
    result = controller.get_mensagens_by_remetente(remetente_nickname, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/conversa/{outro_usuario}", 
    response_model=Dict[str, Any],
    summary="Buscar conversa com outro usuário",
    description="Busca todas as mensagens trocadas entre o usuário autenticado e outro usuário.",
    responses={
        200: {"description": "Conversa encontrada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Usuário não encontrado na tabela pessoa"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_conversa(
    outro_usuario: str,
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar conversa com outro usuário**
    
    Retorna todas as mensagens trocadas entre o usuário autenticado e outro usuário.
    
    - **outro_usuario**: Nickname do outro usuário na conversa
    
    Parâmetros opcionais:
    - **limit**: Limita o número de resultados (1-100)
    """
    # Buscar o nickname do usuário atual na tabela pessoa
    result = controller.get_user_nickname_by_email(current_user.email)
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Usuário autenticado não encontrado na tabela pessoa"
        )
    
    usuario_atual = result["data"]["nickname"]
    
    # Buscar conversa entre os dois usuários
    result = controller.get_conversa(usuario_atual, outro_usuario, limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result
