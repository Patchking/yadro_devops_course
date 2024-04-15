
import httpx
import json
import traceback

import config
from models.weather import WeatherInputModel
from exceptions.weather import UnexpetedAPIAnswerException
from config import logger


async def get(model: WeatherInputModel) -> dict:
    try:
        out = None
        async with httpx.AsyncClient() as client:
            url_to_request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{model.city}/{model.date_from}/{model.date_to}?key={config.WEATHER_TOKEN}&unitGroup=metric&include=hours&elements=datetime,temp"
            ans = await client.get(url_to_request)
        decoded_answer = ans.content.decode()
        out: str = json.loads(decoded_answer)
    except json.JSONDecodeError as e:
        if isinstance(out, str) and out.startswith("You have exceeded the maximum number of daily result records for your account."):
            logger.error("Access key expired. Please change key!")
            raise UnexpetedAPIAnswerException("Access key expired. Please change key!")
        else:
            logger.error("Not a json returned")
            logger.error(decoded_answer)
            raise UnexpetedAPIAnswerException(f"Not a json returned: \n{decoded_answer}")
    except Exception as e:
        logger.error("Whoops. Something went wrong while requesting weather information.")
        logger.error(traceback.print_exc())
        raise UnexpetedAPIAnswerException()
    return out