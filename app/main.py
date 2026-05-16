from fastapi import FastAPI
from app.routers import weather

app = FastAPI(
    title="Weather Dashboard",
    description="Weather API with caching (Redis coming soon)",
    version="1.0.0"
)

app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Weather Dashboard API", "status": "running"}