import bestconfig
import pydantic
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from weather import RequestWeather
from models import WeatherInputModel
from errors import UnexpetedAPIAnswerException

config = bestconfig.Config()
app = FastAPI()

@app.exception_handler(pydantic.ValidationError)
async def validation_error_exception_handler(request: Request, exc: pydantic.ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "details": "Wrong input"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "details": "Wrong input"
        }
    )

@app.exception_handler(UnexpetedAPIAnswerException)
async def validation_error_exception_handler(request: Request, exc: UnexpetedAPIAnswerException):
    return JSONResponse(
        status_code=403,
        content={
            "details": str(exc)
        }
    )

@app.get("/info")
async def get_info():
    version = config.get("VERSION", default_value="0.1.0")
    return JSONResponse({
        "version": version,
        "service": "weather",
        "author": "Ohaggard"
        })


@app.get("/info/weather")
async def get_weather(model: WeatherInputModel = Depends()):
    weather = RequestWeather(config.get("API_KEY"))
    ans = await weather.get_weather_json(model)
    return JSONResponse(content=ans)
