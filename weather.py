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
                url_to_request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{model.city}/{model.date_from}/{model.date_to}?key={self.token}&unitGroup=metric&include=hours&elements=datetime,temp"
                ans = await client.get(url_to_request)
            decoded_answer = ans.content.decode()
            out = json.loads(decoded_answer)
        except httpx.ConnectTimeout as e:
            logging.error("Whoops. Something went wrong while requesting weather information.")
            logging.error(e.args)
            out = {"error": e.args}
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
            temperatures = sorted(a["temp"] for b in ans["days"] for a in b["hours"])
            min_temperature = temperatures[0]
            max_temperature = temperatures[-1]
            arithmetic_temperature = round(sum(temperatures) / len(temperatures), 1)
            median_temperature = temperatures[len(temperatures) // 2]
            return {
                "service": "weather",
                "data": {
                    "temperature_c": {
                        "average": arithmetic_temperature,
                        "median": median_temperature,
                        "min": min_temperature,
                        "max": max_temperature
                    }
                }
            }
        except Exception:
            logging.error("Got unexpected answer from weather api")
            return {
                "message": "Got unexpected answer from weather api"
            }
