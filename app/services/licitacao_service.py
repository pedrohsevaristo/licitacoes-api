from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.licitacao import Licitacao
from app.schemas.licitacao import LicitacaoCreate, LicitacaoUpdate


def listar_licitacoes(
    db: Session,
    cidade: str | None = None,
    modalidade: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple[list[Licitacao], int]:

    statement = select(Licitacao)
    count_statement = select(func.count()).select_from(Licitacao)

    if cidade:
        cidade_normalizada = cidade.strip().lower()

        filtro_cidade = func.lower(
            Licitacao.cidade
        ).contains(cidade_normalizada)

        statement = statement.where(filtro_cidade)
        count_statement = count_statement.where(filtro_cidade)

    if modalidade:
        modalidade_normalizada = modalidade.strip().lower()

        filtro_modalidade = func.lower(
            Licitacao.modalidade
        ).contains(modalidade_normalizada)

        statement = statement.where(filtro_modalidade)
        count_statement = count_statement.where(filtro_modalidade)

    statement = (
        statement
        .order_by(Licitacao.id)
        .limit(limit)
        .offset(offset)
    )

    items = list(
        db.scalars(statement).all()
    )

    total = db.scalar(count_statement) or 0

    return items, total

def buscar_licitacao(db: Session, id: int) -> Licitacao | None:
    return db.get(Licitacao, id)


def criar_licitacao(
    db: Session,
    dados: LicitacaoCreate,
) -> Licitacao:
    licitacao = Licitacao(
        **dados.model_dump()
    )

    db.add(licitacao)
    db.commit()
    db.refresh(licitacao)

    return licitacao


def atualizar_licitacao(
    db: Session,
    id: int,
    dados: LicitacaoUpdate,
) -> Licitacao | None:
    licitacao = db.get(Licitacao, id)

    if licitacao is None:
        return None

    for campo, valor in dados.model_dump().items():
        setattr(licitacao, campo, valor)

    db.commit()
    db.refresh(licitacao)

    return licitacao


def deletar_licitacao(
    db: Session,
    id: int,
) -> bool:
    licitacao = db.get(Licitacao, id)

    if licitacao is None:
        return False

    db.delete(licitacao)
    db.commit()

    return True