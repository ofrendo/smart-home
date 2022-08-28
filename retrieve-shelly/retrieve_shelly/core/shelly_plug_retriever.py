# https://github.com/StyraHem/pyShelly
from pyShelly import pyShelly
from pyShelly import powermeter
import time
import logging
import requests
from retrieve_shelly.core.logging_config import configure_logging
from typing import Dict, List
from retrieve_shelly.core.db_manager import DbManager, ShellySensorMeasurement, ShellySensorPayload
from pydantic import BaseModel
import pathlib

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS: int = 60
CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS: int = 60


class ShellyPlug(BaseModel):
    name: str  # Example: shellyplug-s-123456
    ip_address: str


class ShellyPlugConfig(BaseModel):
    plugs: List[ShellyPlug]


class ShellyPlugHttpRetriever:
    def retrieve_sensor_payload(self, plug: ShellyPlug) -> ShellySensorPayload:
        """
        Retrieves the power (in Watt) via blocking HTTP call
        """
        # get IP address and query /status
        # .meters[0].power
        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-settings-relay-0

        url: str = f"http://{plug.ip_address}/status"
        logger.info(f"Requesting power from Shelly Plug S with url='{url}'...")

        response_raw = requests.get(url)
        response: Dict = response_raw.json()
        try:
            power_w: float = response["meters"][0]["power"]
            # "total" refers to watt-minutes: https://shelly-api-docs.shelly.cloud/gen1/#shelly1-1pm-status
            # Note that this resets every time the plug reboots
            energy_watt_minutes: float = response["meters"][0]["total"]
            energy_watt_hours: float = energy_watt_minutes / 60
            payload = ShellySensorPayload(sensor_id=plug.name, measurements=[
                ShellySensorMeasurement(measurement_name="power", measurement_value=power_w),
                ShellySensorMeasurement(measurement_name="energy_wh", measurement_value=energy_watt_hours),
            ])
            logger.info(f"Found payload={payload}")
            return payload
        except Exception as exception:
            logger.error("Error caught while trying to read power value", exc_info=exception)


class ShellyPlugRetriever:
    def __init__(self):
        self.shelly_plug_config: ShellyPlugConfig = self._load_shelly_plug_config()
        self.shelly_plug_http_retriever = ShellyPlugHttpRetriever()
        self.db_manager = DbManager()

    def _load_shelly_plug_config(self) -> ShellyPlugConfig:
        current_path = pathlib.Path(__file__)
        config_path = str(current_path.parent.parent.resolve()) + "/shelly_plug_config.json"
        #path: str = "retrieve_shelly/shelly_plug_config.json"
        
        logger.info(f"Loading shelly plug config from path='{config_path}'...")
        config = ShellyPlugConfig.parse_file(config_path)
        logger.info(f"Loaded shelly plug config: {config}")
        return config

    def _on_device_found(self, device, code):
        if isinstance(device, powermeter.PowerMeter):
            url: str = f"http://{device.ip_addr}/status"
            logger.info(f"Found powermeter device. Requesting url='{url}'...")

            response_raw = requests.get(url)
            response: Dict = response_raw.json()
            try:
                power: float = response["meters"][0]["power"]
                logger.info(f"Found power={power}W")

            except Exception as exception:
                logger.error("Error caught while trying to read power value", exc_info=exception)

    def _poll_with_discovery(self):
        """
        Discover seems unreliable
        """
        logger.info(f"Polling for new values. Searching for devices for {CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS}s...")
        shelly = pyShelly()
        shelly.cb_device_added.append(self._on_device_found)
        shelly.start()
        shelly.discover()

        time.sleep(CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS)
        logger.info(f"Stopping discovery of new devices for this polling iteration (waited {CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS}s).");
        shelly.close()

    def _poll_with_http(self):
        for plug in self.shelly_plug_config.plugs:
            measurement: ShellySensorPayload = self.shelly_plug_http_retriever.retrieve_sensor_payload(plug=plug)
            self.db_manager.save_shelly_to_influxdb(measurement)

    def start_retrieval(self):
        """
        Starts polling every POLL_INTERVAL_SECONDS seconds. Blocking function
        """
        while True:
            self._poll_with_http()
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    # One time sensor data retrieval
    configure_logging()
    logger.info("Starting one-time data retrieval...")
    shelly_plug_retriever = ShellyPlugRetriever()
    shelly_plug_retriever._poll_with_http()
