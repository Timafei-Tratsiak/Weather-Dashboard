import httpx
from datetime import datetime
from app.config import settings
from app.models import WeatherResponse, ForecastDay, ForecastResponse
from app.services.cache_service import CacheService


class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.cache = CacheService()

    async def _ensure_cache_connected(self):
        """Убеждается что кэш подключён"""
        if settings.USE_REDIS:
            await self.cache.connect()

    async def get_current_weather(self, city: str) -> WeatherResponse:
        await self._ensure_cache_connected()

        # Пытаемся получить из кэша
        cache_key = f"weather:current:{city.lower()}"
        cached = await self.cache.get(cache_key)

        if cached:
            print(f"Cache hit for {city}")
            return WeatherResponse(**cached)

        print(f"Cache miss for {city}, calling OpenWeather API")

        # Если нет в кэше — идём в API
        async with httpx.AsyncClient() as client:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "en"
            }
            response = await client.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            data = response.json()

            result = WeatherResponse(
                city=data["name"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"]
            )

            # Сохраняем в кэш на 10 минут
            await self.cache.set(cache_key, result.dict(), ttl=600)

            return result

    async def get_forecast(self, city: str, days: int = 5) -> ForecastResponse:
        await self._ensure_cache_connected()

        # Пытаемся получить из кэша
        cache_key = f"weather:forecast:{city.lower()}:{days}"
        cached = await self.cache.get(cache_key)

        if cached:
            print(f"Cache hit for forecast {city}")
            return ForecastResponse(**cached)

        print(f"Cache miss for forecast {city}, calling OpenWeather API")

        async with httpx.AsyncClient() as client:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "en",
                "cnt": days * 8
            }
            response = await client.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()

            # Группируем по дням
            daily_data = {}
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                if date not in daily_data:
                    daily_data[date] = {
                        "temps": [],
                        "descriptions": []
                    }
                daily_data[date]["temps"].append(item["main"]["temp"])
                daily_data[date]["descriptions"].append(item["weather"][0]["description"])

            forecast = []
            for date, values in list(daily_data.items())[:days]:
                forecast.append(ForecastDay(
                    date=date,
                    temp_min=min(values["temps"]),
                    temp_max=max(values["temps"]),
                    description=max(set(values["descriptions"]), key=values["descriptions"].count)
                ))

            result = ForecastResponse(
                city=data["city"]["name"],
                forecast=forecast
            )

            # Сохраняем в кэш на 1 час
            await self.cache.set(cache_key, result.dict(), ttl=3600)

            return result

    async def close_cache(self):
        """Закрывает соединение с кэшем"""
        await self.cache.close()