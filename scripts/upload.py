import argparse
import paramiko

parser = argparse.ArgumentParser()
parser.add_argument(
    "hostname", metavar="HOSTNAME", type=str, help="upload server hostname"
)
parser.add_argument(
    "username", metavar="USERNAME", type=str, help="upload server username"
)
parser.add_argument(
    "passphrase", metavar="PASSPHRASE", type=str, help="public key passphrase"
)
parser.add_argument(
    "key", metavar="PUBLIC KEY", type=str, help="ssh public key file path"
)
parser.add_argument("filename", metavar="FILENAME", type=str, help="source file path")
parser.add_argument(
    "target_name", metavar="TARGET PATH", type=str, help="destination path"
)

args = parser.parse_args()


def upload_file(host, user, passphrase, key_file, filename, target_name):
    try:
        print("UPLOADING FILE: {0} TO {1}!".format(filename, host))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=host, username=user, password=passphrase, key_filename=key_file
        )

        sftp = client.open_sftp()
        sftp.put(filename, target_name)
        sftp.close()
        print(
            "{0} UPLOADED SUCCESSFULLY TO {1} on {2}!".format(
                filename, target_name, host
            )
        )
        client.close()
    except:
        print("UPLOAD FAILED SOMETHING HAPPENED CHECK UPLOAD DESTINATION")


if __name__ == "__main__":
    upload_file(
        args.hostname,
        args.username,
        args.passphrase,
        args.key,
        args.filename,
        args.target_name,
    )
