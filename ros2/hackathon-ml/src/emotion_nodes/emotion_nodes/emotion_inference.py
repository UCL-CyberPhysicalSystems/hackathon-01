"""Single-file ROS2 emotion inference node and engine."""

from __future__ import annotations

import json
import logging
import time
from typing import Any

import numpy as np
import rclpy
from cv_bridge import CvBridge
from PIL import Image as PILImage
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from transformers import pipeline as hf_pipeline

logger = logging.getLogger(__name__)


class EmotionInferenceEngine:
    """Wrap Hugging Face image-classification pipeline."""

    def __init__(
        self,
        model_id: str = "dima806/facial_emotions_image_detection",
        device: str = "cpu",
        top_k: int = 3,
        max_retries: int = 3,
    ) -> None:
        self.model_id = model_id
        self.device = device
        self.top_k = top_k
        self.pipeline = None
        self._load_model(max_retries)

    def _load_model(self, max_retries: int) -> None:
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    "Loading model (attempt %d/%d): %s",
                    attempt,
                    max_retries,
                    self.model_id,
                )
                self.pipeline = hf_pipeline(
                    "image-classification",
                    model=self.model_id,
                    device=-1 if self.device == "cpu" else 0,
                )
                logger.info("Model loaded successfully.")
                return
            except Exception as exc:
                logger.error("Model load failed: %s", exc)
                if attempt < max_retries:
                    time.sleep(2**attempt)
                else:
                    raise RuntimeError(
                        f"Could not load model after {max_retries} retries"
                    ) from exc

    def predict(self, image: Any) -> dict[str, Any]:
        if self.pipeline is None:
            raise RuntimeError("Pipeline not loaded")

        if isinstance(image, np.ndarray):
            pil_image = PILImage.fromarray(image)
        else:
            pil_image = image

        t_start = time.monotonic()
        results = self.pipeline(pil_image, top_k=self.top_k)
        inference_ms = (time.monotonic() - t_start) * 1000.0

        labels = [r["label"] for r in results]
        confidences = [round(r["score"], 4) for r in results]

        return {
            "top_label": labels[0],
            "top_confidence": confidences[0],
            "labels": labels,
            "confidences": confidences,
            "inference_ms": round(inference_ms, 2),
        }


class EmotionInferenceNode(Node):
    """ROS2 node that consumes sampled images and publishes JSON predictions."""

    def __init__(self) -> None:
        super().__init__("emotion_inference_node")

        self.declare_parameter("model_id", "dima806/facial_emotions_image_detection")
        self.declare_parameter("device", "cpu")
        self.declare_parameter("top_k", 3)

        model_id = self.get_parameter("model_id").get_parameter_value().string_value
        device = self.get_parameter("device").get_parameter_value().string_value
        top_k = self.get_parameter("top_k").get_parameter_value().integer_value

        self.engine = EmotionInferenceEngine(
            model_id=model_id, device=device, top_k=top_k
        )
        self.bridge = CvBridge()

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.create_subscription(Image, "/emotion/input_image", self.image_callback, qos)
        self.prediction_pub = self.create_publisher(String, "/emotion/prediction", 10)

        self.get_logger().info(f"EmotionInferenceNode ready - model: {model_id}")

        # Matches existing behavior: one startup self-test inference.
        self.startup_timer = self.create_timer(2.0, self.run_startup_test)

    def run_startup_test(self) -> None:
        self.startup_timer.cancel()
        self.get_logger().info("Running startup test with dummy 224x224 image...")

        dummy = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        msg = self.bridge.cv2_to_imgmsg(dummy, encoding="rgb8")
        msg.header.frame_id = "startup_test"
        msg.header.stamp = self.get_clock().now().to_msg()

        self.image_callback(msg)
        self.get_logger().info("Startup test complete. Waiting for /emotion/input_image...")

    def image_callback(self, msg: Image) -> None:
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        except Exception as exc:
            self.get_logger().error(f"cv_bridge conversion failed: {exc}")
            return

        try:
            result = self.engine.predict(cv_image)
            result["header"] = {
                "stamp_sec": msg.header.stamp.sec,
                "stamp_nanosec": msg.header.stamp.nanosec,
                "frame_id": msg.header.frame_id,
            }

            out_msg = String()
            out_msg.data = json.dumps(result)
            self.prediction_pub.publish(out_msg)

            self.get_logger().info(
                f'{result["top_label"]} ({result["top_confidence"]:.2f}) - '
                f'{result["inference_ms"]:.1f}ms'
            )
        except Exception as exc:
            self.get_logger().error(f"Inference failed: {exc}")


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = EmotionInferenceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
