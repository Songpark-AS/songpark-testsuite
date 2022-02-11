import paramiko
import os


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
        raise Exception("SOMETHING HAPPENED COUILD NOT CREATE CLIENT")


def test_on_lab(beatles, elvis, elvis_pi, test_name, run_time, cfg, key, key_pass):
    print("CREATING BEATLES CLIENT")
    beatles = create_client(beatles, key, key_pass, "z")
    print("CREATING ELVIS CLIENT")
    elvis = create_client(elvis, key, key_pass, "z")
    print("CREATING ELVIS PI CLIENT")
    elvis_pi = create_client(elvis_pi)

    print("starting connect on beatles ")
    beatles.exec_command("connect_manual_2022-01-25   10.1.1.102 2000 2001")
    print("starting connect on elvis")
    elvis.exec_command("connect_manual_2022-01-25 10.1.1.100 2000 2001")

    beatles.exec_command("sync")
    beatles.exec_command("start")
    elvis.exec_command("start")

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
    elvis_pi.exec_command(
        f"python3 /tmp/upload.py {cfg.get('base', 'STORAGE_HOST')} {cfg.get('base', 'SG_HOST_USER')} {cfg.get('base', 'PASSPHRASE')} /tmp/ubuntu-rsync-server.pem {test_name}.wav {target_name}"
    )
    print("UPLOADING SUCCESSFUL")
    elvis_pi.close()

    beatles.exec_command("ha")

    beatles.close()
    elvis.close()
