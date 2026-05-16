# Weather Dashboard

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-7.x-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-29.x-blue.svg)](https://www.docker.com/)

## Overview

Weather Dashboard is a high-performance async REST API that provides current weather and 5-day forecasts. Built with FastAPI and Redis caching to minimize external API calls.

## Features

- **Current Weather** — real-time weather data for any city
- **5-day Forecast** — daily min/max temperatures and conditions
- **Smart Caching** — Redis with configurable TTL (10 min for weather, 1 hour for forecasts)
- **Docker Ready** — one-command deployment with Docker Compose
- **Async Architecture** — non-blocking I/O for high concurrency
- **Test Coverage** — 9 pytest tests with edge cases

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Async REST API framework |
| Redis | In-memory caching layer |
| Docker | Containerization & orchestration |
| OpenWeather API | External weather data provider |
| HTTPX | Async HTTP client |
| Pytest | Testing framework |

## Quick Start

### Prerequisites

- Python 3.14+
- Docker Desktop (for Redis)
- OpenWeather API key ([get it here](https://home.openweathermap.org/api_keys))

### Local Development (without Docker)

```bash
# Clone repository
git clone git@github.com:Timafei-Tratsiak/Weather-Dashboard.git
cd Weather-Dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your OpenWeather API key

# Run server
uvicorn app.main:app --reload
```
### With Docker Compose

```bash
# Start both FastAPI and Redis
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop containers
docker-compose down
```
### Running Tests

```bash
pytest tests/ -v
```
### API Documentation

Once running, visit http://localhost:8000/docs for interactive Swagger UI.

### Endpoints

#### Get Current Weather

```http
GET /weather/current?city={city}
```
#### Response:

```json
{
  "city": "London",
  "temperature": 17.14,
  "feels_like": 16.55,
  "humidity": 63,
  "wind_speed": 3.3,
  "description": "few clouds"
}
```
#### Get 5-day Forecast

```http
GET /weather/forecast?city={city}&days={days}
```
#### Parameters:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| city | Yes | — | City name |
| days | No | 5 | Number of days (1-5) |

#### Response:

```json
{
  "city": "London",
  "forecast": [
    {
      "date": "2026-05-16",
      "temp_min": 12.5,
      "temp_max": 18.3,
      "description": "light rain"
    }
  ]
}
```
### Project Structure

```text
Weather-Dashboard/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings & env variables
│   ├── models.py            # Pydantic schemas
│   ├── services/
│   │   ├── weather_service.py
│   │   └── cache_service.py
│   └── routers/
│       └── weather.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```
### Configuration

#### Create .env file based on .env.example:

```env
OPENWEATHER_API_KEY=your_api_key_here
USE_REDIS=true
REDIS_URL=redis://localhost:6379
```
### Caching Strategy

| Data Type | TTL | Cache Key |
|-----------|-----|-----------|
| Current Weather | 10 minutes | `weather:current:{city}` |
| Forecast | 1 hour | `weather:forecast:{city}:{days}` |

### Test Results

```text
====================== 9 passed in 2.16s ======================
```
