import logging
import uvicorn
import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = app.config.get("PORT", default_value=8000)
    wsgi_server = uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=app.config.get("PORT")
    )