# app/middleware.py

import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)


async def log_requests(request: Request, call_next):
    """Log every request and response time."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={process_time:.2f}ms"
    )
    return response


async def global_exception_handler(request: Request, exc: Exception):
    """Return clean JSON errors instead of raw HTML/tracebacks."""
    logger.error(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


def init_middleware(app: FastAPI):
    """Attach all middleware and exception handlers to app."""
    app.middleware("http")(log_requests)
    app.add_exception_handler(Exception, global_exception_handler)
