from websocket import create_connection
from blockchain import blockexplorer
import time
from datetime import datetime
import json
import numpy as np
from collections import deque
import sys, getopt

ws = create_connection("wss://ws.blockchain.info/inv")
ws.send("""{"op":"blocks_sub"}""")

def time_format(t):
    return datetime.fromtimestamp(t).strftime("%H:%M:%S")

#
#    A timestamp is accepted as valid if it is greater than the median timestamp
#    of previous 11 blocks, and less than the network-adjusted time + 2 hours.
#    "Network-adjusted time" is the median of the timestamps returned by all
#    nodes connected to you.
#

def get_timestamps():
    ms = int(round(time.time()*1000))
    result = [i.time for i in blockexplorer.get_blocks(time=ms)]
    return result[:11] if result else result[0][:11]


def fork_watcher(hard_fork_time):
    latest_blocks_time = deque(get_timestamps())
    while True:
        if len(latest_blocks_time) == 11 :
            median = int(round(np.median(latest_blocks_time)))
            if median >= hard_fork_time:
                print("That's all")
                print("Median time: %s \nHard Fork Time: %s" % (time_format(median),
                    time_format(hard_fork_time)))
                print("Median timestamp: %s \nHard Fork Timestamp: %s" % (median,
                    hard_fork_time))
                return True
            else:
                diff = abs(datetime.fromtimestamp(hard_fork_time) - \
                   datetime.fromtimestamp(median))
                print("Timedelta: %s" % diff)
                return False
        else:
            print("Len %d" % len(t))
                tx = ws.recv()
                data = json.loads(tx)
                print(data['x']['hash'])
                print(data['x']['time'])
                latest_blocks_time.pop()
                latest_blocks_time.appendleft(data['x']['time'])


def main():
    options, arg = getopt.getopt(sys.argv[1:], 'p:', 'params=')
    for opt, arg in options:
        if opt in ('-p', '--params'):
            fork_watcher(int(arg))
    ws.close()


if __name__== "__main__":
    main()
