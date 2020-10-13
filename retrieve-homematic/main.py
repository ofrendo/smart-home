import HomematicRetriever
import DBManager
import time

POLL_INTERVAL_SECONDS = 60


if __name__ == "__main__":
    print("Starting to poll...")

    while True: 

        payloads = HomematicRetriever.retrieveAllDevices()
        for payload in payloads: 
            DBManager.saveToInfluxDB(payload)

        print("Saved " + str(len(payloads)) + " payloads.")

        break
        time.sleep(POLL_INTERVAL_SECONDS)
