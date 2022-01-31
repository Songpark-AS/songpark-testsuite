import configparser
import sys
import os
import paramiko
import shutil

cfg = configparser.ConfigParser()
cfg.read("test.ini")


def main():
    print(os.name)


def start_zed_test(host, user):
    """Setups a client and runs a test on the specified zedboard"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            cfg.get("test", host),
            username=user,
            password=cfg.get("test", "PASSWORD"),
            key_filename=cfg.get("test", "SSH_KEY"),
        )
        sftp = client.open_sftp()
        sftp.put("test_call.py", "/tmp/test_call.py")
        sftp.close()

        stdout = client.exec_command("python3 /tmp/test_call")[1]
        for line in stdout:
            print(line)
        client.close()
        sys.exit(0)
    except IndexError:
        print("error")


def start_pi_test(host, user):
    """Setups a client and runs a test on the specified Raspberry pi"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            cfg.get("test", host),
            username=user,
            password="raspberry",
        )
        sftp = client.open_sftp()
        for _, _, file_names in os.walk("audio_analysis/"):
            pass

        stdout = client.exec_command(f"python3 /tmp/{script}")[1]
        for line in stdout:
            print(line)
        client.close()
        sys.exit(0)
    except IndexError:
        print("error")


if __name__ == "__main__":
    shutil.make_archive("pi", "zip", "audio_analysis/")
    # start_test("Z_ALPHA", "root")

    main()
