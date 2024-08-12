import rclpy
from rclpy.node import Node
import wbtros2_interface.msg as wbtros2_interface
import paho.mqtt.client as mqtt



class ROS2Handler(Node):

    def __init__(self) -> None:
        super().__init__('WBTROS2_ROS2Handler_Node')

        try:
            self.declare_parameter('from_mqtt_topics', rclpy.Parameter.Type.STRING_ARRAY)
            self.declare_parameter('to_mqtt_topics', rclpy.Parameter.Type.STRING_ARRAY)
            self.__from_mqtt_topics__   = self.get_parameter('from_mqtt_topics').value
            self.__to_mqtt_topics__     = self.get_parameter('to_mqtt_topics').value

        except:
            self.get_logger().error('Please run the Webots ROS2 Handler via launch with specified parameters')
            self.destroy_node()
            quit()

        self.__mqtt_protocol__  = mqtt.MQTTv311
        self.__mqtt_transport__ = 'websockets'
        self.__mqtt_ws_path__   = '/mqtt'
        self.__mqtt_address__   = 'localhost'
        self.__mqtt_port__      = 9001

        self.mqtt_client = mqtt.Client(
            callback_api_version    = mqtt.CallbackAPIVersion.VERSION2, 
            protocol                = self.__mqtt_protocol__,
            transport               = self.__mqtt_transport__
        )
        self.mqtt_client.on_connect = self.__on_connect__
        self.mqtt_client.on_message = self.__on_message__
        self.mqtt_client.ws_set_options(path=self.__mqtt_ws_path__)

        self.node_subs      = list()
        self.node_pubs      = dict()

        for topic in self.__to_mqtt_topics__:
            self.node_subs = self.create_subscription(
                msg_type    = wbtros2_interface.Wbtros2,
                topic       = topic,
                callback    = self.__subscriber_callback__,
                qos_profile = 1000
            )
            self.get_logger().info(f'Topic: {topic} is ready to be published!')


        for topic in self.__from_mqtt_topics__:
            self.node_pubs.update({
                    topic: self.create_publisher(
                        msg_type    = wbtros2_interface.Wbtros2,
                        topic       = topic,
                        qos_profile = 1000
                    )
                }
            )



    def __on_connect__(self, client, userdata, flags, rc, __) -> None:

        if rc == 0:
            self.get_logger().info(f'Successfully connected to "mqtt://{self.__mqtt_address__}:{self.__mqtt_port__}"')

            for topic in self.__from_mqtt_topics__:
                self.mqtt_client.subscribe(topic)
                self.get_logger().info(f'Topic: {topic} is ready to be subscribed!')

        else:
            self.get_logger().error(f'Failed to connect to "mqtt://{self.__mqtt_address__}:{self.__mqtt_port__}"')
            self.destroy_node()
            quit()



    def __on_message__(self, client, userdata, msg) -> None:
        message         = wbtros2_interface.Wbtros2()
        message.topic   = msg.topic
        message.payload = str(msg.payload.decode())
        self.node_pubs[msg.topic].publish(message)



    def __subscriber_callback__(self, msg:wbtros2_interface.Wbtros2) -> None:
        self.mqtt_client.publish(msg.topic, msg.payload)



    def start(self) -> None:
        self.mqtt_client.connect(self.__mqtt_address__, self.__mqtt_port__)
        self.mqtt_client.loop_start()



    def stop(self) -> None:
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()