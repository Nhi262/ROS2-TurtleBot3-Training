
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np
import cv2


class ViewImage(Node):
    def __init__(self):
        super().__init__('image_processing_node')
        self.bridge = CvBridge()
        self.image_window = cv2.namedWindow("Camera Output")
        self.subscriber_ = self.create_subscription(Image, '/image_raw', self.listener_callback, 10)
       
    def listener_callback(self, msg):
        self.get_logger().info(f'my subscirber node has started')
        self.view_image(msg)

    def view_image(self, img_msg):
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')
        cv2.imshow("image", cv_image)
        cv2.waitKey(1)
    
def main():
    rclpy.init()
    node = ViewImage()
    rclpy.spin(node)


    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()