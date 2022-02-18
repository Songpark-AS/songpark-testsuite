import argparse
import subprocess
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument(
    "timeout",
    metavar="TIMEOUT",
    type=int,
    help="the time for the test",
)
parser.add_argument(
    "test_name",
    metavar="TEST NAME",
    type=int,
    help="the name of the wireshark file to be saved",
)
args = parser.parse_args()

process = subprocess.Popen(
    ["tshark", "-i", "eth1", "-w", args.test_name],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
print(process)
sleep(args.timeout)
process.kill()
