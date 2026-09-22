from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.activities_endpoint import router as activity_router
from app.api.routes.time_sessions_endpoint import router as session_router
from app.api.routes.stats_endpoint import router as stats_router
from app.api.routes.auth_endpoint import router as auth_router
from app.db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan, title="Time Tracker API")

app.include_router(activity_router)
app.include_router(session_router)
app.include_router(stats_router)
app.include_router(auth_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = [
        {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": errors},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}
