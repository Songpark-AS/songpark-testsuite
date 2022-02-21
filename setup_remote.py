import configparser
import sys
import os
import paramiko
import threading
import logging
import time

cfg = configparser.ConfigParser()
cfg.read("test.ini")


def main():
    print(os.name)


def setup(host, device):
    """Setups specified zedboard"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if device == "zed":
            client.connect(
                host,
                username="root",
                password=cfg.get("base", "PASSWORD"),
                key_filename=cfg.get("base", "SSH_KEY"),
            )
        else:
            client.connect(
                host,
                username="pi",
                password="raspberry",
            )

        sftp = client.open_sftp()
        sftp.put("requirements.txt", "/tmp/requirements.txt")
        sftp.close()

        stdout = client.exec_command("pip3 install -r /tmp/requiremnts.txt")[1]
        client.exec_command("rm -rf /tmp/requirements.txt")
        for line in stdout:
            logging.info(line)
        client.close()
        sys.exit(0)
    except IndexError:
        print("error")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("SONG-TST: Setting two Zedboards")
    z_alpha = threading.Thread(target=setup, args=(cfg.get("base", "Z_ALPHA"), "zed"))
    z_omega = threading.Thread(target=setup, args=(cfg.get("base", "Z_ALPHA"), "zed"))
    logging.info("SONG-TST: Setting two Raspberry Pis")
    r_alpha = threading.Thread(target=setup, args=(cfg.get("base", "R_ALPHA"), "pi"))
    r_omega = threading.Thread(target=setup, args=(cfg.get("base", "R_OMEGA"), "pi"))

    z_alpha.start()
    z_omega.start()
    r_alpha.start()
    r_omega.start()

    main()
