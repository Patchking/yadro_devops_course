import json
import httpx
import logging
import pydantic
from models import WeatherInputModel
# from math import round

class RequestWeather():
    def __init__(self, token: str):
        self.token = token

    async def get_weather_raw(self, model: WeatherInputModel) -> dict | str:
        try:
            async with httpx.AsyncClient() as client:
                ans = await client.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{model.city}/{model.date_from}/{model.date_to}?key={self.token}&unitGroup=metric&include=days&elements=datetime,tempmax,tempmin,temp")
            decoded_answer = ans.content.decode()
            out = json.loads(decoded_answer)
        except httpx.ConnectError as e:
            logging.error("Whoops. Something went wrong while requesting weather information.")
            logging.error(e.args)
            out = {"error": e.args}
        except json.JSONDecodeError as e:
            logging.error("Not a json returned")
            logging.error(decoded_answer)
            out =  decoded_answer
        finally:
            return out
        
    async def get_weather_json(self, model: WeatherInputModel) -> dict:
        ans = await self.get_weather_raw(model)
        try:
            temperatures = [a["temp"] for a in ans["days"]]
            min_temperatures = [a["tempmin"] for a in ans["days"]]
            max_temperatures = [a["tempmax"] for a in ans["days"]]
            return {
                "service": "weather",
                "data": {
                    "temperature_c": {
                        "average": round(sum(temperatures) / len(temperatures), 2),
                        "median": temperatures[len(temperatures) // 2],
                        "min": min(min_temperatures),
                        "max": max(max_temperatures)
                    }
                }
            }
        except Exception:
            logging.error("Got unexpected answer from weather api")
            return {
                "message": "Got unexpected answer from weather api"
            }
