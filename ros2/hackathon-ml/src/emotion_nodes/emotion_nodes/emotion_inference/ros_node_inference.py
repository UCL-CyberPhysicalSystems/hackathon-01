"""ROS2 node wrapping the inference engine. Runs inside the ROS2 container."""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import json

from inference import EmotionInferenceEngine


class EmotionInferenceNode(Node):
    def __init__(self):
        super().__init__("emotion_inference_node")

        # Parameters
        self.declare_parameter("model_id", "dima806/facial_emotions_image_detection")
        self.declare_parameter("device", "cpu")
        self.declare_parameter("top_k", 3)

        model_id = self.get_parameter("model_id").get_parameter_value().string_value
        device = self.get_parameter("device").get_parameter_value().string_value
        top_k = self.get_parameter("top_k").get_parameter_value().integer_value

        # Core engine
        self.engine = EmotionInferenceEngine(
            model_id=model_id, device=device, top_k=top_k
        )
        self.bridge = CvBridge()

        # QoS
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Sub & Pub
        self.create_subscription(Image, "/emotion/input_image", self.image_callback, qos)
        self.prediction_pub = self.create_publisher(String, "/emotion/prediction", 10)

        self.get_logger().info(f"EmotionInferenceNode ready — model: {model_id}")
        self.get_logger().info("Waiting for images on /emotion/input_image...")

    def image_callback(self, msg: Image):
        self.get_logger().info(f"Received image — frame_id: {msg.header.frame_id}")

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        except Exception as e:
            self.get_logger().error(f"cv_bridge conversion failed: {e}")
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
                f'{result["top_label"]} ({result["top_confidence"]:.2f}) — '
                f'{result["inference_ms"]:.1f}ms'
            )
        except Exception as e:
            self.get_logger().error(f"Inference failed: {e}")


def main(args=None):
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