from typing import List
from pydantic import BaseModel, FiniteFloat
from datetime import datetime


class Weather(BaseModel):
    date: datetime

    temperature: FiniteFloat
    humidity: FiniteFloat
    pressure: FiniteFloat
    altitude: FiniteFloat

    # user: List[User]
