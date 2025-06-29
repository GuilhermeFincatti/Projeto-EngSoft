from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.carta_controller import (
    CartaController, 
    CartaCreate, 
    CartaUpdate, 
    CartaResponse
)

router = APIRouter(prefix="/cartas", tags=["Cartas"])
controller = CartaController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Criar nova carta",
    description="Cria uma nova carta no sistema. Requer autenticação.",
    responses={
        201: {"description": "Carta criada com sucesso"},
        400: {"description": "Dados inválidos ou QRCode já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def create_carta(
    carta_data: CartaCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) :
    """
    **Criar uma nova carta**
    
    - **qrcode**: Código QR único da carta (obrigatório)
    - **raridade**: Raridade da carta - 'comum', 'rara', 'épica' ou 'lendária' (obrigatório)
    - **imagem**: URL da imagem da carta (opcional)
    - **audio**: URL do áudio da carta (opcional)
    - **localizacao**: Localização da carta no campus (opcional)
    """
    result = controller.create_carta(carta_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/", 
    response_model=Dict[str, Any],
    summary="Listar cartas",
    description="Busca todas as cartas com filtros opcionais. Requer autenticação.",
    responses={
        200: {"description": "Lista de cartas retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_all_cartas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    raridade: Optional[str] = Query(None, description="Filtrar por raridade", enum=["comum", "rara", "épica", "lendária"]),
    localizacao: Optional[str] = Query(None, description="Filtrar por localização (busca parcial)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar todas as cartas**
    
    Parâmetros de filtro opcionais:
    - **limit**: Limita o número de resultados (1-100)
    - **raridade**: Filtra por raridade específica
    - **localizacao**: Busca por localização (permite busca parcial)
    """
    result = controller.get_all_cartas(limit=limit, raridade=raridade, localizacao=localizacao)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/raras", 
    response_model=Dict[str, Any],
    summary="Buscar cartas raras",
    description="Busca cartas raras com informações de história. Requer autenticação.",
    responses={
        200: {"description": "Cartas raras retornadas com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_cartas_raras(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar cartas raras com história**
    
    Retorna cartas raras que possuem informações históricas adicionais.
    """
    result = controller.get_cartas_raras()
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{qrcode}", 
    response_model=Dict[str, Any],
    summary="Buscar carta por QRCode",
    description="Busca uma carta específica pelo QRCode. Requer autenticação.",
    responses={
        200: {"description": "Carta encontrada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada"}
    }
)
def get_carta_by_qrcode(
    qrcode: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar carta por QRCode**
    
    - **qrcode**: Código QR único da carta a ser buscada
    """
    result = controller.get_carta_by_qrcode(qrcode)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.put(
    "/{qrcode}", 
    response_model=Dict[str, Any],
    summary="Atualizar carta",
    description="Atualiza os dados de uma carta existente. Requer autenticação.",
    responses={
        200: {"description": "Carta atualizada com sucesso"},
        400: {"description": "Dados inválidos ou nenhum campo para atualizar"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada"}
    }
)
def update_carta(
    qrcode: str, 
    update_data: CartaUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar dados de uma carta**
    
    - **qrcode**: Código QR único da carta a ser atualizada
    - Campos opcionais para atualização:
      - **raridade**: Nova raridade ('comum', 'rara', 'épica', 'lendária')
      - **imagem**: Nova URL da imagem
      - **audio**: Nova URL do áudio
      - **localizacao**: Nova localização
    """
    result = controller.update_carta(qrcode, update_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{qrcode}", 
    response_model=Dict[str, Any],
    summary="Deletar carta",
    description="Remove uma carta do sistema. Requer autenticação.",
    responses={
        200: {"description": "Carta deletada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Carta não encontrada"}
    }
)
def delete_carta(
    qrcode: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar uma carta**
    
    - **qrcode**: Código QR único da carta a ser deletada
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_carta(qrcode)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
