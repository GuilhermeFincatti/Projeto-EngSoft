from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from auth.auth_dependency import get_current_user
from controllers.educador_controller import (
    EducadorController,
    EducadorCreate,
    EducadorUpdate,
    EducadorResponse
)

router = APIRouter(prefix="/educadores", tags=["Educadores"])
controller = EducadorController()

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=201,
    summary="Criar novo educador",
    description="Cria um novo educador no sistema. Requer autenticação.",
    responses={
        201: {"description": "Educador criado com sucesso"},
        400: {"description": "Dados inválidos ou educador já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def create_educador(
    educador_data: EducadorCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = controller.create_educador(educador_data)
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    return result

@router.get(
    "/{nickname}",
    response_model=Dict[str, Any],
    summary="Buscar educador por nickname",
    description="Busca um educador pelo seu nickname. Requer autenticação.",
    responses={
        200: {"description": "Educador encontrado com sucesso"},
        401: {"description": "Token inválido"},
        404: {"description": "Educador não encontrado"}
    }
)
def get_educador_by_nickname(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = controller.get_educador_by_nickname(nickname)
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    return result

@router.get(
    "/",
    response_model=Dict[str, Any],
    summary="Listar educadores",
    description="Lista todos os educadores, com filtro opcional por cargo.",
    responses={
        200: {"description": "Educadores listados com sucesso"},
        401: {"description": "Token inválido"},
        500: {"description": "Erro interno"}
    }
)
def get_all_educadores(
    cargo: str = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = controller.get_all_educadores(cargo=cargo)
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    return result

@router.put(
    "/{nickname}",
    response_model=Dict[str, Any],
    summary="Atualizar educador",
    description="Atualiza os dados de um educador. Requer autenticação.",
    responses={
        200: {"description": "Educador atualizado com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Token inválido"},
        404: {"description": "Educador não encontrado"}
    }
)
def update_educador(
    nickname: str,
    update_data: EducadorUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = controller.update_educador(nickname, update_data)
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    return result

@router.delete(
    "/{nickname}",
    response_model=Dict[str, Any],
    summary="Deletar educador",
    description="Remove um educador do sistema. Requer autenticação.",
    responses={
        200: {"description": "Educador deletado com sucesso"},
        401: {"description": "Token inválido"},
        404: {"description": "Educador não encontrado"}
    }
)
def delete_educador(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = controller.delete_educador(nickname)
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    return result
