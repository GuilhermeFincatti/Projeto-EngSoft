from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from auth.auth_dependency import get_current_user
from controllers.missao_controller import (
    MissaoController,
    MissaoCreate,
    MissaoUpdate
)

router = APIRouter(prefix="/missoes", tags=["Missao"])
controller = MissaoController()

@router.post("/", response_model=Dict[str, Any], status_code=201)
def create_missao(data: MissaoCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.create_missao(data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result

@router.get("/", response_model=Dict[str, Any])
def get_all(current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_all_missoes()
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 500), detail=result["error"])
    return result

@router.get("/{codigo}", response_model=Dict[str, Any])
def get_missao(codigo: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_missao_by_codigo(codigo)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 404), detail=result["error"])
    return result

@router.put("/{codigo}", response_model=Dict[str, Any])
def update_missao(codigo: int, update_data: MissaoUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.update_missao(codigo, update_data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result

@router.delete("/{codigo}", response_model=Dict[str, Any])
def delete_missao(codigo: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.delete_missao(codigo)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result
