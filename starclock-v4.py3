#!/usr/bin/env python3

###############################################################################
# StarClock v4
#   Written by Greg Vance, Connecticut College
###############################################################################

from __future__ import print_function, division

import argparse, os, math, time, sys

try:
	import readline
except ImportError:
	pass

try:
    import graphics
except ImportError:
    raise ImportError("StarClock requires Zelle's graphics.py to run!")

###############################################################################
# Current longitude setting:
longitude = -111.9400
# This setting is found on line
longitude_line = 24 - 1
# of this file (count starts at 0).
###############################################################################
# Conn College Longitude = -72.1053
# Tempe, AZ Longitude = -111.9400
###############################################################################

info = """StarClock (v4, June 2014, now a self-contained executable)
Created by Greg Vance, Connecticut College

A simple application for observational astronomy that displays:

 - current local time
 - current universal coordinated time
 - current Julian date
 - current local sidereal time

All values are recalculated and updated continuously.

Julian date is calculated using the method found here:
   http://en.wikipedia.org/wiki/Julian_day

Local sidereal time is calculated using the approximation here:
   http://aa.usno.navy.mil/faq/docs/GAST.php

Accurate calculation of LST requires the user's longitude.
This value must be provided by the user via the -l option.

Program includes terminal and GUI display formats.

Script requires Zelle's graphics.py in order to run!"""

parser = argparse.ArgumentParser(description=info,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-g", "--gui", action="store_true", default=False,
    help="start StarClock in GUI mode (default)")
parser.add_argument("-c", "--console", action="store_true", default=False,
    help="start StarClock in console display mode, not GUI mode")
parser.add_argument("-l", "--longitude", action="store_true", default=False,
    help="edit the stored longitude value used for calculating LST")
args = parser.parse_args()

# If no options given, default to GUI startup
if not args.gui and not args.console and not args.longitude:
    args.gui = True

if args.longitude:
    longitude_file = os.path.abspath(__file__)
    # File needs to find the path to itself.
    # Make sure you don't use the .pyc file!
    if longitude_file[-4:] == ".pyc":
        longitude_file = longitude_file[:-1]
    
    # Config for longitude setting.
    # Prompts the user to edit the longitude setting
    print("Current longitude setting:", longitude)
    new_longitude = float(raw_input("Enter new longitude: "))
    this_file = open(longitude_file, "r")
    l = list(this_file)
    this_file.close()
    l[longitude_line] = "longitude = " + str(new_longitude) + "\n"
    s = "".join(l)
    this_file = open(longitude_file, "w")
    this_file.write(s)
    this_file.close()
    print("Longitude was updated to %s.\n" % (new_longitude))
    exit()

def wrap(value, lower, upper):
    # Wraps value to a circular range between lower and upper
    return (value - (upper - lower) *
            math.floor(float(value - lower) / float(upper - lower)))

def julian_date(utc):
    # Calculate Julian Date (float) from UTC struct_time object 
    year = utc.tm_year
    month = utc.tm_mon
    day = utc.tm_mday
    hour = utc.tm_hour
    minute = utc.tm_min
    second = utc.tm_sec
    
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    jd = jdn + (hour - 12) / 24.0 + minute / 1440.0 + second / 86400.0
    
    return jd
 
def local_sidereal_time(jd, longitude):
    # Calculate LST from Julian Date and longitude, return as tuple
    jd0 = math.floor(jd - 0.5) + 0.5
    h = 24 * (jd - jd0)
    d = jd - 2451545
    d0 = jd0 - 2451545
    t = d / 36525.0
    
    gmst = 6.697374558 + 0.06570982441908 * d0 + \
           1.00273790935 * h + 0.000026 * t ** 2.0
    gmst = wrap(gmst, 0.0, 24.0)
    
    omega = math.radians(125.04 - 0.052954 * d)
    l = math.radians(280.47 + 0.98565 * d)
    delta_psi = -0.000319 * math.sin(omega) - 0.000024 * math.sin(2 * l)
    epsilon = math.radians(23.4393 - 0.0000004 * d)
    eqeq = delta_psi * math.cos(epsilon)

    gast = gmst + eqeq
    gast = wrap(gast, 0.0, 24.0)
    
    lst = gast + longitude / 15.0
    lst = wrap(lst, 0.0, 24.0)
    
    seconds = int(wrap(round(lst * 3600.0), 0.0, 86400.0))
    hour = seconds // 3600
    minute = (seconds - hour * 3600) // 60
    second = seconds - hour * 3600 - minute * 60
    
    return hour, minute, second

def calculate_time(longitude):
    # Return the full set of clock values as a dictionary
    now = time.time()
    
    lt = time.localtime(now)
    utc = time.gmtime(now)
    jd = julian_date(utc)
    lst = local_sidereal_time(jd, longitude)
    
    lt = (time.strftime("%Y-%m-%d %H:%M:%S ", lt)
          # Make sure local time zone name is abbreviated
          + "".join(c for c in time.strftime("%Z", lt) if c.isupper()))
    utc = time.strftime("%Y-%m-%d %H:%M:%S UTC", utc)
    jd = "%.5f JD" % (jd)
    lst = "%02dh %02dm %02ds LST" % (lst)
    
    return {"lt": lt, "utc": utc, "jd": jd, "lst": lst}

def animate(draw, fps=30.0):
    # Repeatedly calls function 'draw' at regular time intervals
    # Calls function 'fps' times per second
    while True:
        old_time = time.time()
        draw()
        new_time = time.time()
        time_left = (1.0 / fps) - (new_time - old_time)
        if time_left > 0.0:
            time.sleep(time_left)
#        old_time = new_time

if args.console:
    
    # Clears space in the terminal to prepare for the clock
    print("StarClock (CTRL-C to exit)")
    sys.stdout.write("\n" * 4)
    sys.stdout.flush()
    
    def update_console(time_dict):
        # Displays times from time_dict in the terminal space
        sys.stdout.write("\x1b[A" * 4)  # Doesn't work on Windows... clearing might work
        print(time_dict["lt"] + "\n" + time_dict["utc"] + "\n" + \
        time_dict["jd"] + "\n" + time_dict["lst"])
        sys.stdout.flush()

    # Engine for clock in console.
    def update_clock():
        time_dict = calculate_time(longitude)
        update_console(time_dict)
    # Try statement to allow quitting with CTRL-C
    try:
        animate(update_clock, 30.0)
    except KeyboardInterrupt:
        print()
        raise SystemExit

if args.gui:
    
    # Starts up the GUI and returns the GraphWin and Text objects
    window = graphics.GraphWin("StarClock", 280, 100, autoflush=False)
    window.setBackground("black")
    text = graphics.Text(graphics.Point(140, 50), "0000-00-00 00:00:00 ???\n0000-00-00 00:00:00 UTC\n0000000.00000 JD\n00h 00m 00s LST")
    text.setFace("courier")
    text.setTextColor("red")
    text.setStyle("bold")
    text.draw(window)
    graphics.update()
    
    def update_gui(window, text, time_dict):
        # Displays times from time_dict using text in window
        text.setText("%s\n%s\n%s\n%s" % (time_dict["lt"], time_dict["utc"], time_dict["jd"], time_dict["lst"]))
        graphics.update()
    
    # Engine for clock in graphics window.
    def update_clock():
        if window.closed:
            raise SystemExit
        time_dict = calculate_time(longitude)
        update_gui(window, text, time_dict)
    animate(update_clock, 30.0)
