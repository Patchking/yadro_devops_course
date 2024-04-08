import logging
import uvicorn
import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    port = app.config.get("PORT", default_value=8000)
    wsgi_server = uvicorn.run(
        app="app:app",
        host="127.0.0.1",
        port=app.config.get("PORT")
    )