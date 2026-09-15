from fastapi import FastAPI

from app.api.routes.activities_endpoint import router as activity_router
from app.api.routes.time_sessions_endpoint import router as session_router
from app.api.routes.stats_endpoint import router as stats_router



app = FastAPI(title="Time Tracker API")

app.include_router(activity_router)
app.include_router(session_router)
app.include_router(stats_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
