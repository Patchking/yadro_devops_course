import os
import logging
import bestconfig

# Ручные настройки
DEBUG_MODE = False


# Автоматическая установка
config = bestconfig.Config()
logger = logging.Logger("base_logger")

# Настройка PYTHONPATH
if "PYTHONPATH" not in os.environ:
    os.environ["PYTHONPATH"] = ""
if os.getcwd() not in os.environ["PYTHONPATH"].split(":"):
    os.environ["PYTHONPATH"] += f":{os.getcwd()}"

FASTAPI_PORT = config.get("PORT", default_value=8000)
WEATHER_TOKEN = config.get("API_KEY", default_value=None)

# Установка уровня дебага
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)


