from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    app: str
    mode: Literal["demo"] = "demo"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Detection(BaseModel):
    id: str
    mission_id: str
    class_name: str
    confidence: float = Field(ge=0, le=1)
    verification_status: Literal["verified", "review", "rejected"]
    shadow_ratio: Optional[float] = Field(default=None, ge=0, le=1)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    depth_m: Optional[float] = Field(default=None, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DetectionList(BaseModel):
    items: list[Detection]
    count: int

class QueueRequest(BaseModel):
    detection_id: str = Field(min_length=1)
    priority: Literal["low", "normal", "high"] = "normal"
    notes: str = Field(default="", max_length=500)

class CleanupTask(BaseModel):
    task_id: str
    detection_id: str
    status: Literal["queued"] = "queued"
    priority: Literal["low", "normal", "high"] = "normal"
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DashboardSummary(BaseModel):
    frames_processed: int
    detections_total: int
    false_positives_rejected: int
    inference_ms: float
    cleanup_queue_size: int
    mode: Literal["demo"] = "demo"

class Telemetry(BaseModel):
    mission_id: str
    model_name: str
    mode: Literal["demo"] = "demo"
    connectivity: Literal["online", "offline_queue"] = "offline_queue"
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    note: str = "Sample telemetry; not connected to a live edge device."
