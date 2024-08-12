from .modules.controller_node import *



def main(args=None) -> None:
    rclpy.init()
    node = Turtlebot3Controller()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()