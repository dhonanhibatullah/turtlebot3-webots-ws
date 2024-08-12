from .modules.wbtros2_ros2handler_node import *



def main(args=None) -> None:
    rclpy.init()
    node = ROS2Handler()
    node.start()

    rclpy.spin(node)

    node.stop()
    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()