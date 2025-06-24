from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from auth.auth_dependency import get_current_user
from controllers.participararidade_controller import (
    ParticipaRaridadeController,
    ParticipaRaridadeCreate,
    ParticipaRaridadeUpdate
)

router = APIRouter(prefix="/participacoes/raridade", tags=["ParticipaRaridade"])
controller = ParticipaRaridadeController()

@router.post("/", response_model=Dict[str, Any], status_code=201)
def create_participacao(data: ParticipaRaridadeCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.create_participacao(data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result

@router.get("/", response_model=Dict[str, Any])
def get_all(current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_all_participacoes()
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 500), detail=result["error"])
    return result

@router.get("/{usuario}/{codigo}", response_model=Dict[str, Any])
def get_participacao(usuario: str, codigo: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.get_participacao(usuario, codigo)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 404), detail=result["error"])
    return result

@router.put("/{usuario}/{codigo}", response_model=Dict[str, Any])
def update_participacao(usuario: str, codigo: int, update_data: ParticipaRaridadeUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.update_participacao(usuario, codigo, update_data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result

@router.delete("/{usuario}/{codigo}", response_model=Dict[str, Any])
def delete_participacao(usuario: str, codigo: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    result = controller.delete_participacao(usuario, codigo)
    if not result["success"]:
        raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
    return result
