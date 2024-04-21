from pydantic import BaseModel, model_validator
from datetime import datetime, timedelta, date
from fastapi import HTTPException

class WeatherInputModel(BaseModel):
    city: str = ...
    date_from: date | None = None
    date_to: date | None = None

    @model_validator(mode="after")
    def check_datetime(self):
        if self.date_from is None and self.date_to is not None or \
            self.date_from is not None and self.date_to is None:
                raise ValueError("Both date_from and date_to should be stated or neither of them")
        if self.date_from is None and self.date_to is None:
            self.date_from = date.today() - timedelta(days=1)
            self.date_to = date.today()
        if self.date_from > self.date_to:
            raise ValueError("date_to must be more then date_from")
