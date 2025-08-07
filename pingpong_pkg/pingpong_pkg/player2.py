#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from rclpy.duration import Duration

class Player2(Node):

    def __init__(self):
        self.publisher_ = self.create_publisher(Int64, '/ping_pong', 10)
        self.subcription = self.create_subscription(Int64, '/ping_pong', self.player1_callback,10)

        #------------------------------------------------
        #                    TODO:
        # 1.) Create Player2 Publisher of type Int64 to /ping_pong topic
        # 2.) Create Player2 Subscription to /ping_pong of type Int64 to /ping_pong topic
        #------------------------------------------------
        self.count = 0 
        self.get_logger().info('Player2 Ready!')

    def player1_callback(self, player1_msg):
        if player1_msg.data <= self.count: # discard message for player1
            return
        self.get_clock().sleep_for(Duration(seconds=1.0))
        self.counter = self.player1_msg.data 
        counter +=1
        self.get_logger().info(f"Player2 publishing {self.count}")
        msg = Int64()
        msg = self.count
        self.publisher_.publish(msg)
        #------------------------------------------------
        #                    TODO:
        # 3.) Store received data to self.count 
        # 4.) Increment self.count
        # 5.) Log Player 1 Publishing <count>
        # 6.) Publish the self.count value!
        #------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    player2_node = Player2()
    rclpy.spin(player2_node)
    player2_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
