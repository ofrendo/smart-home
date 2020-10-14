# smart-home

## Overall setup
Download InfluxDB (1.8.3): https://portal.influxdata.com/downloads/

Make sure InfluxDB is running and the database is created:

### Windows
```
sudo influxd 

influx
> create database my_database
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
``` 


## Retrieve thermostat values

### Setup

Documentation: https://github.com/coreGreenberet/homematicip-rest-api

```
pip3 install -r retrieve-homematic/requirements.txt
python3 retrieve-homematic/hmip_generate_auth_token.py
```





