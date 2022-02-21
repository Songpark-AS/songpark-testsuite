import argparse
import subprocess
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument(
    "device", metavar="DEVICE IP", type=str, help="IP for device to call"
)

parser.add_argument(
    "name",
    metavar="NAME",
    type=str,
    help="The device name either beatles or elvis for now",
)

parser.add_argument(
    "timeout", metavar="TIMEOUT", type=str, help="Timeout duration for the call"
)

args = parser.parse_args()


def run_beatles():
    print("Starting connect_nosip_2022-02-10")
    process = subprocess.Popen(
        ["connect_nosip_2022-02-10", args.device, "4000", "4001"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    sleep(10)
    process.stdin.write("sync")
    sleep(2)
    process.stdin.write("start")
    sleep(args.timeout)
    process.kill()


def run_elvis():
    print("Starting connect_nosip_2022-02-10")
    process = subprocess.Popen(
        ["connect_nosip_2022-02-10", args.device, "4000", "4001"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    sleep(12)
    process.stdin.write("start")
    sleep(args.timeout)
    process.kill()


if __name__ == "__main__":
    if args.name == "elvis":
        run_elvis()
    else:
        run_beatles()
    print(f"RAN A CALL ON DEVICE {args.name} for {args.timeout} seconds")
