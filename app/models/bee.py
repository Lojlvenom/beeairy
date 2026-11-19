import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BeeType(str, enum.Enum):
    """Grupo da abelha: sem ferrão (meliponíneos) ou Apis (apicultura)."""

    STINGLESS = "stingless"
    APIS = "apis"


class Bee(Base):
    """Espécie de abelha manejada no meliponário/apiário."""

    __tablename__ = "bees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    common_name: Mapped[str] = mapped_column(String(100), index=True)
    scientific_name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    bee_type: Mapped[BeeType] = mapped_column(Enum(BeeType, native_enum=False, length=20))
    native: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
