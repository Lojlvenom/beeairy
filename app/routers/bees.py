from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.crud import bee as crud
from app.database import get_db
from app.models.bee import Bee, BeeType
from app.schemas.bee import BeeCreate, BeeRead, BeeUpdate

router = APIRouter(prefix="/bees", tags=["bees"])


def get_bee_or_404(bee_id: int, db: Session = Depends(get_db)) -> Bee:
    bee = crud.get_bee(db, bee_id)
    if bee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Abelha não encontrada")
    return bee


def ensure_unique_scientific_name(db: Session, scientific_name: str, current_id: int | None = None) -> None:
    existing = crud.get_bee_by_scientific_name(db, scientific_name)
    if existing is not None and existing.id != current_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma abelha com o nome científico '{scientific_name}'",
        )


@router.get("", response_model=list[BeeRead])
def list_bees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    bee_type: BeeType | None = None,
    search: str | None = Query(None, description="Busca por nome popular ou científico"),
    db: Session = Depends(get_db),
):
    return crud.list_bees(db, skip=skip, limit=limit, bee_type=bee_type, search=search)


@router.post("", response_model=BeeRead, status_code=status.HTTP_201_CREATED)
def create_bee(data: BeeCreate, db: Session = Depends(get_db)):
    ensure_unique_scientific_name(db, data.scientific_name)
    return crud.create_bee(db, data)


@router.get("/{bee_id}", response_model=BeeRead)
def get_bee(bee: Bee = Depends(get_bee_or_404)):
    return bee


@router.patch("/{bee_id}", response_model=BeeRead)
def update_bee(data: BeeUpdate, bee: Bee = Depends(get_bee_or_404), db: Session = Depends(get_db)):
    if data.scientific_name is not None:
        ensure_unique_scientific_name(db, data.scientific_name, current_id=bee.id)
    return crud.update_bee(db, bee, data)


@router.delete("/{bee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bee(bee: Bee = Depends(get_bee_or_404), db: Session = Depends(get_db)):
    crud.delete_bee(db, bee)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
