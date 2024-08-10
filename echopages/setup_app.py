import os
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from echopages.backend.api import endpoints as api_endpoints

# TODO: Move this to a config file
FRONTEND_BUILD_DIR = "echopages/frontend/build"


def configure_frontend(app: FastAPI) -> None:
    """Configure serving of static files, favicon and React app."""
    app.mount(
        "/static",
        StaticFiles(directory=f"{FRONTEND_BUILD_DIR}/static"),
        name="static",
    )

    @app.get("/favicon.ico")
    async def favicon() -> FileResponse:
        return FileResponse(f"{FRONTEND_BUILD_DIR}/favicon.ico")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str) -> Any:
        index_file = f"{FRONTEND_BUILD_DIR}/index.html"
        if not os.path.isfile(index_file):
            return {"error": "React frontend not built or incorrect path provided"}
        return FileResponse(index_file)


def configure_backend(app: FastAPI) -> None:
    """Configure routes from API."""
    app.include_router(api_endpoints.api_router)


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI(title="EchoPages", description="Read, Repeat, Retain.")

    configure_backend(app)
    configure_frontend(app)

    return app
