import HomematicRetriever
import DBManager
import time
from util.Logger import logging

POLL_INTERVAL_SECONDS = 450

if __name__ == "__main__":
    logging.info("Starting to poll with poll interval=" + str(POLL_INTERVAL_SECONDS) + " seconds...")

    while True: 
        
        try:
            payloads = HomematicRetriever.retrieveAllDevices()
        
            for payload in payloads: 
                DBManager.saveToInfluxDB(payload)
        
            logging.info("Saved " + str(len(payloads)) + " payloads.")
        except BaseException as error:
            logging.error("Error while trying to retrieve or save data", exc_info=error)

        time.sleep(POLL_INTERVAL_SECONDS)
