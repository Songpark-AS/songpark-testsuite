import configparser
import sys
import os
import paramiko
import logging
import threading
import time

cfg = configparser.ConfigParser()
cfg.read("test.ini")


def main():
    print(os.name)


def start_zed_test(host):
    """Setups a client and runs a test on the specified zedboard"""
    try:
        print("I AM STARTING THIS")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            host,
            username="root",
            password=cfg.get("test", "PASSWORD"),
            key_filename=cfg.get("test", "SSH_KEY"),
        )
        sftp = client.open_sftp()
        sftp.put("scripts/test_call.py", "/tmp/test_call.py")
        sftp.close()
        sip_id = cfg.get("test", "SIP_ID")
        timeout = cfg.get("test", "TEST_RUNTIME")
        cmd = f"python3 /tmp/test_call.py {sip_id} {timeout}"
        _, stdout, _ = client.exec_command(
            f"python3 /tmp/test_call.py {sip_id} {timeout}"
        )[1]
        for line in stdout:
            print(line)
        client.close()
        sys.exit(0)
    except IndexError:
        print("error")


def start_pi_test(host, mode):
    """Setups a client and runs a test on the specified Raspberry pi"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            host,
            username="pi",
            password="raspberry",
        )

        sftp = client.open_sftp()
        if mode == "generate":
            sftp.put("scripts/generate_audio.py", "/tmp/generate_audio.py")
            stdout = client.exec_command("python3 /tmp/generate_audio.py")[1]
            print(stdout.readlines())
            time.sleep(int(cfg.get("test", "TEST_RUNTIME")))
            _, stdout2, _ = client.exec_command("\x03")
            print(stdout2.readlines())
            client.close()
            sys.exit(0)
        else:
            print("RECORDING AUDIO")
            sftp.put("scripts/record_audio.py", "/tmp/record_audio.py")
            sftp.put("scripts/upload.py", "/tmp/upload.py")
            stdout = client.exec_command("python3 /tmp/record_audio.py")[1]
            print(stdout.readlines())
            time.sleep(int(cfg.get("test", "TEST_RUNTIME")))
            _, stdout2, _ = client.exec_command("\x03")
            print(stdout2.readlines())
            client.close()
            sys.exit(0)
        # for line in stdout:
        #     print(line)

    except IndexError:
        print("error")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("SONG-TST: Starting a call on %s", cfg.get("test", "Z_ALPHA"))
    z_alpha = threading.Thread(
        target=start_zed_test, args=(cfg.get("test", "Z_ALPHA"),)
    )
    logging.info("SONG-TST: Starting a recording on %s", cfg.get("test", "R_OMEGA"))
    r_omega = threading.Thread(
        target=start_pi_test, args=(cfg.get("test", "R_OMEGA"), "record")
    )
    logging.info("SONG-TST: Starting a signal on %s", cfg.get("test", "R_ALPHA"))
    r_alpha = threading.Thread(
        target=start_pi_test, args=(cfg.get("test", "R_ALPHA"), "generate")
    )
    r_omega.start()
    r_alpha.start()
    z_alpha.start()
    main()
