from contextlib import asynccontextmanager
import datetime
import logging
from typing import List
from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware
from app.routers.general import router as general_router
from app.routers.users import router as user_router
from app.routers.weathers import router as weather_router
from app.db.mongo import MongoDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app.service.raspberrypi.service import RaspberryPiService
from app.service.scheduler.service import SchedulerService

logger = logging.getLogger("apscheduler")
logging.basicConfig(level=logging.INFO)


async def make_read(reader: str, app: FastAPI, job_id: str):
    logger.info(f"Executing job for {reader} with job_id: {job_id}")
    logger.info(f"Reading weather data for: {reader}")
    # call make read function from scheduler service

    app.scheduler_service.make_read(reader)

    await schedule_next_job(reader, app, job_id)


async def schedule_next_job(reader: str, app: FastAPI, job_id: str):
    logger.info(f"Scheduling next job for {reader}...")

    next_schedule_time = datetime.datetime.now()

    trigger = CronTrigger(
        hour=next_schedule_time.hour,
        minute=next_schedule_time.minute,
        second=next_schedule_time.second,
    )

    app.scheduler.remove_job(job_id)

    app.scheduler.add_job(
        func=make_read,
        args=(reader, app, job_id),
        trigger=trigger,
        id=job_id,
        replace_existing=True,
    )
    logger.info(
        f"Job {job_id} scheduled again at {next_schedule_time.hour}:{next_schedule_time.minute}"
    )


async def refresh_schedules(app: FastAPI):
    logger.info("Refreshing schedules...")

    schedules = await app.scheduler_service.get_schedules()
    if not schedules:
        logger.info("No tasks")
        return

    current_job_ids = {
        f"{reader}_{time.hour}_{time.minute}_{time.second}"
        for time, reader in schedules.items()
    }

    for job in app.scheduler.get_jobs():
        if job.id == "refresh_schedules":
            continue
        if job.id not in current_job_ids:
            app.scheduler.remove_job(job.id)
            logger.info(f"Removed outdated job {job.id}")

    for time, reader in schedules.items():
        job_id = f"{reader}_{time.hour}_{time.minute}_{time.second}"
        try:
            trigger = CronTrigger(
                hour=time.hour,
                minute=time.minute,
                second=time.second,
                timezone="Europe/Warsaw",
            )
            logger.info(f"Adding/updating job {job_id}")

            app.scheduler.add_job(
                func=make_read,
                args=(reader, app, job_id),
                trigger=trigger,
                id=job_id,
                replace_existing=True,
            )
            job = app.scheduler.get_job(job_id)
            logger.info(f"Scheduled job {job_id}. Next run: {job.next_run_time}")
        except Exception as e:
            logger.error(f"Error scheduling job {job_id}: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo = MongoDB()
    app.database = app.mongo.db

    app.scheduler = AsyncIOScheduler(timezone="UTC")
    app.scheduler.start()
    logger.info("Scheduler started.")

    app.raspberry_pi_service = RaspberryPiService()
    app.scheduler_service = SchedulerService(
        db=app.mongo, raspberry=app.raspberry_pi_service
    )

    await refresh_schedules(app)

    app.scheduler.add_job(
        refresh_schedules,
        trigger=IntervalTrigger(seconds=30),
        args=[app],
        id="refresh_schedules",
        replace_existing=True,
    )

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

    app.include_router(general_router, prefix="/api/v1")
    app.include_router(user_router, prefix="/api/v1")
    app.include_router(weather_router, prefix="/api/v1")
    return app


app = create_app()


@app.get("/jobs", response_model=List[dict])
async def list_jobs():
    jobs = app.scheduler.get_jobs()
    return [
        {
            "id": job.id,
            "trigger": str(job.trigger),
            "next_run_time": (
                job.next_run_time.isoformat() if job.next_run_time else None
            ),
        }
        for job in jobs
    ]
