import uvicorn
import config

if __name__ == "__main__":
    wsgi_server = uvicorn.run(
        app="app:app",
        host="127.0.0.1",
        port=config.FASTAPI_PORT,
        reload=config.DEBUG_MODE
    )