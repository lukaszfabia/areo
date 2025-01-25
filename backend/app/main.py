from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.general import router as general_router
from app.routers.users import router as user_router
from app.db.mongo import MongoDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.service.scheduler.service import SchedulerService


async def load_schedules(app: FastAPI):
    schedules = await app.database.schedules.find().to_list(length=None)
    for schedule in schedules:
        sensor_id = schedule["sensor_id"]
        time_str = schedule["time"]
        hour, minute = map(int, time_str.split(":"))

        trigger = CronTrigger(hour=hour, minute=minute)
        app.scheduler.add_job(
            app.scheduler_service.make_read(), trigger, args=[sensor_id, app]
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo = MongoDB()
    app.database = app.mongo.db

    app.scheduler_service = SchedulerService(app.mongo)

    app.scheduler = AsyncIOScheduler()
    app.scheduler.start()

    await load_schedules(app)

    try:
        yield
    finally:
        app.mongo.close()
        app.scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Official areo api",
        description="Areo API, helps to handle users and weather",
        version="1.0.0",
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
