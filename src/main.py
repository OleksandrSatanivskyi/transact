from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers.stock_router import router as stock_router
from src.routers.crypto_router import router as crypto_router
from src.routers.crypto_transaction_router import router as crypto_transaction_router
from src.routers.stock_transaction_router import router as stock_transaction_router

app = FastAPI(
    title="API",
    description="transact",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(stock_router)
app.include_router(crypto_router)
app.include_router(stock_transaction_router)
app.include_router(crypto_transaction_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=settings.API_PORT,
        reload=True
    )

