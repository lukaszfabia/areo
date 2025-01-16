from pydantic import FiniteFloat
from typing import Optional
from model import Model


class Weather(Model):

    temperature: Optional[FiniteFloat] = None
    humidity: Optional[FiniteFloat] = None
    pressure: Optional[FiniteFloat] = None
    altitude: Optional[FiniteFloat] = None

    # username
    reader: Optional[str] = None
