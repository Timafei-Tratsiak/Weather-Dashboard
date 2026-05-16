import json
from typing import Optional, Any
import redis.asyncio as redis
from app.config import settings


class CacheService:
    def __init__(self):
        self.redis = None
        self.enabled = settings.USE_REDIS

    async def connect(self):
        """Подключается к Redis если он включён"""
        if self.enabled and not self.redis:
            try:
                self.redis = await redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
                await self.redis.ping()
                print("Redis connected successfully")
            except Exception as e:
                print(f"Redis connection failed: {e}")
                self.enabled = False
                self.redis = None

    async def get(self, key: str) -> Optional[Any]:
        """Получает данные из кэша"""
        if not self.enabled or not self.redis:
            return None

        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 600):
        """Сохраняет в кэш с TTL (по умолчанию 10 минут)"""
        if not self.enabled or not self.redis:
            return

        try:
            await self.redis.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            print(f"Cache set error: {e}")

    async def close(self):
        """Закрывает соединение с Redis"""
        if self.redis:
            await self.redis.close()