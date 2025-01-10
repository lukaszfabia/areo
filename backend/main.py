from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db

app = FastAPI()


@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    return {"message": "Database connected!"}
