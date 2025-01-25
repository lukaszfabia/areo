import asyncio
from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.general import router as general_router
from app.routers.users import router as user_router
from app.db.mongo import MongoDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.db.models.model import Time
from app.service.raspberrypi.impl import RaspberryPiServiceImpl
from app.service.scheduler.service import SchedulerService


# TOOD: fix cron trigger


async def load_schedules(app: FastAPI):
    print("Loading schedules...")
    schedules: Dict[Time, str] = await app.scheduler_service.get_schedules()

    for time, reader in schedules.items():
        trigger = CronTrigger(hour=time.hour, minute=time.minute, second=time.second)
        print(f"Weather scheduled on: {time.hour}:{time.minute}:{time.second}")
        app.scheduler.add_job(
            func=lambda: asyncio.create_task(app.scheduler_service.make_read(reader)),
            trigger=trigger,
            id=f"schedule_{reader}",
            replace_existing=True,
        )


async def weather_reading(app: FastAPI):
    await load_schedules(app)

    trigger = IntervalTrigger(hours=1)
    app.scheduler.add_job(
        func=lambda: asyncio.create_task(load_schedules(app)),
        trigger=trigger,
        id="refresh_schedules",
        replace_existing=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo = MongoDB()
    app.database = app.mongo.db

    app.raspberry_pi_service = RaspberryPiServiceImpl()

    app.scheduler_service = SchedulerService(
        db=app.mongo, raspberry=app.raspberry_pi_service
    )

    app.scheduler = AsyncIOScheduler()
    app.scheduler.start()

    await weather_reading(app)

    try:
        yield
    finally:
        app.mongo.close()
        app.scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Official Areo API",
        description="Areo API helps to handle users and weather",
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

    # Dodanie routerów
    app.include_router(general_router, prefix="/api/v1")
    app.include_router(user_router, prefix="/api/v1")
    return app


# Utworzenie instancji aplikacji
app = create_app()
