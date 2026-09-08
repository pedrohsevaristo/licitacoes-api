from typing import Annotated, TypeAlias

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.licitacao import (
    LicitacaoCreate,
    LicitacaoListResponse,
    LicitacaoResponse,
    LicitacaoUpdate,
)
from app.services import licitacao_service


router = APIRouter(
    prefix="/licitacoes",
    tags=["Licitações"],
)

DatabaseSession: TypeAlias = Annotated[Session, Depends(get_db)]


@router.get(
    "/",
    response_model=LicitacaoListResponse,
    summary="Listar licitações",
)
def listar_licitacoes(
    db: DatabaseSession,
    cidade: str | None = Query(
        default=None,
        min_length=2,
        max_length=100,
        description="Filtrar por cidade",
    ),
    modalidade: str | None = Query(
        default=None,
        min_length=2,
        max_length=50,
        description="Filtrar por modalidade",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Quantidade máxima de registros retornados",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Quantidade de registros a ignorar",
    ),
):
    items, total = licitacao_service.listar_licitacoes(
        db=db,
        cidade=cidade,
        modalidade=modalidade,
        limit=limit,
        offset=offset,
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get(
    "/{id}",
    response_model=LicitacaoResponse,
    summary="Buscar licitação por ID",
    responses={
        404: {"description": "Licitação não encontrada"},
    },
)
def buscar_licitacao(id: int, db: DatabaseSession):
    licitacao = licitacao_service.buscar_licitacao(db, id)

    if licitacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )

    return licitacao


@router.post(
    "/",
    response_model=LicitacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar licitação",
)
def criar_licitacao(
    licitacao: LicitacaoCreate,
    db: DatabaseSession,
):
    return licitacao_service.criar_licitacao(
        db,
        licitacao,
    )


@router.put(
    "/{id}",
    response_model=LicitacaoResponse,
    summary="Atualizar licitação",
    responses={
        404: {"description": "Licitação não encontrada"},
    },
)
def atualizar_licitacao(
    id: int,
    dados: LicitacaoUpdate,
    db: DatabaseSession,
):
    licitacao = licitacao_service.atualizar_licitacao(
        db,
        id,
        dados,
    )

    if licitacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )

    return licitacao


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir licitação",
    responses={
        404: {"description": "Licitação não encontrada"},
    },
)
def deletar_licitacao(
    id: int,
    db: DatabaseSession,
):
    deletada = licitacao_service.deletar_licitacao(
        db,
        id,
    )

    if not deletada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )