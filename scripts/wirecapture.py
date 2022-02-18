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
args = parser.parse_args()

process = subprocess.Popen(
    ["tshark", "-i", "eth1", "-w", "wsharkcapture-test"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
print(process)
sleep(args.timeout)
process.kill()
