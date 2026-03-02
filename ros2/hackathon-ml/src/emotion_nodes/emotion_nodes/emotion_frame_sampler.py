from __future__ import annotations

from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image


class EmotionFrameSamplerNode(Node):
    """Sample latest camera frame at a fixed cadence for downstream inference."""

    def __init__(self) -> None:
        super().__init__("emotion_frame_sampler")

        self.declare_parameter("input_topic", "/peak_cam/W_6340/image_raw")
        self.declare_parameter("output_topic", "/emotion/input_image")
        self.declare_parameter("sample_rate_hz", 4.0)
        self.declare_parameter("publish_if_no_new_frame", False)
        self.declare_parameter("diagnostics_period_s", 5.0)

        self._input_topic = str(self.get_parameter("input_topic").value)
        self._output_topic = str(self.get_parameter("output_topic").value)
        self._sample_rate_hz = float(self.get_parameter("sample_rate_hz").value)
        self._publish_if_no_new_frame = bool(
            self.get_parameter("publish_if_no_new_frame").value
        )
        self._diagnostics_period_s = float(
            self.get_parameter("diagnostics_period_s").value
        )

        self._validate_params()

        self._latest_msg: Optional[Image] = None
        self._latest_seq = 0
        self._last_published_seq = -1
        self._received_frames = 0
        self._sampled_frames = 0
        self._empty_ticks = 0
        self._skipped_duplicate_ticks = 0
        self._start_time = self.get_clock().now()

        # Equivalent to SensorDataQoS with an explicit depth=1 requirement.
        qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
        )

        self._sub = self.create_subscription(
            Image, self._input_topic, self._on_image, qos
        )
        self._pub = self.create_publisher(Image, self._output_topic, qos)

        sample_period_s = 1.0 / self._sample_rate_hz
        self._sample_timer = self.create_timer(sample_period_s, self._on_sample_tick)
        self._diag_timer = self.create_timer(
            self._diagnostics_period_s, self._on_diag_tick
        )

        self.get_logger().info(
            "emotion_frame_sampler configured: "
            f"input_topic={self._input_topic}, "
            f"output_topic={self._output_topic}, "
            f"sample_rate_hz={self._sample_rate_hz:.3f}, "
            f"publish_if_no_new_frame={self._publish_if_no_new_frame}, "
            f"diagnostics_period_s={self._diagnostics_period_s:.3f}"
        )

    def _validate_params(self) -> None:
        if self._sample_rate_hz <= 0.0:
            raise ValueError("sample_rate_hz must be > 0.0")
        if self._diagnostics_period_s <= 0.0:
            raise ValueError("diagnostics_period_s must be > 0.0")

    def _on_image(self, msg: Image) -> None:
        try:
            self._latest_msg = msg
            self._latest_seq += 1
            self._received_frames += 1
        except Exception as exc:  # pragma: no cover
            self.get_logger().error(f"image callback failure: {exc}")

    def _on_sample_tick(self) -> None:
        if self._latest_msg is None:
            self._empty_ticks += 1
            return

        if (
            not self._publish_if_no_new_frame
            and self._latest_seq == self._last_published_seq
        ):
            self._skipped_duplicate_ticks += 1
            return

        self._pub.publish(self._latest_msg)
        self._sampled_frames += 1
        self._last_published_seq = self._latest_seq

    def _on_diag_tick(self) -> None:
        now = self.get_clock().now()
        elapsed_s = max((now - self._start_time).nanoseconds / 1e9, 1e-9)
        dropped_frames = max(0, self._received_frames - self._sampled_frames)
        effective_output_hz = self._sampled_frames / elapsed_s

        self.get_logger().info(
            "frame_sampler metrics: "
            f"received_frames={self._received_frames}, "
            f"sampled_frames={self._sampled_frames}, "
            f"dropped_frames={dropped_frames}, "
            f"empty_ticks={self._empty_ticks}, "
            f"skipped_duplicate_ticks={self._skipped_duplicate_ticks}, "
            f"effective_output_hz={effective_output_hz:.3f}"
        )


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = EmotionFrameSamplerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
