from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LicitacaoBase(BaseModel):
    titulo: str = Field(
        min_length=3,
        max_length=200
    )
    cidade: str = Field(
        min_length=2,
        max_length=100
    )
    valor_estimado: Decimal = Field(
        gt=0
    )
    modalidade: str = Field(
        min_length=2,
        max_length=50
    )


class LicitacaoCreate(LicitacaoBase):
    pass


class LicitacaoUpdate(LicitacaoBase):
    pass


class LicitacaoResponse(LicitacaoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class LicitacaoListResponse(BaseModel):
    items: list[LicitacaoResponse]
    total: int
    limit: int
    offset: int