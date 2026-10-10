from fastapi.testclient import TestClient
from app.main import app
from app import service

client = TestClient(app)

def setup_function():
    service.clear_demo_state()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["mode"] == "demo"

def test_detections():
    r = client.get("/api/v1/detections")
    assert r.status_code == 200
    assert r.json()["count"] == 2

def test_queue_task():
    r = client.post("/api/v1/cleanup/tasks", json={
        "detection_id": "det-017", "priority": "high", "notes": "Review sample"})
    assert r.status_code == 201
    assert r.json()["status"] == "queued"

def test_unknown_detection_returns_404():
    r = client.post("/api/v1/cleanup/tasks", json={"detection_id": "missing"})
    assert r.status_code == 404

def test_export():
    r = client.get("/api/v1/export/targets.json")
    assert r.status_code == 200
    assert len(r.json()["targets"]) == 2

def test_non_image_upload_rejected():
    r = client.post("/api/v1/inference/demo",
                    files={"file": ("notes.txt", b"not an image", "text/plain")})
    assert r.status_code == 415
