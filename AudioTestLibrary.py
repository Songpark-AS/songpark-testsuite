import logging
from time import sleep
import serial
import os
from robotremoteserver import RobotRemoteServer

from audio_analysis import generate_audio, record_audio

logger = logging.getLogger("SONGPARK")

TP_BP = ""
BP_TO = ""
TARGET_DEVICE = b""
SERVICE_NAME = ""

upoad_url = ""


class AudioTestLibrary(object):
    def __init__(self):
        self.ser = serial.Serial(TP_BP)

    def check_service_status(self, service_name):
        stat = os.system(f"service {service_name} status")
        return True if stat == 0 else False

    def start_call(self):
        if self.check_service_status(SERVICE_NAME):
            self.ser.write(b"m")
            sleep(3)
            self.ser.write(TARGET_DEVICE)
        logger.error("SERVICES ARE NOT RUNNING")

    def generate_audio(self):
        generate_audio.start_audio_generation()

    def record_audio(self):
        record_audio.start_recording()

    def upload_audio(self):
        pass

    def stop_call(self):
        self.ser.write(b"ha")


if __name__ == "__main__":
    RobotRemoteServer(AudioTestLibrary())
