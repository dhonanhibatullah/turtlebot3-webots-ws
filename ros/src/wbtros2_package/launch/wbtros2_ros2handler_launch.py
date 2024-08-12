from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    
    wbtros2_ros2handler_node = Node(
        package     = 'wbtros2_package',
        executable  = 'wbtros2_ros2handler',
        name        = 'WBTROS2_ROS2Handler_Node',
        parameters  = [
            {'from_mqtt_topics': [
                'test/from_mqtt_topic1',
                'test/from_mqtt_topic2'
            ]},
            {'to_mqtt_topics': [
                'test/to_mqtt_topic1',
                'test/to_mqtt_topic2'
            ]}
        ]
    )

    return LaunchDescription([
        wbtros2_ros2handler_node
    ])