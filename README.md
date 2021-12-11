# smart-home

## Overall setup
Download InfluxDB (1.8.3): https://portal.influxdata.com/downloads/

Make sure InfluxDB is running and the database is created:
```
sudo influxd run 

influx
> create database my_database
> SHOW DATABASES
> use my_database

> show series

```


## Retrieve thermostat values

### Setup
Documentation: https://github.com/coreGreenberet/homematicip-rest-api

```
pip3 install -U homematicip 
python3 hmip_generate_auth_token.py
```


## Grafana

- Running on ip-address:3000

## Data retrieval

```
pm2 list

```





