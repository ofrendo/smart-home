from typing import List
import paho.mqtt.client as mqtt
import logging

from retrieve_shelly.db_manager import DbManager, ShellySensorPayload

logger = logging.getLogger(__name__)


measurement_names_to_process: List[str] = ["temperature", "humidity", "battery"]


class ShellyMqttSubscriber:
    
    def __init__(self, mqtt_host: str):
        # Shelly topics format: 
        # shellies/shellyht-123456/sensor/temperature
        # shellies/shellyht-123456/sensor/humidity
        # shellies/shellyht-123456/sensor/battery
        self.mqtt_host: str = mqtt_host
        self.mqtt_topic: str = "shellies/+/sensor/+"
        self.mqtt_client: mqtt.Client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.db_manager = DbManager()

    def connect_and_loop_forever(self):
        logger.info(f"Connecting to MQTT host on '{self.mqtt_host}'...")
        self.mqtt_client.connect(host=self.mqtt_host, port=1883)
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        # The callback for when the client receives a CONNACK response from the server.
        logger.info(f"Connected to MQTT broker with result code {rc}. Subscribing to topic '{self.mqtt_topic}'...")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.mqtt_client.subscribe(self.mqtt_topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logger.info(f"Received message on topic '{msg.topic}': '{msg.payload}'")
        # shellies/shellyht-123456/sensor/temperature
        topic_parts: List[str] = str(msg.topic).split("/")
        try: 
            measurement_name: str = topic_parts[3]
            if measurement_name not in measurement_names_to_process:
                return
            
            payload = ShellySensorPayload(
                sensor_id=topic_parts[1],
                measurement_name=topic_parts[3],
                measurement_value=float(msg.payload)
            )
            self.db_manager.save_shelly_to_influxdb(payload=payload)
        except Exception as exception:
            logger.error(f"Error while processing MQTT message: {exception}")
