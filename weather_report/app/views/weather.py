import config
from config import logger
from exceptions.weather import UnexpetedAPIAnswerException
from models.weather import WeatherInputModel
import utils.visualcrossing

async def get(model: WeatherInputModel) -> str:
    try:
        raw_weather = await utils.visualcrossing.get(model)
        temperatures = sorted(
        [
            a["temp"] for b in raw_weather["days"]
            if "hours" in b
            for a in b["hours"]
        ] + 24 * [
            a["temp"] for a in raw_weather["days"]
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
    except UnexpetedAPIAnswerException:
        raise
    except Exception:
        logger.error("Got unprocessable answer from weather api")
        raise UnexpetedAPIAnswerException("Got unprocessable answer from weather api")