import logging
from time import sleep
import serial
import os
import sys

# from AudioTestLibrary import TARGET_DEVICE

SERVICE_NAME = "sp-bridgeprogram"
ser = serial.Serial("/tmp/ttyTPX")

logger = logging.getLogger("SONGPARK")


def command(cmd):
    cmd_str = cmd + " \n"
    return bytes(cmd_str, "UTF-8")


def check_service_status(service_name):
    stat = os.system("service {} status".format(service_name))
    return True if stat == 0 else False


def start_call(target):
    # if check_service_status(SERVICE_NAME):
    logger.info("STARTING TO MAKE CALL")
    ser.write(command("m"))
    sleep(2)
    ser.write(command(target))
    logger.info("CALL HAS BEEN STARTED")
    # logger.error("TPX SERIAL PORT SERVICE IS NOT RUNNING")


if __name__ == "__main__":
    target_device = sys.argv[1]
    print("STARTING CALL")
    start_call(target_device)
    print("CALL STARTED")
    sleep(int(sys.argv[2]))
    ser.write(command("ha"))
    print("CALL ENDED AFTER 60 seconds")
    ser.close()
