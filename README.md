# smart-home
- [smart-home](#smart-home)
  - [Overall setup](#overall-setup)
    - [Windows](#windows)
    - [Raspberry Pi](#raspberry-pi)
  - [Retrieve thermostat values](#retrieve-thermostat-values)
    - [Setup](#setup)
    - [Start polling values (CLI)](#start-polling-values-cli)
    - [Start polling values (PM2)](#start-polling-values-pm2)
  - [Retrieve power (HS110 or KP115 smart plug)](#retrieve-power-hs110-or-kp115-smart-plug)
    - [Start polling values (CLI)](#start-polling-values-cli-1)
    - [Start polling values (PM2)](#start-polling-values-pm2-1)
  - [Retrieve power (Shelly Plug S)](#retrieve-power-shelly-plug-s)
    - [Configuring the Shelly Plug S](#configuring-the-shelly-plug-s)
    - [Starting the Python Shelly Plug S retriever (for debugging)](#starting-the-python-shelly-plug-s-retriever-for-debugging)
    - [Starting the Python Shelly Plug S retriever (PM2)](#starting-the-python-shelly-plug-s-retriever-pm2)
  - [Retrieve temperature (Shelly H\&T)](#retrieve-temperature-shelly-ht)
    - [Configuring the MQTT server on the Raspberry Pi](#configuring-the-mqtt-server-on-the-raspberry-pi)
    - [Starting the Python MQTT subscriber (PM2)](#starting-the-python-mqtt-subscriber-pm2)
    - [Configuring the Shelly sensor](#configuring-the-shelly-sensor)
    - [Sending a test MQTT message](#sending-a-test-mqtt-message)
    - [Sample MQTT messages from Shelly](#sample-mqtt-messages-from-shelly)

## Overall setup
Download InfluxDB (1.8.3): https://portal.influxdata.com/downloads/

Make sure InfluxDB is running and the database is created:

### Windows 
```
sudo influxd 

influx
> create database my_database
> SHOW DATABASES
> use my_database

> show series
=======
> create database test_database
```

Check if values exist: 
```
influx
> use my_database
> show measurements
```

### Raspberry Pi 
See Debian under https://docs.influxdata.com/influxdb/v1.8/introduction/install/

```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install influxdb
sudo service influxdb start

influx
> create database my_database
> create database test_database
``` 

Download Grafana
```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update && sudo apt-get install -y grafana

sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
```


Download PM2 (https://www.npmjs.com/package/pm2) and follow instructions! 
```
sudo npm install pm2 -g
pm2 startup
```


Download and compile Python3.8, depending on RPI version: https://maker-tutorials.com/python3-pip-raspberry-pi-installieren/



## Retrieve thermostat values

### Setup

Documentation: https://github.com/hahn-th/homematicip-rest-api

Run the following code to generate `retrieve-homematic/config.ini` containing credentials.
- To find SGTIN: Open HomematicIP app -> More -> Device Overview -> Access Point -> Info (top right)
- client/devicename: Leave blank
- PIN: Leave blank

```
cd retrieve-homematic
poetry install
poetry run python3 retrieve_homematic/hmip_generate_auth_token.py
```

Debugging:
```
poetry run python3 retrieve_homematic/hmip_cli.py --help
```

### Start polling values (CLI)


Start the Python process: 
``` 
cd retrieve-homematic
poetry run python3 retrieve_homematic/main.py
``` 

### Start polling values (PM2)
Start the Python process permanently (so that it starts even after reboot): 
```
cd retrieve-homematic
pm2 start retrieve_homematic/main.py --interpreter .venv/bin/python --name retrieve-homematic
pm2 save
```


## Retrieve power (HS110 or KP115 smart plug)

API documentation: https://plasticrake.github.io/tplink-smarthome-api/


### Start polling values (CLI)
Start the JavaScript process:

```
cd retrieve-tplink-hs110
node main.js
```

### Start polling values (PM2)

Start the process permanently (so that it starts even after reboot): 
```
cd retrieve-tplink-hs110
pm2 start main.js --name "retrieve-tplink-hs110"
pm2 save
```


## Retrieve power (Shelly Plug S)
This is a separate step because Shelly Plug S supports MQTT only when the cloud connection is disabled. However, the cloud connection
is a useful feature because a weekly schedule can be set via cloud connection (Shelly app).

### Configuring the Shelly Plug S
- Settings --> Power on default mode --> "ON"


### Starting the Python Shelly Plug S retriever (for debugging)
```
cd retrieve-shelly
poetry install
poetry run python3 retrieve_shelly/main_shelly_plug_retriever.py
```


### Starting the Python Shelly Plug S retriever (PM2)

Start the Python process permanently (so that it starts even after reboot): 
```
cd retrieve-shelly
poetry install
pm2 start retrieve_shelly/main_shelly_plug_retriever.py --interpreter .venv/bin/python --name retrieve-shelly-plug
pm2 save
```


## Retrieve temperature (Shelly H&T)
This step uses MQTT.

### Configuring the MQTT server on the Raspberry Pi
Guide: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

```
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```

### Starting the Python MQTT subscriber (PM2)

Start the Python process permanently (so that it starts even after reboot): 
```
cd retrieve-shelly
poetry install
pm2 start retrieve_shelly/main_shelly_mqtt.py --interpreter .venv/bin/python --name retrieve-shelly-ht
pm2 save
```


### Configuring the Shelly sensor

- Turn on the Shelly sensor: The LED should be on (not blinking)
- Get the IP address of the sensor via the Shelly App
- Connect to the sensor via browser
- Click on "Internet & Security" -> "Advanced - Developer Settings"
- Click on "Enable MQTT"
- Enter IP address of Raspberry PI
- Click "Save"


### Sending a test MQTT message
```
mosquitto_pub -t "shellies/shellyht-70/sensor/temperature" -m 50 -h localhost -p 1883
```

### Sample MQTT messages from Shelly

```
shellies/shellyht-123456/online true
shellies/announce {"id":"shellyht-123456","model":"SHHT-1","mac":"123456789","ip":"192.168.0.123","new_fw":false,"fw_ver":"20210710-130145/v1.11.0-g12a9327-master"}
shellies/shellyht-123456/announce {"id":"shellyht-123456","model":"SHHT-1","mac":"123456789","ip":"192.168.0.123","new_fw":false,"fw_ver":"20210710-130145/v1.11.0-g12a9327-master"}
shellies/shellyht-123456/sensor/temperature 29.62
shellies/shellyht-123456/sensor/humidity 40.5
shellies/shellyht-123456/sensor/battery 100
```


