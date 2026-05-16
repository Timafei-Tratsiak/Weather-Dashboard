from pydantic import BaseModel
from typing import List, Optional

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str

class ForecastDay(BaseModel):
    date: str
    temp_min: float
    temp_max: float
    description: str

class ForecastResponse(BaseModel):
    city: str
    forecast: List[ForecastDay]