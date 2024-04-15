FROM python:3.11-alpine

RUN mkdir /app && adduser -D app && chown -R app /app
WORKDIR /app

COPY app/requirements.txt .
RUN python3.11 -m pip install -r requirements.txt

COPY    app .

ENV APP_TMP_DATA=/tmp PYTHONPATH=/app PORT=8000
USER app
EXPOSE 8000
ENTRYPOINT ["python3.11", "main.py"]
