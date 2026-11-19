from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra os modelos no metadata)
from app.config import settings
from app.database import Base, engine
from app.routers import bees


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Enquanto não usamos migrations (Alembic), criamos as tabelas na inicialização.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="API para gerenciamento de meliponários e apiários.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(bees.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
