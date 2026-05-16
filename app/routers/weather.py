from fastapi import APIRouter, HTTPException
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["weather"])
weather_service = WeatherService()

@router.get("/current")
async def get_current_weather(city: str):
    try:
        return await weather_service.get_current_weather(city)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or API error: {str(e)}")

@router.get("/forecast")
async def get_forecast(city: str, days: int = 5):
    if days < 1 or days > 5:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 5")
    try:
        return await weather_service.get_forecast(city, days)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or API error: {str(e)}")