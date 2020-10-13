from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "my_database"
client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

def saveToInfluxDB(payload):
    measurementName = payload["label"] + " (" + payload["room"] + ")"
    dbPayload = Point(measurementName)

    dbPayload._time = payload["lastStatusUpdate"] 
    
    for fieldName, value in payload.items(): 
        if fieldName != "label" and fieldName != "room" and fieldName != "lastStatusUpdate": 
            dbPayload.field(fieldName, value)

    write_api.write(bucket=bucket, record=dbPayload)
    #print("Saved payload in DB.")



