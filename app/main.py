from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.logging import setup_logging
from app.middlewares import AuthValidationMiddleware
from app.routers import user_router
from app.schemas import AppStatusSchema
from app.scripts import create_mongo_index_user_telegram_id


app = FastAPI(
    title="Logout service",
    description="Service for logout user from system.",
    on_startup=[create_mongo_index_user_telegram_id],
)

app.add_middleware(AuthValidationMiddleware)
app.include_router(user_router)

setup_logging()
Instrumentator().instrument(app).expose(app)


@app.get("/health", tags=["internal"])
async def health() -> AppStatusSchema:
    return AppStatusSchema(status="UP")
