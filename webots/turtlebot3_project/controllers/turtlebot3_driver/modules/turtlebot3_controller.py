from controller import Robot, Lidar, Motor
from modules.wbthandler import *
import json



class Turtlebot3Controller:

    def __init__(self) -> None:
        self.__lidar_sensor_name__          = 'LDS-01'
        self.__motor_lidar1_name__          = 'LDS-01_main_motor'
        self.__motor_lidar2_name__          = 'LDS-01_secondary_motor'
        self.__motor_right_name__           = 'right wheel motor'
        self.__motor_left_name__            = 'left wheel motor'

        self.robot          = Robot()
        self.timestep       = int(self.robot.getBasicTimeStep())

        self.lidar          = self.robot.getDevice(self.__lidar_sensor_name__)
        self.motor_lidar1   = self.robot.getDevice(self.__motor_lidar1_name__)
        self.motor_lidar2   = self.robot.getDevice(self.__motor_lidar2_name__)
        self.motor_right    = self.robot.getDevice(self.__motor_right_name__)
        self.motor_left     = self.robot.getDevice(self.__motor_left_name__) 

        self.lidar.enable(self.timestep)
        self.motor_lidar1.setPosition(float('inf'))
        self.motor_lidar1.setVelocity(30.0)
        self.motor_lidar2.setPosition(float('inf'))
        self.motor_lidar2.setVelocity(60.0)
        self.motor_right.setPosition(float('inf'))
        self.motor_right.setVelocity(0.0)
        self.motor_left.setPosition(float('inf'))
        self.motor_left.setVelocity(0.0)

        self.lidar_width        = self.lidar.getHorizontalResolution()
        self.lidar_max_range    = self.lidar.getMaxRange()
        self.motor_right_vel    = 0.0
        self.motor_left_vel     = 0.0
        self.motor_vel_update   = False

        self.wbthandler = WBTHandler(
            topic_to_sub=['turtlebot3/motor_speed'],
            subscribe_callback=self.wbthandlerCallback,
            mqtt_address='172.17.81.180'
        )



    def wbthandlerCallback(self, client, userdata, msg) -> None:
        if msg.topic == 'turtlebot3/motor_speed':
            msg_str     = msg.payload.decode()
            msg_json    = json.loads(msg_str)

            self.motor_right_vel    = float(msg_json['r_wheel'])
            self.motor_left_vel     = float(msg_json['l_wheel'])
            self.motor_vel_update   = True

    

    def loop(self) -> None:
        self.wbthandler.start()

        pub_msg = {
            'max_range': self.lidar_max_range,
            'width': self.lidar_width,
            'image': []
        }

        while self.robot.step(self.timestep) != -1:
            pub_msg['image']    = self.lidar.getRangeImage()
            pub_msg_json_str    = json.dumps(pub_msg)
            self.wbthandler.publish(
                'turtlebot3/lidar',
                pub_msg_json_str
            )

            if self.motor_vel_update:
                self.motor_vel_update = False
                self.motor_right.setVelocity(self.motor_right_vel)
                self.motor_left.setVelocity(self.motor_left_vel)

        self.wbthandler.stop()