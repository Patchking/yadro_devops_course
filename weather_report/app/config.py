import os
import sys
import logging
import bestconfig

# Ручные настройки
DEBUG_MODE = False


# Автоматическая установка
config = bestconfig.Config()
logger = logging.Logger("base_logger")

# Настройка PYTHONPATH

sys.path.append(os.getcwd())

FASTAPI_PORT = config.get("PORT", default_value=8000)
WEATHER_TOKEN = config.get("API_KEY", default_value=None)

# Установка уровня дебага
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)


