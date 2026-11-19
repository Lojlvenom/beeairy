from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bee import Bee, BeeType
from app.schemas.bee import BeeCreate, BeeUpdate


def get_bee(db: Session, bee_id: int) -> Bee | None:
    return db.get(Bee, bee_id)


def get_bee_by_scientific_name(db: Session, scientific_name: str) -> Bee | None:
    return db.scalar(select(Bee).where(Bee.scientific_name == scientific_name))


def list_bees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    bee_type: BeeType | None = None,
    search: str | None = None,
) -> list[Bee]:
    stmt = select(Bee)
    if bee_type is not None:
        stmt = stmt.where(Bee.bee_type == bee_type)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(Bee.common_name.ilike(pattern) | Bee.scientific_name.ilike(pattern))
    stmt = stmt.order_by(Bee.id).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create_bee(db: Session, data: BeeCreate) -> Bee:
    bee = Bee(**data.model_dump())
    db.add(bee)
    db.commit()
    db.refresh(bee)
    return bee


def update_bee(db: Session, bee: Bee, data: BeeUpdate) -> Bee:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(bee, field, value)
    db.commit()
    db.refresh(bee)
    return bee


def delete_bee(db: Session, bee: Bee) -> None:
    db.delete(bee)
    db.commit()
