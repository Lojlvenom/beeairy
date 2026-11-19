from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.bee import BeeType


class BeeBase(BaseModel):
    common_name: str = Field(..., min_length=1, max_length=100, examples=["Jataí"])
    scientific_name: str = Field(
        ..., min_length=1, max_length=150, examples=["Tetragonisca angustula"]
    )
    bee_type: BeeType = Field(..., examples=[BeeType.STINGLESS])
    native: bool = Field(True, description="Espécie nativa do Brasil?")
    description: str | None = Field(None, examples=["Abelha sem ferrão, dócil e muito comum."])


class BeeCreate(BeeBase):
    pass


class BeeUpdate(BaseModel):
    """Todos os campos são opcionais (atualização parcial)."""

    common_name: str | None = Field(None, min_length=1, max_length=100)
    scientific_name: str | None = Field(None, min_length=1, max_length=150)
    bee_type: BeeType | None = None
    native: bool | None = None
    description: str | None = None


class BeeRead(BeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
