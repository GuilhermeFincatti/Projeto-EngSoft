from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from auth.auth_dependency import get_current_user
from controllers.colecao_controller import (
    ColecaoController, 
    AdicionarCartaRequest, 
    RemoverCartaRequest
)

router = APIRouter(prefix="/api", tags=["Coleção"])
controller = ColecaoController()

@router.get(
    "/minha-colecao", 
    response_model=Dict[str, Any],
    summary="Buscar minha coleção",
    description="Busca todas as cartas coletadas pelo usuário autenticado.",
    responses={
        200: {"description": "Coleção retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_minha_colecao(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar minha coleção de cartas**
    
    Retorna todas as cartas coletadas pelo usuário autenticado, incluindo:
    - Informações básicas da carta (QRCode, raridade, imagem, etc.)
    - Quantidade de cada carta possuída
    """
    result = controller.get_minha_colecao(current_user)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.post(
    "/colecao/adicionar", 
    response_model=Dict[str, Any],
    status_code=201,
    summary="Adicionar carta à coleção",
    description="Adiciona uma carta à coleção do usuário autenticado.",
    responses={
        201: {"description": "Carta adicionada com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada"}
    }
)
def adicionar_carta_colecao(
    request: AdicionarCartaRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Adicionar carta à coleção**
    
    - **carta_id**: QRCode da carta a ser adicionada
    - **quantidade**: Quantidade a adicionar (padrão: 1)
    """
    result = controller.adicionar_carta(current_user, request)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/colecao/remover", 
    response_model=Dict[str, Any],
    summary="Remover carta da coleção",
    description="Remove uma carta da coleção do usuário autenticado.",
    responses={
        200: {"description": "Carta removida com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada na coleção"}
    }
)
def remover_carta_colecao(
    request: RemoverCartaRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Remover carta da coleção**
    
    - **carta_id**: QRCode da carta a ser removida
    - **quantidade**: Quantidade a remover (padrão: 1)
    
    Se a quantidade for igual ou maior que a possuída, a carta será removida completamente.
    """
    result = controller.remover_carta(current_user, request)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/colecao/estatisticas", 
    response_model=Dict[str, Any],
    summary="Estatísticas da coleção",
    description="Busca estatísticas detalhadas da coleção do usuário.",
    responses={
        200: {"description": "Estatísticas retornadas com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_estatisticas_colecao(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Estatísticas da coleção**
    
    Retorna informações estatísticas sobre a coleção do usuário:
    - Total de cartas coletadas
    - Número de cartas únicas
    - Distribuição por raridade
    """
    result = controller.get_estatisticas(current_user)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/colecao/verificar/{carta_id}", 
    response_model=Dict[str, Any],
    summary="Verificar se possui carta",
    description="Verifica se o usuário possui uma carta específica.",
    responses={
        200: {"description": "Carta encontrada na coleção"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada na coleção"}
    }
)
def verificar_carta_colecao(
    carta_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Verificar se possui carta**
    
    - **carta_id**: QRCode da carta a ser verificada
    """
    result = controller.verificar_carta(current_user, carta_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/colecao/limpar", 
    response_model=Dict[str, Any],
    summary="Limpar coleção",
    description="Remove todas as cartas da coleção do usuário. Operação irreversível!",
    responses={
        200: {"description": "Coleção limpa com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        400: {"description": "Erro ao limpar coleção"}
    }
)
def limpar_colecao(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Limpar toda a coleção**
    
    Atenção: Esta operação remove todas as cartas da coleção e é irreversível!
    """
    result = controller.limpar_colecao(current_user)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
