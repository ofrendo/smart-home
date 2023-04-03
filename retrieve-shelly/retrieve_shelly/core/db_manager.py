import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pydantic import BaseModel
from typing import List

logger = logging.getLogger(__name__)


class ShellySensorMeasurement(BaseModel):
    sensor_id: str  # shellyht-123
    measurement_name: str  # temperature, battery, humidity, power, energy_wh
    measurement_value: float


class DbManager:
    def __init__(self):
        self.bucket: str = "my_database"
        self.client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def save_shelly_to_influxdb(self, measurement: ShellySensorMeasurement):
        logger.info(f"Saving payload in DB: {measurement}")
        db_payload: Point = Point(measurement.sensor_id)
        db_payload.field(measurement.measurement_name, measurement.measurement_value)

        self.write_api.write(bucket=self.bucket, record=db_payload)
        logger.info("Saved payload in DB.")
