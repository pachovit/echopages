import logging
import os
from datetime import datetime
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import echopages.bootstrap as bootstrap
import echopages.config
from echopages.api import endpoints as api_endpoints

logger = logging.getLogger(__name__)

app = FastAPI(title="EchoPages", description="Read, Repeat, Retain.")

# Include the API routes
app.include_router(api_endpoints.api_router)

# Serve the static files (React frontend)
app.mount(
    "/static", StaticFiles(directory="echopages/frontend/build/static"), name="static"
)


# Serve the React app's entry point (index.html)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str) -> Any:
    index_file = os.path.join("echopages/frontend/build", "index.html")
    if not os.path.isfile(index_file):
        return {"error": "React frontend not built or incorrect path provided"}

    return FileResponse(index_file)


def configure_logging() -> None:
    """Configure the logger to log info messages."""
    log_level = logging.getLevelName(echopages.config.get_config().log_level)
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def start_scheduler() -> None:
    """Start the scheduler that will send daily digest emails."""
    config = echopages.config.get_config()
    logger.info(
        f"Starting Scheduler at {datetime.now()}, " f"{config.daily_time_of_digest}"
    )
    scheduler = bootstrap.get_scheduler()
    scheduler.start()


def main() -> None:
    """Main function that configures the logging and starts the API server."""
    configure_logging()
    config = echopages.config.get_config()
    start_scheduler()
    uvicorn.run(app, host=config.api_host, port=config.api_port)


if __name__ == "__main__":
    main()
