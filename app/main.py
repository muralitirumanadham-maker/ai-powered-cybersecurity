from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from app.config import settings
from app.database import init_db
from app.routes import health, detect, incidents
from app.services.detector import load_models

app = FastAPI(
    title=settings.app_name,
    description="ML threat detection + anomaly scoring + LangGraph investigation agent",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(detect.router)
app.include_router(incidents.router)


@app.on_event("startup")
def startup():
    init_db()
    load_models()


@app.get("/demo.csv", include_in_schema=False)
def demo_csv():
    path = Path("data/demo_network_traffic.csv")
    if not path.exists():
        return Response(status_code=404)
    return Response(path.read_bytes(), media_type="text/csv", headers={"Content-Disposition": "inline; filename=demo_network_traffic.csv"})


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(Path("frontend/index.html"))
