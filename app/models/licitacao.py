from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Licitacao(Base):
    __tablename__ = "licitacoes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    cidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    valor_estimado: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    modalidade: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )