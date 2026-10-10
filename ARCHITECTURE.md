# Architecture

## Intended workflow

1. **Sonar acquisition:** receive side-scan frames with synchronized sensor metadata.
2. **Preprocessing:** validate inputs; optionally apply Lee filtering, CLAHE, and nadir/water-column masks.
3. **Candidate detection:** run a trained object-detection model.
4. **Verification:** assess acoustic-shadow evidence and reject likely false positives using validated logic.
5. **Geolocation:** use calibrated sonar geometry, slant-to-ground correction, and synchronized GPS/IMU to estimate WGS84 coordinates.
6. **Persistence/queue:** save detections and cleanup tasks with provenance.
7. **Dashboard/telemetry:** visualize detections and device status, including offline queue state.

## Current state

The backend is a development scaffold with sample detections and in-memory cleanup tasks. Restarting the API clears the queue. Image uploads return a demo payload; no model analyzes the image. Coordinates are illustrative. No database, MQTT, ROS 2, GPS/IMU device, or trained model is connected.

## Production boundaries

Separate acquisition, preprocessing, inference, verification, geolocation, storage, and API transport. Version model weights and preprocessing settings together. Validate on held-out missions and varied environments. Add authentication, audit logs, data retention rules, and monitoring before exposing the API.
