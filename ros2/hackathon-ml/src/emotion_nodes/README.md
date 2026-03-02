# emotion_nodes

ROS2 Python package for nodes in the facial expression pipeline defined in `docs/architecture.md`.

Current status:
- Implemented: `emotion_frame_sampler`
- Planned by architecture: `emotion_inference_node`, `emotion_emoji_mapper`, optional `emotion_overlay_node`

## Architecture Alignment

From `docs/architecture.md`, `emotion_frame_sampler` is responsible for:
- Subscribing to `/peak_cam/W_6340/image_raw` (`sensor_msgs/msg/Image`)
- Keeping only the latest frame
- Sampling on a 4 Hz timer (250 ms)
- Publishing to `/emotion/input_image` (`sensor_msgs/msg/Image`)
- Using depth-1, sensor-data QoS behavior to avoid backlog

This package implementation follows that contract and includes an optional duplicate-suppression mode.

## Node: `emotion_frame_sampler`

Entrypoint:
- `emotion_frame_sampler` (Python module: `emotion_nodes.emotion_frame_sampler`)

### Topics

Subscribe:
- `input_topic` (default: `/peak_cam/W_6340/image_raw`)
- Type: `sensor_msgs/msg/Image`

Publish:
- `output_topic` (default: `/emotion/input_image`)
- Type: `sensor_msgs/msg/Image`

QoS:
- `KEEP_LAST`, `depth=1`, `BEST_EFFORT`, `VOLATILE`

### Parameters

- `input_topic` (`string`, default `/peak_cam/W_6340/image_raw`)
- `output_topic` (`string`, default `/emotion/input_image`)
- `sample_rate_hz` (`double`, default `4.0`, must be `> 0`)
- `publish_if_no_new_frame` (`bool`, default `false`)
- `diagnostics_period_s` (`double`, default `5.0`, must be `> 0`)

### Publish Cadence Semantics

- Timer cadence is always `sample_rate_hz`.
- If `publish_if_no_new_frame=false` (default): publish only when a newer frame has arrived since the previous publish; effective output rate is `<= sample_rate_hz`.
- If `publish_if_no_new_frame=true`: republish latest cached frame every timer tick once at least one frame has been received.

Default mode (`false`) avoids duplicate inference on stale frames when upstream image production is slower than the sampling trigger.

### Diagnostics

The node logs periodic counters:
- `received_frames`
- `sampled_frames`
- `dropped_frames` (derived as `received_frames - sampled_frames`, floored at 0)
- `empty_ticks`
- `skipped_duplicate_ticks`
- `effective_output_hz`

## Build and Run

From workspace root (the directory that contains `src/`):

```bash
colcon build --packages-select emotion_nodes
source install/setup.bash
ros2 run emotion_nodes emotion_frame_sampler
```

Example with parameter overrides:

```bash
ros2 run emotion_nodes emotion_frame_sampler --ros-args \
  -p input_topic:=/peak_cam/W_6340/image_raw \
  -p output_topic:=/emotion/input_image \
  -p sample_rate_hz:=4.0 \
  -p publish_if_no_new_frame:=false \
  -p diagnostics_period_s:=5.0
```

## Quick Verification

In another terminal:

```bash
source install/setup.bash
ros2 topic hz /emotion/input_image
ros2 topic echo /emotion/input_image --once
```

Expected behavior:
- With active camera input, output rate is at most configured `sample_rate_hz`.
- No unbounded queue growth (depth-1 latest-frame behavior).
- Output message header is preserved from input image.
