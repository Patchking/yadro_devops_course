import uvicorn
import config

if __name__ == "__main__":
    wsgi_server = uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=config.FASTAPI_PORT,
        reload=config.DEBUG_MODE
    )