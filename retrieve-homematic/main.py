import HomematicRetriever
import DBManager
import time
from util.Logger import logging

POLL_INTERVAL_SECONDS = 60

if __name__ == "__main__":
    logging.info("Starting to poll...")

    while True: 
        payloads = HomematicRetriever.retrieveAllDevices()
        
        for payload in payloads: 
            DBManager.saveToInfluxDB(payload)
        
        logging.info("Saved " + str(len(payloads)) + " payloads.")
        
        time.sleep(POLL_INTERVAL_SECONDS)
