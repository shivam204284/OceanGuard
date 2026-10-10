# Mavericks Marine Debris AI

A starter GitHub repository for a side-scan-sonar marine debris workflow. It packages the supplied browser dashboard, a FastAPI backend, API documentation, tests, Docker configuration, and model-integration notes.

> **Prototype limitation:** the dashboard and API use sample/demo data. No trained sonar model is included. The inference endpoint does not run YOLO or analyze image pixels. Coordinates are illustrative and must not be used for navigation or real cleanup dispatch.

## Repository structure

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI endpoints
│   │   ├── schemas.py    # Pydantic request/response models
│   │   ├── service.py    # Demo detections and in-memory queue
│   │   └── inference.py  # Replaceable model adapter
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html        # Supplied dashboard prototype
│   └── API_INTEGRATION.md
├── docs/
├── data/sample/
├── .env.example
└── docker-compose.yml
```

## Run locally

Requires Python 3.10+.

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs  
Health check: http://127.0.0.1:8000/health

### Frontend

Open `frontend/index.html` directly to run the standalone simulation. Or serve it over HTTP from the repository root:

```bash
python -m http.server 5500 --directory frontend
```

Open http://127.0.0.1:5500. The original UI is not yet wired to the API; see `frontend/API_INTEGRATION.md`.

### Tests

From the repository root:

```bash
python -m pip install -r backend/requirements.txt
python -m pytest backend/tests -q
```

### Docker

From the repository root:

```bash
docker compose up --build
```

Backend: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

## API endpoints

- `GET /health`
- `GET /api/v1/dashboard/summary`
- `GET /api/v1/detections`
- `GET /api/v1/detections/{detection_id}`
- `POST /api/v1/inference/demo` — image upload with a demo-only response
- `GET /api/v1/cleanup/tasks`
- `POST /api/v1/cleanup/tasks`
- `GET /api/v1/telemetry`
- `GET /api/v1/export/targets.json`

## Next steps toward a real system

1. Collect and label properly licensed sonar data.
2. Implement and evaluate preprocessing (Lee filtering, CLAHE, nadir/water-column masking).
3. Train and validate a model; report per-class precision/recall and false positives on held-out missions.
4. Implement acoustic-shadow verification as a tested component.
5. Implement slant-to-ground correction using calibrated sonar geometry and synchronized GPS/IMU.
6. Persist detections/tasks in a database instead of process memory.
7. Add authentication, audit logging, monitoring, and deployment hardening.
8. Evaluate edge inference on the actual device before attempting TensorRT/INT8 optimization.

## License

MIT for this repository scaffold. Check dataset and model licenses separately.
