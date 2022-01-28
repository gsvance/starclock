# The core of the StarClock module.
# Includes several functions that build the actual Starclock program.

import info
import longitude
import clock
import animation
import console
import gui

def longitude_config():
    # Config for longitude setting.
    longitude.config()
    reload(longitude)
    print

def console_clock():
    # Engine for clock in console.
    console.initialize()
    def update_clock():
        time_dict = clock.calc(longitude.longitude)
        console.update(time_dict)
    # Try statement to allow quitting with CTRL-C
    try:
        animation.animate(update_clock, 30.0)
    except KeyboardInterrupt:
        print
        raise SystemExit

def gui_clock():
    # Engine for clock in graphics window.
    window, text = gui.initialize()
    def update_clock():
        if window.closed:
            raise SystemExit
        time_dict = clock.calc(longitude.longitude)
        gui.update(window, text, time_dict)
    animation.animate(update_clock, 30.0)
