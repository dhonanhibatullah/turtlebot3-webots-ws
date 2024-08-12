from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():

    turtlebot3_controller_node = Node(
        package     = 'turtlebot3_controller',
        executable  = 'controller',
        name        = 'Turtlebot3_Controller_Node'
    )
    
    wbtros2_ros2handler_node = Node(
        package     = 'wbtros2_package',
        executable  = 'wbtros2_ros2handler',
        name        = 'WBTROS2_ROS2Handler_Node',
        parameters  = [
            {'from_mqtt_topics': [
                'turtlebot3/lidar'
            ]},
            {'to_mqtt_topics': [
                'turtlebot3/motor_speed'
            ]}
        ]
    )

    return LaunchDescription([
        turtlebot3_controller_node,
        wbtros2_ros2handler_node
    ])