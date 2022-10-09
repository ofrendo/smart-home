import datetime
import pytz
from util.Logger import logging


def getLocalTimezone(): 
    #localTimezone = reference.LocalTimezone()
    localTimezone = pytz.timezone("Europe/Berlin")
    return localTimezone

def convertDatetimeToUtc(datetimeParam):
    """
    https://stackoverflow.com/questions/31977563/python-how-do-you-convert-a-datetime-timestamp-from-one-timezone-to-another-tim
    """
    # create both timezone objects
    localTimezone = getLocalTimezone()
    newTimezone = pytz.timezone("UTC")

    # two-step process
    localizedTimestamp = localTimezone.localize(datetimeParam)
    newTimezoneTimestamp = localizedTimestamp.astimezone(newTimezone)

    return newTimezoneTimestamp



if __name__ == "__main__":
    currentTime = datetime.datetime.now()

    logging.info("Local timezone: " + str(getLocalTimezone()))

    currentTimeUtc = convertDatetimeToUtc(currentTime)
    logging.info(currentTimeUtc)