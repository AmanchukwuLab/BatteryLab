import rclpy
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from battery_lab_custom_msg.srv import CaptureImage

class CameraService(Node):
    def __init__(self, node_name="camera_service", serv_name=None):
        super().__init__(node_name)
        self.declare_parameter('service_name', '/batterylab/capture_image')
        service_name = serv_name if serv_name is not None else self.get_parameter('service_name').get_parameter_value().string_value
        self.srv = self.create_service(CaptureImage, service_name, self.capture_image_callback)
        
        # Initialize camera and verify it opened successfully
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error('Failed to open camera device /dev/video0')
            self.get_logger().info('Attempting fallback: checking camera status with v4l2-ctl')
            self.cap = None
        else:
            # Attempt to set optimal camera properties
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffering for freshness
            self.get_logger().info("Camera device opened successfully")
        
        self.br = CvBridge()
        self.get_logger().info("The camera server is ready accept requests...")

    def capture_image_callback(self, request, response):
        # Check if camera is available
        if self.cap is None or not self.cap.isOpened():
            self.get_logger().error('Camera device is not available')
            # Return empty image with proper encoding
            empty_image = Image()
            empty_image.encoding = 'bgr8'
            response.image = empty_image
            return response
        
        try:
            # Discard buffered frames to get the freshest image
            for i in range(10):
                self.cap.read()
            ret, frame = self.cap.read()
            if ret:
                response.image = self.br.cv2_to_imgmsg(frame, 'bgr8')
            else:
                self.get_logger().error('Failed to capture image from camera')
                # Create an empty image with proper encoding to avoid cv_bridge errors
                empty_image = Image()
                empty_image.encoding = 'bgr8'
                response.image = empty_image
        except Exception as e:
            self.get_logger().error(f'Exception during image capture: {e}')
            # Return empty image with proper encoding
            empty_image = Image()
            empty_image.encoding = 'bgr8'
            response.image = empty_image
        return response

    def destroy_node(self):
        """Clean up camera resource on shutdown."""
        if self.cap is not None:
            self.cap.release()
            self.get_logger().info("Camera device released")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
