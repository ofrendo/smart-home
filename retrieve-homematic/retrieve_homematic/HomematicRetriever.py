# Source: https://github.com/coreGreenberet/homematicip-samples/blob/master/GetDevicesAndValues/api_with_url.py

import requests
import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContactMagnetic, HeatingThermostat, WindowState, ValveState
from util.Logger import logging



config = homematicip.find_and_load_config_file()

home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)
    
def setPayloadFields(payload, device, fields: [str]): 
    for field in fields: 
        value = getattr(device, field)
        if isinstance(value, WindowState) or isinstance(value, ValveState):
            value = value.value

        payload[field] = value

def getInitialPayload(room: str, device):
    """
    all devices data structure: 
        label                   String
        lastStatusUpdate        Datetime (NOTE: Returns time in local time zone!)
        lowBat                  Boolean
        unreach                 Boolean
        rssiDeviceValue         Integer
        rssiPeerValue           Integer
        configPending           Boolean
        dutyCycle               Boolean
    """
    
    payload = {"room": room}
    defaultFields = ["label", "lastStatusUpdate", "lowBat", "unreach", "rssiDeviceValue", "rssiPeerValue", "configPending", "dutyCycle"]
    setPayloadFields(payload, device, defaultFields)
    return payload

def getPayload(room: str, device, deviceSpecificFields: [str]):
    payload = getInitialPayload(room, device)
    setPayloadFields(payload, device, deviceSpecificFields)
    return payload

def retrieveShutterContactMagnetic(room: str, device: ShutterContactMagnetic):
    """
    Example:
    device data structure: 
        windowState             Enum / String
    """   
    fields = ["windowState"]
    payload = getPayload(room, device, fields)
    return payload

def retrieveHeatingThermostat(room, device: HeatingThermostat):
    """
    device data structure
        operationLockActive     Boolean
        valvePosition           Double
        valveState              Enum / String
        temperatureOffset       Double
        setPointTemperature     Double
        valveActualTemperature  Double
    """
    fields = ["operationLockActive", "valvePosition", "valveState", "temperatureOffset", "setPointTemperature", "valveActualTemperature"]
    payload = getPayload(room, device, fields)
    return payload
	
def retrieveAllDevices():
    resultPayloads = []

    global home
    home.get_current_state()
    for group in home.groups:
        if group.groupType=="META":
            for device in group.devices:
                if isinstance(device, HeatingThermostat):
                    resultPayloads.append(retrieveHeatingThermostat(group.label, device))
                elif isinstance(device, ShutterContactMagnetic): 
                    resultPayloads.append(retrieveShutterContactMagnetic(group.label, device))
                else:
                    print("Found unknown device: ", device, " (class=", type(device), ")")

    return resultPayloads



if __name__ == "__main__":
    logging.info("Retrieving single payloads:")
    payloads = retrieveAllDevices()
    for payload in payloads: 
        logging.info(payload)