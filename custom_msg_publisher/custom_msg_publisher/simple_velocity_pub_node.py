import rclpy
from rclpy.node import Node
from simple_velocity_msg.msg import SimpleVelocity 
#------------------------------------------------
#                    TODO:
#  Import your SimpleVelocity here
#------------------------------------------------


from geometry_msgs.msg import Twist


class MyPublisher(Node):


    def __init__(self):
        super().__init__('MyPublisher')
        self.publishers_ = self.create_publisher(SimpleVelocity, '/simple_vel', 10)
        
        #------------------------------------------------
        #                    TODO:
        #  Create your publisher below! Remember that your
        #  publishes StringVelocity type message to a topic called
        #  simple_vel
        #------------------------------------------------
        self.subscription_ = self.create_subscription(Twist, '/cmd_vel', self.listener_callback, 10)
        #------------------------------------------------
        #                    TODO:
        #  Create your subscriber below! Remember that your
        #  subscribes to twist type message from the topic
        #  simple_vel
        #------------------------------------------------

        #------------------------------------------------
        #                    TODO:
        #  Once you have completed creating your publisher,
        #  Initialise a twist message and call it self.msg
        #------------------------------------------------


        self.msg = Twist()
        #------------------------------------------------
        #                    TODO:
        # Create your timer below and it should be set at
        # 1 seocnds
        #------------------------------------------------
        self.timer = self.create_timer(1.0, self.timer_callback) 


        
    def listener_callback(self, msg):
        self.msg = msg

    def timer_callback(self):
        msg = SimpleVelocity()
        msg.linear_velocity = self.msg.linear.x
        msg.angular_velocity = self.msg.angular.z

        #------------------------------------------------
        #                    TODO:
        #  Create a line below that publishes the msg object to
        #  the topic 
        #------------------------------------------------
        self.publishers_.publish(msg)

        self.get_logger().info('Publishing linear velocity: "%s" m/s, angular velocity: "%s" rad/s' % (msg.linear_velocity, msg.angular_velocity))

       

def main(args=None):
    rclpy.init(args=args)

    my_publisher = MyPublisher()

    rclpy.spin(my_publisher)

    my_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()