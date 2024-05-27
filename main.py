import asyncio
import argparse
import os
from source.script import start_script, OUTPUT_PATH, logging

parser = argparse.ArgumentParser(description="Interval argument parser")
parser.add_argument("--interval", type=int, required=False,
                    help="Provide number of seconds between each requests interval, 5 by default",
                    default=5)
args = parser.parse_args()

if __name__ == '__main__':

    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    try:
        asyncio.run(start_script(args.interval))
    except Exception as e:
        logging.info("Script work failed")
        logging.error(e)
