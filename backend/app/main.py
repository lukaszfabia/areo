from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.general import router as general_router
from app.routers.users import router as user_router
from app.db.connection import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo = MongoDB()
    app.database = app.mongo.db
    try:
        yield
    finally:
        app.mongo.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Official areo api",
        description="Areo API, helps to handle users and weather",
        version="0.0.1",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(general_router, prefix="/api/v1")
    app.include_router(user_router, prefix="/api/v1")
    return app


app = create_app()
