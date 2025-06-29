from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.missaoqtd_controller import (
    MissaoQtdController,
    MissaoQtdCreate,
    MissaoQtdUpdate,
    MissaoQtdResponse
)

router = APIRouter(prefix="/missaoqtd", tags=["MissaoQtd"])
controller = MissaoQtdController()

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=201,
    summary="Criar nova MissaoQtd",
    description="Cria uma nova entrada de MissaoQtd no sistema. Requer autenticação.",
    responses={
        201: {"description": "MissaoQtd criada com sucesso"},
        400: {"description": "Dados inválidos ou MissaoQtd já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def create_missaoqtd(
    missaoqtd_data: MissaoQtdCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar uma nova MissaoQtd**
    
    - **Codigo**: Código da missão (obrigatório, chave primária)
    - **QuantidadeTotal**: Quantidade total da missão (obrigatório)
    """
    result = controller.create_missaoqtd(missaoqtd_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/",
    response_model=Dict[str, Any],
    summary="Listar MissaoQtd",
    description="Busca todas as entradas de MissaoQtd com limite opcional. Requer autenticação.",
    responses={
        200: {"description": "Lista de MissaoQtd retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_all_missaoqtd(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar todas as MissaoQtd**
    
    Parâmetro opcional:
    - **limit**: Número máximo de resultados (1-100)
    """
    result = controller.get_all_missaoqtd(limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{codigo}",
    response_model=Dict[str, Any],
    summary="Buscar MissaoQtd por código",
    description="Busca uma MissaoQtd específica pelo código. Requer autenticação.",
    responses={
        200: {"description": "MissaoQtd encontrada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "MissaoQtd não encontrada"}
    }
)
def get_missaoqtd_by_codigo(
    codigo: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar MissaoQtd por código**
    
    - **codigo**: Código da missão
    """
    result = controller.get_missaoqtd_by_codigo(codigo)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.put(
    "/{codigo}",
    response_model=Dict[str, Any],
    summary="Atualizar MissaoQtd",
    description="Atualiza os dados de uma MissaoQtd existente. Requer autenticação.",
    responses={
        200: {"description": "MissaoQtd atualizada com sucesso"},
        400: {"description": "Dados inválidos ou nenhum campo para atualizar"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "MissaoQtd não encontrada"}
    }
)
def update_missaoqtd(
    codigo: int,
    update_data: MissaoQtdUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar MissaoQtd**
    
    - **codigo**: Código da missão a ser atualizada
    - Campos opcionais:
      - **QuantidadeTotal**: Novo valor da quantidade total
    """
    result = controller.update_missaoqtd(codigo, update_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{codigo}",
    response_model=Dict[str, Any],
    summary="Deletar MissaoQtd",
    description="Remove uma MissaoQtd do sistema. Requer autenticação.",
    responses={
        200: {"description": "MissaoQtd deletada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "MissaoQtd não encontrada"}
    }
)
def delete_missaoqtd(
    codigo: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar uma MissaoQtd**
    
    - **codigo**: Código da missão a ser deletada
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_missaoqtd(codigo)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
