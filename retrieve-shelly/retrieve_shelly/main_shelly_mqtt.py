from retrieve_shelly.core.mqtt_subscriber import ShellyMqttSubscriber
from retrieve_shelly.core.logging_config import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)

logger.info("Starting Shelly H&T sensor retrieval script...")

subscriber = ShellyMqttSubscriber(mqtt_host="localhost")
subscriber.connect_and_loop_forever()  # blocks main thread forever
