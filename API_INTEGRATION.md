# Connecting the dashboard to the API

`index.html` remains the supplied standalone simulation and currently uses hard-coded demo detections. The following functions illustrate how to fetch API data from a page served at `http://localhost:5500`.

```js
const API_BASE = "http://127.0.0.1:8000";

async function loadSummary() {
  const response = await fetch(`${API_BASE}/api/v1/dashboard/summary`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

async function loadDetections() {
  const response = await fetch(`${API_BASE}/api/v1/detections`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

async function queueCleanup(detectionId) {
  const response = await fetch(`${API_BASE}/api/v1/cleanup/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      detection_id: detectionId,
      priority: "normal",
      notes: "Queued from dashboard"
    })
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}
```

Keep the UI clearly labelled as demo mode until a validated model and live telemetry are connected.
