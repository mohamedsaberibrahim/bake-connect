from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from app.settings import settings
from app.router import api_router
from importlib import metadata
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.lifetime import (register_shutdown_event, register_startup_event)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="bakeConnect",
        version="1.0.0", #  metadata.version("bakeConnect")
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds static files.
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Adds landing page for the application.
    app.add_api_route("/", endpoint=lambda: FileResponse('static/index.html'))

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
