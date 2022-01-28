# Module for proper timing of FPS animations.
# Used by StarClock to update the clock displays regularly.

import time

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
