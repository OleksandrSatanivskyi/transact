from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=settings.API_PORT,
        reload=True
    )

