# ASCII Art Bounce Script
import sys
import os
import time
import math

art_file = "/home/julian/.local/scripts/misc/hiunixporn"  # Put any ascii art here
gravity = 1.8       # Acceleration (pixels/frame^2) - adjust for feel
bounce_factor = 0.5 # Energy loss on bounce (0 to <1)
initial_vy = 0.0
delay = 0.04

with open(art_file, 'r') as f:
    art_lines = f.read().splitlines() # Read without trailing newlines

art_height = len(art_lines)
art_width = max(len(line) for line in art_lines) # Real width needed now

def print_at(r, c, text):
    # Clamp row/col to be within bounds
    r = max(1, min(r, lines))
    c = max(1, min(c, cols - len(text) + 1)) # Basic terminal width check
    sys.stdout.write(f"\033[{int(r)};{int(c)}H{text}")

try:
    sys.stdout.write("\033[?25l\033[2J") # Hide cursor, clear
    sys.stdout.flush()

    cols, lines = os.get_terminal_size()
    target_col = (cols - art_width) // 2 + 1
    floor_row = lines - art_height + 1

    y = 1.0 # Current top row (float for physics)
    vy = initial_vy # Current velocity
    bouncing = True

    while bouncing:
        sys.stdout.write("\033[2J") # Clear screen

        # Draw art at current position
        draw_row = math.ceil(y) # Use ceiling to avoid going below floor too early
        for i, line in enumerate(art_lines):
             if draw_row + i <= lines: # Don't draw below screen
                print_at(draw_row + i, target_col, line)

        sys.stdout.flush()
        time.sleep(delay)

        # Update physics
        vy += gravity
        y += vy

        # Check for bounce
        if y >= floor_row:
            y = floor_row # Snap to floor
            vy *= -bounce_factor # Reverse and dampen velocity

            # Stop bouncing if velocity is very low
            if abs(vy) < 1.0: # Adjust threshold
                 # Draw final resting frame
                 sys.stdout.write("\033[2J")
                 for i, line in enumerate(art_lines):
                     print_at(floor_row + i, target_col, line)
                 sys.stdout.flush()
                 bouncing = False # Exit loop

finally:
    sys.stdout.write(f"\033[{lines};1H\033[?25h") # Show cursor at bottom
    sys.stdout.flush()
