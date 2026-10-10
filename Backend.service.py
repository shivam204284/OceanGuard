from uuid import uuid4
from .schemas import CleanupTask, Detection, QueueRequest
from .inference import run_demo_inference

SAMPLE_DETECTIONS = [
    Detection(id="det-017", mission_id="MAV-01", class_name="ghost_net",
              confidence=0.94, verification_status="verified", shadow_ratio=0.81,
              latitude=11.62481, longitude=79.76834, depth_m=18.4),
    Detection(id="det-018", mission_id="MAV-01", class_name="pipe",
              confidence=0.87, verification_status="review", shadow_ratio=0.62,
              latitude=11.62512, longitude=79.76901, depth_m=17.9),
]
_cleanup_queue: list[CleanupTask] = []

def list_detections():
    return list(SAMPLE_DETECTIONS)

def get_detection(detection_id: str):
    return next((d for d in SAMPLE_DETECTIONS if d.id == detection_id), None)

def enqueue_cleanup(request: QueueRequest):
    if get_detection(request.detection_id) is None:
        raise ValueError("Detection not found")
    task = CleanupTask(task_id=f"task-{uuid4().hex[:8]}",
                       detection_id=request.detection_id,
                       priority=request.priority, notes=request.notes)
    _cleanup_queue.append(task)
    return task

def list_cleanup_tasks():
    return list(_cleanup_queue)

def clear_demo_state():
    _cleanup_queue.clear()

def run_inference(filename: str):
    return run_demo_inference(filename)
