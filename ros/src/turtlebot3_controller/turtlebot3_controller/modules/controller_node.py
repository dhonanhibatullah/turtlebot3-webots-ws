import rclpy
from rclpy.node import Node
import wbtros2_interface.msg as wbtros2_interface
import numpy as np
import json



class Turtlebot3Controller(Node):

    def __init__(self) -> None:
        super().__init__('Turtlebot3Controller_Node')

        self.lidar_init         = True
        self.lidar_max_range    = 0.0
        self.lidar_width        = 0.0
        self.lidar_image        = []
        self.motor_vel_msg      = {
            'r_wheel': 0.0,
            'l_wheel': 0.0
        }

        self.motor_vel_pub = self.create_publisher(
            msg_type    = wbtros2_interface.Wbtros2,
            topic       = 'turtlebot3/motor_speed',
            qos_profile = 1000
        )

        self.lidar_sub = self.create_subscription(
            msg_type    = wbtros2_interface.Wbtros2,
            topic       = 'turtlebot3/lidar',
            callback    = self.lidarCallback,
            qos_profile = 1000
        )

        self.update_timer = self.create_timer(
            timer_period_sec    = 0.032,
            callback            = self.updateCallback
        )

        self.time = 0.0



    def lidarCallback(self, msg:wbtros2_interface.Wbtros2) -> None:
        msg_json = json.loads(msg.payload)

        if self.lidar_init:
            self.lidar_max_range    = float(msg_json['max_range'])
            self.lidar_width        = float(msg_json['width'])
            self.lidar_init         = False

        self.lidar_image = msg_json['image']



    def updateCallback(self) -> None:
        vel = 6.0*np.sin(2.0*np.pi*0.3*self.time)
        self.motor_vel_msg['r_wheel'] = vel
        self.motor_vel_msg['l_wheel'] = vel

        pub_msg         = wbtros2_interface.Wbtros2()
        pub_msg.topic   = 'turtlebot3/motor_speed'
        pub_msg.payload = json.dumps(self.motor_vel_msg)

        self.motor_vel_pub.publish(pub_msg) 

        self.time += 0.032