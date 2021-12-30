const { Client } = require('tplink-smarthome-api');
const {InfluxDB, Point} = require('@influxdata/influxdb-client');

const POLL_INTERVAL_SECONDS = 60; // How often to poll for values
const CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS = 1; // Per iteration: How long should we seach (=discovery) per polling iteration?
const url = "http://localhost:8086";
const token = "my-token"; 
const org = "my-org";
const bucket = "my_database";

console.log("Connecting to InfluxDB...");
const influxWriteApi = new InfluxDB({url, token}).getWriteApi(org, bucket, 'ns');
console.log("Connected to InfluxDB.");

console.log("Init: Starting to poll with poll interval=" + POLL_INTERVAL_SECONDS + "s...");

retrieveAndSaveValues();
setInterval(function() {
    retrieveAndSaveValues();
}, POLL_INTERVAL_SECONDS * 1000); 


function retrieveAndSaveValues() {
    const client = new Client();
    
    client.startDiscovery().on("device-new", (device) => {
        const deviceName = device._sysInfo.alias;
        console.log("Found device: '" + deviceName + "'");
        device.emeter.getRealtime().then(realtimeValues => saveValues(deviceName, realtimeValues));
    });
    // Give this iteration time to find all devices
    setTimeout(function() {
        console.log("Stopping discovery of new devices for this polling iteration (waited " + CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS + "s).");
        client.stopDiscovery();
    }, CLIENT_STOP_DISCOVERY_PER_POLLING_ITERATION_SECONDS * 1000);
}

function saveValues(deviceName, realtimeValues) {
    console.log("Found values for device='" + deviceName + "' in InfluxDB: " + JSON.stringify(realtimeValues)); 

    // Which fields should be stored in the DB?
    // Example: {"voltage_mv":233596,"current_ma":582,"power_mw":84007,"total_wh":7109,"err_code":0,"current":0.582,"power":84.007,"total":7.109,"voltage":233.596}
    const valueNames = ["current", "voltage", "power", "total_wh"];
    
    const point = new Point(deviceName);
        
    valueNames.forEach(valueName => {
        const value = realtimeValues[valueName];
        console.log("Saving value for device='" + deviceName + "' in InfluxDB: " + valueName + "=" + value);
        point.floatField(valueName, value);
    });
    influxWriteApi.writePoint(point);
    influxWriteApi.flush();
}

 