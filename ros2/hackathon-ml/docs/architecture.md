# Facial Expression Classification Pipeline (ROS2 + Hugging Face)

## 1. Objective
Build a ROS2 pipeline that consumes a camera image stream, samples at **4 Hz**, performs facial expression classification using **`dima806/facial_emotions_image_detection`** from Hugging Face, transforms predictions into matching emojis, and publishes structured outputs for downstream robotics behaviors.

## 2. Scope
In scope:
- ROS2 image ingestion from a camera topic (`sensor_msgs/msg/Image`)
- Rate-limited frame selection at 4 Hz
- Image preprocessing for model input
- Inference with Hugging Face model
- Publishing expression labels + confidence + timing metadata

Out of scope (initial version):
- Multi-face tracking identities
- Long-term emotion smoothing/fusion across sessions
- Edge accelerator optimization (TensorRT/OpenVINO)

## 3. High-Level Architecture

```text
Camera Driver Node
  -> /peak_cam/W_6340/image_raw (sensor_msgs/Image)

emotion_frame_sampler (ROS2 node)
  Sub: /peak_cam/W_6340/image_raw
  - Keeps latest frame
  - Timer-trigger at 4 Hz
  Pub: /emotion/input_image (sensor_msgs/Image)

emotion_inference_node (ROS2 node)
  Sub: /emotion/input_image
  - Convert ROS Image -> OpenCV/PIL
  - Preprocess to model format
  - Hugging Face inference
  Pub: /emotion/prediction (custom msg or std_msgs/String + metadata topic)

emotion_emoji_mapper (ROS2 node)
  Sub: /emotion/prediction
  - Map top_label to emoji
  - Attach confidence and timestamp metadata
  Pub: /emotion/emoji (custom msg or std_msgs/String)

emotion_overlay_node (optional)
  Sub: /peak_cam/W_6340/image_raw + /emotion/prediction + /emotion/emoji
  - Draw top label/confidence/emoji
  Pub: /emotion/debug_image (sensor_msgs/Image)

consumer nodes
  Sub: /emotion/prediction and /emotion/emoji
  - HRI behavior, UI rendering, logging, analytics, state machines
```

## 4. ROS2 Nodes and Responsibilities

### 4.1 `emotion_frame_sampler`
Purpose: decouple camera frame rate from model inference rate.

Responsibilities:
- Subscribe to `/peak_cam/W_6340/image_raw`
- Cache only latest frame (drop older queued frames)
- Trigger publish every 250 ms (4 Hz)
- Publish frame to `/emotion/input_image`

Design notes:
- Use QoS: `SensorDataQoS` for image subscription
- Use depth 1 queue to avoid backlog
- This node enforces deterministic sampling even if camera is 15/30 FPS

### 4.2 `emotion_inference_node`
Purpose: run ML inference and produce machine-readable expression outputs.

Responsibilities:
- Load model/pipeline at startup:
  - Hugging Face model: `dima806/facial_emotions_image_detection`
- Subscribe to `/emotion/input_image`
- Convert ROS image (`bgr8`/`rgb8`) to model-ready format
- Run forward inference
- Publish top-k predictions and metadata

Recommended topic output:
- `/emotion/prediction` as custom message (`EmotionPrediction.msg`)

Proposed `EmotionPrediction.msg` fields:
- `std_msgs/Header header`
- `string top_label`
- `float32 top_confidence`
- `string[] labels`
- `float32[] confidences`
- `float32 inference_ms`
- `string model_id`

If custom msg creation is not immediately available, publish:
- `/emotion/prediction/json` (`std_msgs/String`, JSON payload)

### 4.3 `emotion_emoji_mapper`
Purpose: convert model label outputs into deterministic emoji representations.

Responsibilities:
- Subscribe to `/emotion/prediction`
- Map `top_label` to emoji using configurable dictionary
- Publish mapped output to `/emotion/emoji`

Recommended topic output:
- `/emotion/emoji` as custom message (`EmotionEmoji.msg`)

