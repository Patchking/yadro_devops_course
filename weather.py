import json
import httpx
import logging
import pydantic
import traceback
from models import WeatherInputModel
from errors import UnexpetedAPIAnswerException
# from math import round

class RequestWeather():
    def __init__(self, token: str):
        self.token = token

    async def get_weather_raw(self, model: WeatherInputModel) -> dict | str:
        try:
            out = None
            async with httpx.AsyncClient() as client:
                url_to_request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{model.city}/{model.date_from}/{model.date_to}?key={self.token}&unitGroup=metric&include=hours&elements=datetime,temp"
                ans = await client.get(url_to_request)
            decoded_answer = ans.content.decode()
            out: str = json.loads(decoded_answer)
        except json.JSONDecodeError as e:
            if isinstance(out, str) and out.startswith("You have exceeded the maximum number of daily result records for your account."):
                logging.error("Access key expired. Please change key!")
                raise UnexpetedAPIAnswerException("Access key expired. Please change key!")
            else:
                logging.error("Not a json returned")
                logging.error(decoded_answer)
                raise UnexpetedAPIAnswerException(f"Not a json returned: \n{decoded_answer}")
        except Exception as e:
            logging.error("Whoops. Something went wrong while requesting weather information.")
            logging.error(traceback.print_exc())
            raise UnexpetedAPIAnswerException()
        return out
        
    async def get_weather_json(self, model: WeatherInputModel) -> dict:
        ans = await self.get_weather_raw(model)
        try:
            temperatures = sorted(
            [
                a["temp"] for b in ans["days"]
                if "hours" in b
                for a in b["hours"]
            ] + 24 * [
                a["temp"] for a in ans["days"]
                if "hours" not in a
                ]
            )
            min_temperature = temperatures[0]
            max_temperature = temperatures[-1]
            arithmetic_temperature = round(sum(temperatures) / len(temperatures), 2)
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
            logging.error("Got unprocessable answer from weather api")
            raise UnexpetedAPIAnswerException("Got unprocessable answer from weather api")
