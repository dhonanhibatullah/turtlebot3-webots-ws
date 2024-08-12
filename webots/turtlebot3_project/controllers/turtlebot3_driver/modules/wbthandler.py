import paho.mqtt.client as mqtt
from typing import Callable, Any



class WBTHandler:

    def __init__(self, topic_to_sub:list, subscribe_callback:Callable[[Any, Any, Any], None], mqtt_address:str) -> None:
        self.__mqtt_protocol__  = mqtt.MQTTv311
        self.__mqtt_transport__ = 'websockets'
        self.__mqtt_ws_path__   = '/mqtt'
        self.__mqtt_address__   = mqtt_address
        self.__mqtt_port__      = 9001
        self.__topic_to_sub__   = topic_to_sub

        self.mqtt_client = mqtt.Client(
            callback_api_version    = mqtt.CallbackAPIVersion.VERSION2, 
            protocol                = self.__mqtt_protocol__,
            transport               = self.__mqtt_transport__
        )
        self.mqtt_client.on_connect = self.__on_connect__
        self.mqtt_client.on_message = subscribe_callback
        self.mqtt_client.ws_set_options(path=self.__mqtt_ws_path__)


    
    def __on_connect__(self, client, userdata, flags, rc, __) -> None:
        if rc == 0:
            print(f'Successfully connected to "mqtt://{self.__mqtt_address__}:{self.__mqtt_port__}"')
            
            for topic in self.__topic_to_sub__:
                self.mqtt_client.subscribe(topic)
                print(f'Subscribed to {topic}!')

        else:
            print(f'Failed to connect to "mqtt://{self.__mqtt_address__}:{self.__mqtt_port__}"')
            quit()



    def publish(self, topic:str, payload:str) -> None:
        self.mqtt_client.publish(topic, payload)



    def start(self) -> None:
        print('------[ STARTING WEBOTS <-> ROS2 GATEWAY HANDLER ]------')
        self.mqtt_client.connect(self.__mqtt_address__, self.__mqtt_port__)
        self.mqtt_client.loop_start()



    def stop(self) -> None:
        print('------[ STOPPING WEBOTS <-> ROS2 GATEWAY HANDLER ]------')
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()