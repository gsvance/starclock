# Module that remembers and changes the StarClock longitude setting.

###############################################################################
# Current longitude setting:
longitude = -72.1053
# This setting is found on line
line = 4
# of this file (count starts at 0).
###############################################################################

import os

longitude_file = os.path.abspath(__file__)
# File needs to find the path to itself.
# Make sure you don't use the .pyc file!
if longitude_file[-4:] == ".pyc":
    longitude_file = longitude_file[:-1]

def config():
    # Prompts the user to edit the longitude setting
    print "Current longitude setting:", longitude
    new_longitude = float(raw_input("Enter new longitude: "))
    this_file = open(longitude_file, "r")
    l = list(this_file)
    this_file.close()
    l[line] = "longitude = " + str(new_longitude) + "\n"
    s = "".join(l)
    this_file = open(longitude_file, "w")
    this_file.write(s)
    this_file.close()
    print "Longitude was updated to %s." % (new_longitude)
