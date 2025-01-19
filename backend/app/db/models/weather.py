from pydantic import FiniteFloat
from typing import Optional
from app.db.models.model import Model


class Weather(Model):
    __repr_name__ = "weather_data"

    temperature: Optional[FiniteFloat] = None
    humidity: Optional[FiniteFloat] = None
    pressure: Optional[FiniteFloat] = None
    altitude: Optional[FiniteFloat] = None

    # username
    reader: Optional[str] = None
