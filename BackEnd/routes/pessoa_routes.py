from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional, Dict, Any
from auth.auth_dependency import get_current_user
from controllers.pessoa_controller import (
    PessoaController, 
    PessoaCreate, 
    PessoaUpdate, 
    PessoaResponse
)

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])
controller = PessoaController()

@router.post(
    "/", 
    response_model=Dict[str, Any], 
    status_code=201,
    summary="Criar nova pessoa",
    description="Cria uma nova pessoa no sistema. Requer autenticação.",
    responses={
        201: {"description": "Pessoa criada com sucesso"},
        400: {"description": "Dados inválidos ou pessoa já existe"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
def create_pessoa(
    pessoa_data: PessoaCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Criar uma nova pessoa**
    
    - **nickname**: Nome único do usuário (obrigatório)
    - **email**: Email válido (obrigatório)
    - **tipo**: Tipo de usuário - 'usuario' ou 'educador' (obrigatório)
    """
    result = controller.create_pessoa(pessoa_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/", 
    response_model=Dict[str, Any],
    summary="Listar pessoas",
    description="Busca todas as pessoas com filtros opcionais. Requer autenticação.",
    responses={
        200: {"description": "Lista de pessoas retornada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)
def get_all_pessoas(
    limit: Optional[int] = Query(None, description="Limite de resultados a retornar", ge=1, le=100),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de usuário", enum=["usuario", "educador"]),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar todas as pessoas**
    
    Parâmetros de filtro opcionais:
    - **limit**: Limita o número de resultados (1-100)
    - **tipo**: Filtra por tipo de usuário ('usuario' ou 'educador')
    """
    result = controller.get_all_pessoas(limit=limit, tipo=tipo)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 500),
            detail=result["error"]
        )
    
    return result

@router.get(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Buscar pessoa por nickname",
    description="Busca uma pessoa específica pelo nickname. Requer autenticação.",
    responses={
        200: {"description": "Pessoa encontrada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Pessoa não encontrada"}
    }
)
def get_pessoa_by_nickname(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Buscar pessoa por nickname**
    
    - **nickname**: Nome único do usuário a ser buscado
    """
    result = controller.get_pessoa_by_nickname(nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 404),
            detail=result["error"]
        )
    
    return result

@router.put(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Atualizar pessoa",
    description="Atualiza os dados de uma pessoa existente. Requer autenticação.",
    responses={
        200: {"description": "Pessoa atualizada com sucesso"},
        400: {"description": "Dados inválidos ou nenhum campo para atualizar"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Pessoa não encontrada"}
    }
)
def update_pessoa(
    nickname: str, 
    update_data: PessoaUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Atualizar dados de uma pessoa**
    
    - **nickname**: Nome único do usuário a ser atualizado
    - Campos opcionais para atualização:
      - **email**: Novo email válido
      - **tipo**: Novo tipo ('usuario' ou 'educador')
    """
    result = controller.update_pessoa(nickname, update_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result

@router.delete(
    "/{nickname}", 
    response_model=Dict[str, Any],
    summary="Deletar pessoa",
    description="Remove uma pessoa do sistema. Requer autenticação.",
    responses={
        200: {"description": "Pessoa deletada com sucesso"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        404: {"description": "Pessoa não encontrada"}
    }
)
def delete_pessoa(
    nickname: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    **Deletar uma pessoa**
    
    - **nickname**: Nome único do usuário a ser deletado
    
    ⚠️ **Atenção**: Esta operação é irreversível!
    """
    result = controller.delete_pessoa(nickname)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"]
        )
    
    return result