Proposed `EmotionEmoji.msg` fields:
- `std_msgs/Header header`
- `string top_label`
- `string emoji`
- `float32 top_confidence`
- `string model_id`

Reference mapping (initial):
- `happy` -> `😊`
- `sad` -> `😢`
- `angry` -> `😠`
- `fear` -> `😨`
- `surprise` -> `😲`
- `neutral` -> `😐`
- `disgust` -> `🤢`

Fallback behavior:
- Unknown/unmapped label -> `❓`

### 4.4 `emotion_overlay_node` (optional)
Purpose: operator observability.

Responsibilities:
- Synchronize latest prediction with incoming image
- Draw label + confidence + latency on frame
- Publish `/emotion/debug_image`

## 5. Data and Timing Flow

1. Camera node publishes `/peak_cam/W_6340/image_raw` continuously.
2. `emotion_frame_sampler` stores latest frame and republishes at 4 Hz.
3. `emotion_inference_node` preprocesses sampled frame and performs inference.
4. Predictions published with frame timestamp to `/emotion/prediction`.
5. `emotion_emoji_mapper` transforms prediction label into emoji and publishes `/emotion/emoji`.
6. Downstream nodes consume `/emotion/prediction` and `/emotion/emoji` for behavior, UI, or monitoring.

Latency budget targets (initial):
- Frame sampling jitter: < 20 ms
- Inference time (CPU baseline): <= 150 ms typical
- End-to-end sample-to-publish: <= 250 ms typical

## 6. Preprocessing and Inference Details

Input handling:
- Convert ROS `sensor_msgs/Image` to `numpy` array via `cv_bridge`
- Convert BGR -> RGB when needed
- Preserve original timestamp from image header

Model invocation options:
- Preferred: Hugging Face `pipeline("image-classification", model="dima806/facial_emotions_image_detection")`
- Alternative: `AutoImageProcessor` + `AutoModelForImageClassification` for more control and batching

Postprocessing:
- Sort predictions descending confidence
- Keep top-k (default k=3)
- Publish normalized confidence values from model output
- Map top-1 label to emoji and publish emoji topic for lightweight consumers

## 7. Runtime and Deployment

Execution model:
- ROS2 Python nodes (`rclpy`) for rapid integration
- Single-process composition is acceptable for MVP
- Use separate process for inference node if CPU contention appears

Dependencies (MVP):
- `rclpy`
- `sensor_msgs`
- `cv_bridge`
- `opencv-python`
- `torch`
- `transformers`
- `Pillow`

Configuration parameters:
- `input_topic` (default: `/peak_cam/W_6340/image_raw`)
- `sample_rate_hz` (default: `4.0`)
- `model_id` (default: `dima806/facial_emotions_image_detection`)
- `device` (`cpu` or `cuda`)
- `top_k` (default: `3`)

## 8. Reliability and Failure Handling

- On model load failure: node logs error and retries with backoff
- On malformed image frame: drop frame, increment error counter, continue
- If inference exceeds sampling interval: process latest frame only (drop stale)
- On unknown label in mapper: publish fallback emoji (`❓`) and increment unmapped_label counter
- Publish diagnostics counters:
  - received_frames
  - sampled_frames
  - dropped_frames
  - inference_failures
  - unmapped_labels
  - avg_inference_ms

## 9. Validation Plan

Functional checks:
- Verify 4 Hz publish rate on `/emotion/input_image`
- Verify prediction output exists for each sampled frame
- Verify `/emotion/emoji` output exists for each `/emotion/prediction` message
- Verify timestamp continuity and no queue growth

Performance checks:
- Measure inference latency distribution over 5 minutes
- Confirm no sustained backlog under expected camera FPS

Quality checks:
- Manual spot-check predictions against known facial expression test images
- Validate top-1 consistency across repeated frames
- Validate label-to-emoji mapping table and fallback (`❓`) on unknown labels

## 10. Future Extensions

- Add face detection + crop before emotion classification (improves robustness)
- Add temporal smoothing (moving average / HMM)
- Add per-person tracking and multi-face outputs
- Export metrics to Prometheus + ROS2 diagnostics dashboard
