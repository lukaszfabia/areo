from pydantic import FiniteFloat
from typing import Optional
from app.db.models.model import Model, Field


class Weather(Model):
    __repr_name__ = "weather_data"

    temperature: Optional[FiniteFloat] = Field(
        None, description="Temperature in degrees Celsius"
    )
    humidity: Optional[FiniteFloat] = Field(
        None, description="Relative humidity in percentage"
    )
    pressure: Optional[FiniteFloat] = Field(
        None, description="Atmospheric pressure in hPa"
    )
    altitude: Optional[FiniteFloat] = Field(None, description="Altitude in meters")
    reader: Optional[FiniteFloat] = Field(
        None, description="Name of the user or device reading the data"
    )
