const { Client } = require('tplink-smarthome-api');
const {InfluxDB, Point, HttpError} = require('@influxdata/influxdb-client');

const POLL_INTERVAL_SECONDS = 60;
const url = "http://localhost:8086";
const token = "my-token"; 
const org = "my-org";
const bucket = "my_database";

console.log("Connecting to InfluxDB...");
const influxWriteApi = new InfluxDB({url, token}).getWriteApi(org, bucket, 'ns');
console.log("Connected to InfluxDB.");

console.log("Init: Starting to poll with poll interval (seconds)=" + POLL_INTERVAL_SECONDS + "...");
retrieveAndSaveValues();
setInterval(function() {
    retrieveAndSaveValues();
}, POLL_INTERVAL_SECONDS * 1000); 



function retrieveAndSaveValues() {
    const client = new Client();
    console.log("Searching for devices...");
    client.startDiscovery().on("device-new", (device) => {
        client.stopDiscovery();
        console.log("Found device. Retrieving value...");
        device.emeter.getRealtime().then(realtimeValues => saveValues(realtimeValues));
    });
}

function saveValues(realtimeValues) {
    console.log("Saving values in InfluxDB: " + JSON.stringify(realtimeValues)); 

    // Which fields should be stored in the DB?
    // Example: {"voltage_mv":233596,"current_ma":582,"power_mw":84007,"total_wh":7109,"err_code":0,"current":0.582,"power":84.007,"total":7.109,"voltage":233.596}
    const valueNames = ["current", "voltage", "power", "total_wh"];
    
    const deviceName = "HS110 Plug under desk (router)";
    const point = new Point(deviceName);
        
    valueNames.forEach(valueName => {
        const value = realtimeValues[valueName];
        console.log("Saving value in InfluxDB: " + valueName + "=" + value);
        point.floatField(valueName, value);
    });
    influxWriteApi.writePoint(point);
    influxWriteApi.flush();
}

 