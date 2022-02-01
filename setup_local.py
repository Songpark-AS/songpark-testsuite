from genericpath import exists
import os
import shutil
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
if not exists("test.ini"):
    logging.info("CREATING test.ini file")
    shutil.copyfile("app.ini", "test.ini")
print("********************FILE EXISTS**********************")
