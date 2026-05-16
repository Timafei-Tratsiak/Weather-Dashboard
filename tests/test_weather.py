import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Проверяет что корневой эндпоинт работает"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@pytest.mark.asyncio
async def test_current_weather_valid_city():
    """Проверяет текущую погоду для существующего города"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/weather/current?city=London")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "temperature" in data
    assert "feels_like" in data
    assert "humidity" in data
    assert "wind_speed" in data
    assert "description" in data
    assert data["city"] == "London"


@pytest.mark.asyncio
async def test_current_weather_invalid_city():
    """Проверяет обработку несуществующего города"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/weather/current?city=ThisCityDoesNotExist12345")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_forecast_valid_city():
    """Проверяет прогноз для существующего города"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/weather/forecast?city=Paris&days=3")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "forecast" in data
    assert len(data["forecast"]) == 3

    # Проверяем структуру каждого дня прогноза
    for day in data["forecast"]:
        assert "date" in day
        assert "temp_min" in day
        assert "temp_max" in day
        assert "description" in day


@pytest.mark.asyncio
async def test_forecast_invalid_days():
    """Проверяет валидацию количества дней (1-5)"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Дней больше 5
        response = await ac.get("/weather/forecast?city=London&days=10")
    assert response.status_code == 400

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Дней меньше 1
        response = await ac.get("/weather/forecast?city=London&days=0")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_forecast_default_days():
    """Проверяет что по умолчанию возвращается 5 дней"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/weather/forecast?city=Tokyo")
    assert response.status_code == 200
    data = response.json()
    assert len(data["forecast"]) == 5


@pytest.mark.asyncio
async def test_city_case_insensitive():
    """Проверяет что город работает независимо от регистра"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response_lower = await ac.get("/weather/current?city=moscow")
        response_upper = await ac.get("/weather/current?city=MOSCOW")
        response_normal = await ac.get("/weather/current?city=Moscow")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    assert response_normal.status_code == 200

    # Все ответы должны быть для одного города
    assert response_lower.json()["city"] == "Moscow"