import asyncio
import argparse
import os
from script import start_script, OUTPUT_PATH

parser = argparse.ArgumentParser(description="Interval argument parser")
parser.add_argument("--interval", type=int, required=False,
                    help="Provide number of seconds between each requests interval, 5 by default",
                    default=0)
args = parser.parse_args()

if __name__ == '__main__':

    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    asyncio.run(start_script(args.interval))
