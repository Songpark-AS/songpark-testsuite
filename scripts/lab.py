from time import sleep
import paramiko
import os
import threading


def create_client(host, key="", passphrase="", device="pi"):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if device == "pi":
            client.connect(
                host,
                username="pi",
                password="raspberry",
            )
        else:
            client.connect(
                host,
                username="root",
                password=passphrase,
                key_filename=key,
            )
        return client
    except:
        raise Exception(f"SOMETHING HAPPENED COULD NOT CREATE {host} CLIENT")


def run_on_zed(host, name, target, key, key_pass, run_time):
    print(f"CREATING {name} CLIENT")
    client = create_client(host, key, key_pass, "z")
    sftp = client.open_sftp()
    sftp.put("scripts/run_connnect.py", "/tmp/run_connect.py")
    stdout = client.exec_command(
        f"python3 /tmp/run_connect.py {target} {name} {run_time}"
    )[1]
    print(stdout.readlines())
    client.close()


def test_on_lab(beatles, elvis, elvis_pi, test_name, run_time, cfg, key, key_pass):
    beatles_t = threading.Thread(
        target=run_on_zed, args=(beatles, "beatles", elvis, key, key_pass, run_time)
    )
    elvis_t = threading.Thread(
        target=run_on_zed, args=(elvis, "elvis", beatles, key, key_pass, run_time)
    )
    print("CREATING ELVIS PI CLIENT")
    elvis_pi = create_client(elvis_pi)

    beatles_t.start()
    elvis_t.start()

    sftp = elvis_pi.open_sftp()
    print("RECORDING AUDIO")
    print(os.getcwd())
    sftp.put("scripts/record_audio.py", "/tmp/record_audio.py")
    sftp.put("scripts/upload.py", "/tmp/upload.py")
    sftp.put(cfg.get("base", "STORAGE_KEY"), "/tmp/ubuntu-rsync-server.pem")
    stdout = elvis_pi.exec_command(
        f"python3 /tmp/record_audio.py {run_time} {test_name}.wav"
    )[1]
    print(stdout.readlines())
    print("UPLOADING AUDIO FILE")
    target_name = f"/tmp/{test_name}.wav"
    stdout = elvis_pi.exec_command(
        f"python3 /tmp/upload.py {cfg.get('base', 'STORAGE_HOST')} {cfg.get('base', 'SG_HOST_USER')} {cfg.get('base', 'PASSPHRASE')} /tmp/ubuntu-rsync-server.pem {test_name}.wav {target_name}"
    )[1]
    print(stdout.readlines())
    elvis_pi.close()


def capture_wireshark(bridge, cfg, timeout, test_name):
    print("CREATING BRIDGE CLIENT")
    bridge_pi = create_client(bridge)
    sftp = bridge_pi.open_sftp()
    sftp.put("scripts/wirecapture.py", "/tmp/wirecapture.py")
    print("STARTING WIRESHARK CAPTURE")
    stdout = bridge_pi.exec_command(
        f"python3 /tmp/wirecapture.py {timeout} {test_name}"
    )[1]
    sleep(int(timeout))
    print(stdout.readlines())
    print("UPLOADING WIRESHARK FILE")
    print(
        f"python3 /tmp/upload.py {cfg.get('base', 'STORAGE_HOST')} {cfg.get('base', 'SG_HOST_USER')} {cfg.get('base', 'PASSPHRASE')} /tmp/ubuntu-rsync-server.pem wsharkcapture-test/tmp/wireshark-test"
    )
    stdout = bridge_pi.exec_command(
        f"python3 /tmp/upload.py {cfg.get('base', 'STORAGE_HOST')} {cfg.get('base', 'SG_HOST_USER')} {cfg.get('base', 'PASSPHRASE')} /tmp/ubuntu-rsync-server.pem {test_name} /tmp/{test_name}"
    )[1]
    print(stdout.readlines())
    bridge_pi.close()


def test_on_lab_wireshark(
    beatles, elvis, elvis_pi, bridge, test_name, run_time, cfg, key, key_pass
):
    try:
        bridge_thread = threading.Thread(
            target=capture_wireshark, args=(bridge, cfg, run_time, test_name)
        )
        bridge_thread.start()
        test_on_lab(beatles, elvis, elvis_pi, test_name, run_time, cfg, key, key_pass)
    except Exception as e:
        print(e)
