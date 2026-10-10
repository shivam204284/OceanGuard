# API reference

Start the API and open `/docs` for interactive Swagger documentation.

Base URL: `http://127.0.0.1:8000`

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/dashboard/summary` | Dashboard metrics |
| GET | `/api/v1/detections` | Sample detections |
| GET | `/api/v1/detections/{detection_id}` | One detection |
| POST | `/api/v1/inference/demo` | Image upload; demo response only |
| GET | `/api/v1/cleanup/tasks` | Queued tasks |
| POST | `/api/v1/cleanup/tasks` | Queue a known detection |
| GET | `/api/v1/telemetry` | Sample edge telemetry |
| GET | `/api/v1/export/targets.json` | Export sample target JSON |

## Queue a cleanup task

```bash
curl -X POST http://127.0.0.1:8000/api/v1/cleanup/tasks \
  -H "Content-Type: application/json" \
  -d '{"detection_id":"det-017","priority":"high","notes":"Review sample target"}'
```

## Upload a demo image

```bash
curl -X POST http://127.0.0.1:8000/api/v1/inference/demo -F "file=@sonar-frame.png"
```

Allowed extensions: PNG, JPG/JPEG, WEBP, BMP, TIF/TIFF. The endpoint enforces a file size limit but does not inspect pixels or run a model.
