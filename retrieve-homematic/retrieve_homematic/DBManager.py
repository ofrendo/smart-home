from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from util.Logger import logging
import util.TimeUtil as TimeUtil


bucket = "my_database"
client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

def saveToInfluxDB(payload):
    measurementName = payload["label"] + " (" + payload["room"] + ")"
    dbPayload = Point(measurementName)

    # payload.lastStatusUpdate is in LOCAL time ("Europe/Berlin")
    # point.time() expects time in UTC   
    
    localDatetime = payload["lastStatusUpdate"]
    utcDatetime = TimeUtil.convertDatetimeToUtc(localDatetime)

    logging.info("Converted lastStatusUpdate ('" + payload["label"] + "') local time (" + str(localDatetime) + ") to UTC (" + str(utcDatetime) + ")")

    dbPayload.time(utcDatetime)
    
    for fieldName, value in payload.items(): 
        if fieldName != "label" and fieldName != "room" and fieldName != "lastStatusUpdate": 
            dbPayload.field(fieldName, value)

    write_api.write(bucket=bucket, record=dbPayload)
    #print("Saved payload in DB.")


if __name__ == "__main__":
    logging.info("Saving single test value in DB...")
    testPayload = Point("testMeasurement")
    testPayload.field("testField", 0.5)
    
    # Point.time expects datetime in UTC 
    #logging.info("Current UTC time: " + str(datetime.now(pytz.utc)))

    testPayload.time(datetime.now(pytz.utc))

    write_api.write(bucket="test_database", record=testPayload)
   