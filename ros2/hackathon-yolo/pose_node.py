
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import threading
from flask import Flask, Response


# Flask app and shared frame
app = Flask(__name__)
latest_frame = None
frame_lock = threading.Lock()


@app.route('/video')
def video():
   def generate():
       while True:
           with frame_lock:
               if latest_frame is None:
                   continue
               _, jpeg = cv2.imencode('.jpg', latest_frame)
           yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
   return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
   return '<html><body><h2>Pose Estimator</h2><img src="/video" width="100%"/></body></html>'




class PoseEstimatorNode(Node):
   def __init__(self):
       super().__init__('pose_estimator')


       self.model = YOLO('yolov8n-pose.pt')
       self.get_logger().info('Model loaded')


       self.bridge = CvBridge()


       self.subscription = self.create_subscription(
           Image,
           '/peak_cam/W_6340/image_raw',
           self.image_callback,
           10
       )


       self.publisher = self.create_publisher(Image, '/pose_estimator/annotated', 10)


       # Start Flask in background thread
       flask_thread = threading.Thread(
           target=lambda: app.run(host='0.0.0.0', port=5000, debug=False),
           daemon=True
       )
       flask_thread.start()
       self.get_logger().info('Web stream started at http://0.0.0.0:5000')
       self.get_logger().info('Waiting for frames...')


   def image_callback(self, msg: Image):
       global latest_frame


       self.get_logger().info('Frame received!')


       # Convert to OpenCV
       frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
       frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)


       # Run pose estimation
       results = self.model(frame_bgr, verbose=False)
       annotated = results[0].plot()


       # Update shared frame for Flask
       with frame_lock:
           latest_frame = annotated.copy()


       # Publish to ROS
       out_msg = self.bridge.cv2_to_imgmsg(annotated, encoding='bgr8')
       out_msg.header = msg.header
       self.publisher.publish(out_msg)




def main(args=None):
   rclpy.init(args=args)
   node = PoseEstimatorNode()
   try:
       rclpy.spin(node)
   except KeyboardInterrupt:
       pass
   finally:
       node.destroy_node()
       rclpy.shutdown()




if __name__ == '__main__':
   main()
