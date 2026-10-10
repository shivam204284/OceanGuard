"""Demo inference adapter. Replace this function with a validated model pipeline."""
from pathlib import Path
from typing import Any

ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

def run_demo_inference(filename: str) -> dict[str, Any]:
    """Return synthetic output; this deliberately does not load or run an ML model."""
    return {
        "filename": Path(filename).name,
        "mode": "demo",
        "model_name": "demo-placeholder",
        "message": "Demo only: no trained model was loaded and no image inference was performed.",
        "detections": [{
            "class_name": "ghost_net",
            "confidence": 0.94,
            "verification_status": "review",
            "shadow_ratio": 0.81
        }]
    }
