import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core import redis_helper
from app.handlers import main_handlers as main

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    log.info(f"Pytex started at: {datetime.now()}")
    yield
    await redis_helper.dispose()
    log.info(f"Pytex shutdown at: {datetime.now()}")


main_app = FastAPI(lifespan=lifespan, title="Pytex", root_path="")


@main_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for err in exc.errors():
        loc = ".".join(map(str, err.get("loc", ())))
        log.error(
            "Request validation | field=%s | msg=%s | type=%s",
            loc,
            err.get("msg"),
            err.get("type"),
        )
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


main_app.include_router(main.router)


real_static_path = Path("./static").resolve()


main_app.mount(
    "/",
    StaticFiles(
        directory=str(real_static_path),
        follow_symlink=True,
        check_dir=True,
    ),
    name="static",
)
