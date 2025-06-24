from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from auth.auth_dependency import get_current_user
from controllers.missaoraridade_controller import (
    MissaoRaridadeController,
    MissaoRaridadeCreate
)

router = APIRouter(prefix="/missoes/raridade", tags=["MissaoRaridade"])
controller = MissaoRaridadeController()

@router.post("/", response_model=Dict[str, Any], status_code=201)
def create_relacao(data: MissaoRaridadeCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.create_relacao(data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result

@router.get("/", response_model=Dict[str, Any])
def get_all(current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_all_relacoes()
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 500), detail=result["error"])
    return result

@router.get("/{codigo}/{cartarara}", response_model=Dict[str, Any])
def get_relacao(codigo: int, cartarara: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_relacao(codigo, cartarara)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 404), detail=result["error"])
    return result

@router.delete("/{codigo}/{cartarara}", response_model=Dict[str, Any])
def delete_relacao(codigo: int, cartarara: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.delete_relacao(codigo, cartarara)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result
