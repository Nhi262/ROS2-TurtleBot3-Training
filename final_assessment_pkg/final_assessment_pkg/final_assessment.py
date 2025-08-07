import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseArray, Pose
from perception_msgs.srv import GetObjectLocation
import numpy as np
import time

class TurtleBotAruco(Node):
    def __init__(self):
        super().__init__('final_assessment')
        # Recommended values, change if you want!
        self.distance_threshold = 3.0
        self.max_linear_velocity = 0.1
        self.max_angular_velocity = 1.0
        # self.close_distance = 0.1

        self.service_client = self.create_client(GetObjectLocation, '/find_objects')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.twist_msg = Twist()

        while not self.service_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.timer = self.create_timer(0.1, self.send_request) # thay đổi xuống còn 50ms để chạy nhanh hơn 


    def send_request(self):
        self.req = GetObjectLocation.Request()
        self.future_ = self.service_client.call_async(self.req)  
        self.future_.add_done_callback(self.response_callback)  

    def response_callback(self, future):
        try:
            result = future.result()
            self.get_logger().info("Service response result: %d" % result.result)

            
            pose = result.object_pose
            self.get_logger().info(
                f"Object Pose - x: {pose.position.x:.2f}, y: {pose.position.y:.2f}, z: {pose.position.z:.2f}")

            self.get_logger().info(
                f"Orientation - x: {pose.orientation.x:.2f}, y: {pose.orientation.y:.2f}, z: {pose.orientation.z:.2f}, w: {pose.orientation.w:.2f}")

            self.check_tag(result, pose)
            
            

        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def check_tag(self, result):

        if result is True:
            #level 1
            self.get_logger().info(f"Aruco tag found")
            self.twist_msg.msg.linear.x = self.max_linear_velocity
            self.twist_msg.msg.angular.z = 0.0
            self.move_turtlebot(self.max_angular_velocity, 0.0)
            #level 2 
            # current_distance = self.get_tag_distance(pose.position.x, pose.position.y                     )

        else:
            self.get_logger().info(f"There is no aruco tag")
            self.move_turtlebot(0.0, 0.0)

        self.publisher_.publish(self.twist_msg)
        
        #-----------------------------------------------------------------------
        #                    TODO:
        #  Create a function check the tag poses, and move the robot accordingly
        #------------------------------------------------------------------------

    
    def get_tag_pose(self, pose):
        # self.x = pose.position.x
        # self.y = pose.position.y 
        # self.distance = self.get_tag_angle(x,y)
        pass
        #------------------------------------------------
        #                    TODO:
        #  Create a function to get the pose of the tag 
        #------------------------------------------------

    def move_turtlebot(self, linear_velocity, angular_velocity):
        self.twist_msg.linear.x = linear_velocity
        self.twist_msg.angular.z = angular_velocity
        pass
        #------------------------------------------------
        #                    TODO:
        #  Create a function to move the robot
        #------------------------------------------------

    def get_tag_distance(self, x, y):
        return math.sqrt((x ** 2) + (y ** 2))

   
    

    def get_tag_angle(self, x, y):
        return np.arctan2(y, x)


def main(args=None):
    rclpy.init(args=args)
    turtlebot_move = TurtleBotAruco()
    rclpy.spin(turtlebot_move)
    turtlebot_move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
