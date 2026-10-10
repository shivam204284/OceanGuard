# Model integration checklist

No model weights are shipped and no accuracy claims are made by this repository.

1. Define a documented class taxonomy (e.g. ghost net, rope, tire, metal debris, pipe, unknown).
2. Split data by mission/site, not only by random frame, to reduce spatial leakage.
3. Build reproducible preprocessing and version its configuration.
4. Train and benchmark candidate models. Track per-class precision/recall, mAP where appropriate, false positives per kilometre/frame, latency, and memory.
5. Return typed bounding boxes, confidence, model version, and inference timing.
6. Implement acoustic-shadow verification as a separately tested component.
7. Add slant-range correction only with known sonar geometry and synchronized navigation data.
8. Test on held-out missions and difficult conditions such as sediment, vegetation, rocks, and changing sonar range.
9. Keep model code behind `backend/app/inference.py`; load weights once at startup.
10. Document dataset/model licenses, limitations, and rollback steps.

Consider a durable local database and offline synchronization for edge use. Optimize for Jetson/TensorRT/INT8 only after validating baseline accuracy on target hardware.
