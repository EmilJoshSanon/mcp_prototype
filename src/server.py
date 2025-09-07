from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests as rq
from pydantic import BaseModel

app = FastAPI(title="GetTodaysWeatherrServer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your Open WebUI URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Weather(BaseModel):
    temperature: str
    rain: str
    precipitation_probability: str
    cloud_cover: str

class WeatherDay(BaseModel):
    morning: Weather
    afternoon: Weather

@app.get("/get_the_weather_forecast_for_today", operation_id="get_the_weather_forecast_for_today", response_model=WeatherDay)
def get_todays_weather_forecast() -> WeatherDay:
    """Use this tool to get the weather forecast for today"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=55.675872&longitude=12.56882&hourly=temperature_2m,rain,precipitation_probability,cloud_cover&timezone=Europe%2FBerlin&forecast_days=1"
    response = rq.get(url)
    weather = response.json()
    llm_answer = {
        "morning": {
            'temperature': str(weather['hourly']['temperature_2m'][8]) + "C",
            'rain': str(weather['hourly']['rain'][8]) + " mm",
            'precipitation_probability': str(weather['hourly']['precipitation_probability'][8]) + "%",
            'cloud_cover': str(weather['hourly']['cloud_cover'][8]) + "%"
        },
        "afternoon": {
            'temperature': str(weather['hourly']['temperature_2m'][14]) + "C",
            'rain': str(weather['hourly']['rain'][14]) + " mm",
            'precipitation_probability': str(weather['hourly']['precipitation_probability'][14]) + "%",
            'cloud_cover': str(weather['hourly']['cloud_cover'][14]) + "%"
        }
    }
    return WeatherDay(**llm_answer)