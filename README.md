# smart-home

## Overall setup
Download InfluxDB (1.8.3): https://portal.influxdata.com/downloads/

Make sure InfluxDB is running and the database is created:

### Windows 
```
sudo influxd 

influx
> create database my_database
> create database test_database
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

## Retrieve thermostat values

### Setup

Documentation: https://github.com/coreGreenberet/homematicip-rest-api

```
pip3 install -r retrieve-homematic/requirements.txt
python3 retrieve-homematic/hmip_generate_auth_token.py
```

### Start polling values (CLI)

Start the Python process: 

``` 
cd retrieve-homematic
python3 main.py
``` 

### Start polling values (PM2)
Start the Python process permanently (so that it starts even after reboot): 
```
cd retrieve-homematic
pm2 start main.py --interpreter python3
pm2 save
```








