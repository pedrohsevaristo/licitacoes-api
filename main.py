from fastapi import FastAPI
from app.routers.licitacoes import router as licitacoes_router

app = FastAPI(
    title="Licitações API",
    description="API REST para gerenciamento de licitações públicas",
    version="1.0.0"
)

app.include_router(licitacoes_router)

@app.get("/")
def root():
    return {
        "message": "Licitações API funcionando!",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }