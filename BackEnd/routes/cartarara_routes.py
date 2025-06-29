from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.cartarara_controller import (
    CartaRaraController,
    CartaRaraCreate,
    CartaRaraUpdate,
    CartaRaraResponse
)

router = APIRouter(prefix="/cartararas", tags=["CartaRara"])
controller = CartaRaraController()

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=201,
    summary="Criar nova CartaRara",
    description="Cria uma nova CartaRara no sistema. Requer autenticação.",
    responses={
        201: {"description": "CartaRara criada com sucesso"},
        400: {"description": "Dados inválidos ou QRCode já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def create_cartarara(
    cartarara_data: CartaRaraCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar uma nova CartaRara**
    
    - **qrcode**: Código QR único da carta (obrigatório)
    - **historia**: Texto com a história da carta (obrigatório)
    """
    result = controller.create_cartarara(cartarara_data)

    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )

    return result

@router.get(
    "/",
    response_model=Dict[str, Any],
    summary="Listar CartasRaras",
    description="Busca todas as CartasRaras com limite opcional. Requer autenticação.",
    responses={
        200: {"description": "Lista de CartasRaras retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_all_cartararas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar todas as CartasRaras**
    
    Parâmetro opcional:
    - **limit**: Número máximo de resultados (1-100)
    """
    result = controller.get_all_cartararas(limit)

    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )

    return result

@router.get(
    "/{qrcode}",
    response_model=Dict[str, Any],
    summary="Buscar CartaRara por QRCode",
    description="Busca uma CartaRara específica pelo QRCode. Requer autenticação.",
    responses={
        200: {"description": "CartaRara encontrada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "CartaRara não encontrada"}
    }
)
def get_cartarara_by_qrcode(
    qrcode: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar CartaRara por QRCode**
    
    - **qrcode**: Código QR da carta rara
    """
    result = controller.get_cartarara_by_qrcode(qrcode)

    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )

    return result

@router.put(
    "/{qrcode}",
    response_model=Dict[str, Any],
    summary="Atualizar CartaRara",
    description="Atualiza os dados de uma CartaRara existente. Requer autenticação.",
    responses={
        200: {"description": "CartaRara atualizada com sucesso"},
        400: {"description": "Nenhum campo para atualizar ou dados inválidos"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "CartaRara não encontrada"}
    }
)
def update_cartarara(
    qrcode: str,
    update_data: CartaRaraUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar dados de uma CartaRara**
    
    - **qrcode**: Código QR da carta rara
    - Campos opcionais:
      - **historia**: Novo texto da história
    """
    result = controller.update_cartarara(qrcode, update_data)

    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )

    return result

@router.delete(
    "/{qrcode}",
    response_model=Dict[str, Any],
    summary="Deletar CartaRara",
    description="Remove uma CartaRara do sistema. Requer autenticação.",
    responses={
        200: {"description": "CartaRara deletada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "CartaRara não encontrada"}
    }
)
def delete_cartarara(
    qrcode: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar uma CartaRara**
    
    - **qrcode**: Código QR da carta rara a ser deletada
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_cartarara(qrcode)

    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )

    return result
