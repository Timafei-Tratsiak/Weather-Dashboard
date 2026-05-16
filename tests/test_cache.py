import pytest
from httpx import AsyncClient
from app.main import app
from app.services.cache_service import CacheService


@pytest.mark.asyncio
async def test_cache_connection():
    """Проверяет что кэш-сервис может подключиться (если Redis запущен)"""
    cache = CacheService()
    await cache.connect()
    # Не падает — уже хорошо
    await cache.close()


@pytest.mark.asyncio
async def test_cache_set_get():
    """Проверяет базовые операции кэша (требует Redis)"""
    cache = CacheService()
    await cache.connect()

    if cache.enabled and cache.redis:
        test_key = "test:key"
        test_value = {"test": "data", "number": 42}

        await cache.set(test_key, test_value, ttl=60)
        retrieved = await cache.get(test_key)

        assert retrieved == test_value

        await cache.redis.delete(test_key)

    await cache.close()