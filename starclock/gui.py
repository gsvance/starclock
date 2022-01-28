# Module that handles the GUI window for StarClock.
# Starts and updates the window as appropriate.

import graphics

def initialize():
    # Starts up the GUI and returns the GraphWin and Text objects
    window = graphics.GraphWin("StarClock", 280, 100, autoflush=False)
    window.setBackground("black")
    text = graphics.Text(graphics.Point(140, 50), "0000-00-00 00:00:00 ???\n0000-00-00 00:00:00 UTC\n0000000.00000 JD\n00h 00m 00s LST")
    text.setFace("courier")
    text.setTextColor("red")
    text.setStyle("bold")
    text.draw(window)
    graphics.update()
    return window, text

def update(window, text, time_dict):
    # Displays times from time_dict using text in window
    text.setText("%s\n%s\n%s\n%s" % (time_dict["lt"], time_dict["utc"], time_dict["jd"], time_dict["lst"]))
    graphics.update()
