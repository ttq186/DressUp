from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.closet.router import router as closet_router
from src.config import app_configs, settings
from src.database import database
from src.product.router import router as product_router
from src.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect DB on start
    await database.connect()

    yield

    # Disconnect DB on shutdown
    await database.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(closet_router)
