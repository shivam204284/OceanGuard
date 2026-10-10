import os
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .schemas import CleanupTask, DashboardSummary, DetectionList, HealthResponse, QueueRequest, Telemetry
from . import service
from .inference import ALLOWED_IMAGE_SUFFIXES

APP_NAME = os.getenv("APP_NAME", "Mavericks Marine Debris AI API")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

app = FastAPI(title=APP_NAME, version="0.1.0",
    description="Demo API for marine-debris dashboard. Results and telemetry are sample data.")
origins = [x.strip() for x in os.getenv(
    "CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

@app.get("/", tags=["system"])
def root():
    return {"name": APP_NAME, "status": "ok", "mode": "demo",
            "docs": "/docs", "warning": "No trained sonar model is connected."}

@app.get("/health", response_model=HealthResponse, tags=["system"])
def health():
    return HealthResponse(app=APP_NAME)

@app.get("/api/v1/dashboard/summary", response_model=DashboardSummary, tags=["dashboard"])
def dashboard_summary():
    return DashboardSummary(frames_processed=1284, detections_total=len(service.list_detections()),
        false_positives_rejected=31, inference_ms=38.0,
        cleanup_queue_size=len(service.list_cleanup_tasks()))

@app.get("/api/v1/detections", response_model=DetectionList, tags=["detections"])
def detections():
    items = service.list_detections()
    return DetectionList(items=items, count=len(items))

@app.get("/api/v1/detections/{detection_id}", tags=["detections"])
def detection_detail(detection_id: str):
    item = service.get_detection(detection_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return item

@app.post("/api/v1/inference/demo", tags=["inference"])
async def infer_demo(file: Annotated[UploadFile, File(description="Sonar frame image")]):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_IMAGE_SUFFIXES:
        raise HTTPException(status_code=415, detail="Unsupported image extension")
    contents = await file.read(MAX_UPLOAD_BYTES + 1)
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"File exceeds {MAX_UPLOAD_MB} MB limit")
    # This scaffold intentionally does not inspect image pixels or call an ML model.
    return service.run_inference(file.filename or "uploaded-image")

@app.get("/api/v1/cleanup/tasks", response_model=list[CleanupTask], tags=["cleanup"])
def cleanup_tasks():
    return service.list_cleanup_tasks()

@app.post("/api/v1/cleanup/tasks", response_model=CleanupTask, status_code=201, tags=["cleanup"])
def create_cleanup_task(request: QueueRequest):
    try:
        return service.enqueue_cleanup(request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get("/api/v1/telemetry", response_model=Telemetry, tags=["telemetry"])
def telemetry():
    return Telemetry(mission_id="MAV-01", model_name="demo-placeholder")

@app.get("/api/v1/export/targets.json", tags=["export"])
def export_targets():
    payload = {"mode": "demo", "mission_id": "MAV-01",
        "warning": "Sample coordinates only; not for navigation or dispatch.",
        "targets": [item.model_dump(mode="json") for item in service.list_detections()]}
    return JSONResponse(content=payload, headers={
        "Content-Disposition": 'attachment; filename="mavericks_targets.json"'})
