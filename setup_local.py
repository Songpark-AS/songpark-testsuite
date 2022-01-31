from genericpath import exists
import os
import shutil

if not exists("test.ini"):
    shutil.copyfile("app.ini", "test.ini")
print("********************FILE EXISTS**********************")
