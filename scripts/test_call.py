import logging
from time import sleep
import serial
import os

# from AudioTestLibrary import TARGET_DEVICE

SERVICE_NAME = "sp-bridgeprogram"
TARGET_DEVICE = b"sip:9106@voip1.inonit.no \n"
ser = serial.Serial("/tmp/ttyTPX")

logger = logging.getLogger("SONGPARK")


def check_service_status(service_name):
    stat = os.system("service {} status".format(service_name))
    return True if stat == 0 else False


def start_call():
    # if check_service_status(SERVICE_NAME):
    logger.info("STARTING TO MAKE CALL")
    ser.write(b"m \n")
    sleep(2)
    ser.write(TARGET_DEVICE)
    logger.info("CALL HAS BEEN STARTED")
    # logger.error("TPX SERIAL PORT SERVICE IS NOT RUNNING")


if __name__ == "__main__":
    print("STARTING CALL")
    start_call()
    print("CALL STARTED")
    sleep(60)
    ser.write(b"ha \n")
    print("CALL ENDED AFTER 60 seconds")
    ser.close()
