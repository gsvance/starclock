# Module that handles the console-based StarClock.
# Prepares and updates the console.

import sys

def initialize():
    # Clears space in the terminal to prepare for the clock
    print "StarClock (CTRL-C to exit)"
    sys.stdout.write("\n" * 4)
    sys.stdout.flush()

def update(time_dict):
    # Displays times from time_dict in the terminal space
    sys.stdout.write("\x1b[A" * 4)
    print time_dict["lt"] + "\n" + time_dict["utc"] + "\n" + \
    time_dict["jd"] + "\n" + time_dict["lst"]
    sys.stdout.flush()
