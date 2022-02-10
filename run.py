import argparse
import configparser
import sys
import os
import paramiko
import logging
import threading
import time

cfg = configparser.ConfigParser()
cfg.read("test.ini")

parser = argparse.ArgumentParser()
parser.add_argument(
    "test_name",
    metavar="TEST NAME",
    type=str,
    help="the name to be used for the test e.g 'test_1'",
)
args = parser.parse_args()


def main():
    print(os.name)


def start_zed_test(host):
    """Setups a client and runs a test on the specified zedboard"""
    try:
        print("STARTING CALL")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            host,
            username="root",
            password=cfg.get("base", "PASSPHRASE"),
            key_filename=cfg.get("base", "SSH_KEY"),
        )
        sftp = client.open_sftp()
        sftp.put("scripts/test_call.py", "/tmp/test_call.py")
        sftp.close()
        sip_id = cfg.get("base", "SIP_ID")
        timeout = cfg.get("test1", "TEST_RUNTIME")
        _, stdout, _ = client.exec_command(
            f"python3 /tmp/test_call.py {sip_id} {timeout}"
        )[1]
        print(stdout)
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
        test_runtime = int(cfg.get("test1", "TEST_RUNTIME"))
        if mode == "generate":
            print("GENERATING AUDIO")
            sftp.put("scripts/generate_audio.py", "/tmp/generate_audio.py")
            stdout = client.exec_command(
                f"python3 /tmp/generate_audio.py {test_runtime}"
            )[1]
            print(stdout.readlines())
            client.close()
            sys.exit(0)
        else:
            print("RECORDING AUDIO")
            sftp.put("scripts/record_audio.py", "/tmp/record_audio.py")
            sftp.put("scripts/upload.py", "/tmp/upload.py")
            sftp.put(cfg.get("base", "STORAGE_KEY"), "/tmp/ubuntu-rsync-server.pem")
            stdout = client.exec_command(
                f"python3 /tmp/record_audio.py {test_runtime} {args.test_name}.wav"
            )[1]
            print(stdout.readlines())
            print("UPLOADING AUDIO FILE")
            target_name = f"/tmp/{args.test_name}.wav"
            client.exec_command(
                f"python3 /tmp/upload.py {cfg.get('base', 'STORAGE_HOST')} {cfg.get('base', 'SG_HOST_USER')} {cfg.get('base', 'PASSPHRASE')} /tmp/ubuntu-rsync-server.pem {args.test_name}.wav {target_name}"
            )
            print("UPLOADING SUCCESSFUL")
            client.close()
            sys.exit(0)

    except IndexError:
        print("error")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info(f"SONG_TST: Starting {args.test_name}")

    logging.info("SONG-TST: Starting a call on %s", cfg.get("base", "Z_ALPHA"))
    z_alpha = threading.Thread(
        target=start_zed_test, args=(cfg.get("base", "Z_ALPHA"),)
    )
    logging.info("SONG-TST: Starting a recording on %s", cfg.get("base", "R_OMEGA"))
    r_omega = threading.Thread(
        target=start_pi_test, args=(cfg.get("base", "R_OMEGA"), "record")
    )
    logging.info("SONG-TST: Starting a signal on %s", cfg.get("base", "R_ALPHA"))
    r_alpha = threading.Thread(
        target=start_pi_test, args=(cfg.get("base", "R_ALPHA"), "generate")
    )
    r_omega.start()
    r_alpha.start()
    z_alpha.start()
    main()
