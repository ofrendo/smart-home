import HomematicRetriever
import DBManager
from util.Logger import logging
import time

POLL_INTERVAL_SECONDS = 450

if __name__ == "__main__":
    logging.info(f"Starting to poll with poll interval={POLL_INTERVAL_SECONDS} seconds...")

    while True: 
        try:
            payloads = HomematicRetriever.retrieveAllDevices()
            for payload in payloads: 
                DBManager.saveToInfluxDB(payload)

            logging.info("Saved " + str(len(payloads)) + " payloads.")
        except BaseException as error:
            logging.error("Error while trying to retrieve or save data", exc_info=error)

        logging.info(f"Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
        time.sleep(POLL_INTERVAL_SECONDS)
