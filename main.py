import curses
from curses import wrapper
import time
import random

# Starting screen
def start_screen(stdscr):
    stdscr.clear()  # Clears any content on screen
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()  # Refresh screen
    stdscr.getkey()

# Function to display screen
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    # Overlay the typing over the text
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)  # Get color pair with ID

# Get random string
def load_text():
    with open("data.txt", "r") as file:
        lines = file.readlines()
        return random.choice(lines).strip()

# WPM test
def wpm_test(stdscr):
    # Text to type
    target_text = load_text()
    # List to get text typed
    current_text = []
    wpm = 0
    # Start time to calculate WPM
    start_time = time.time()
    stdscr.nodelay(True)  # Stops blocking, aka still updates WPM even if user isn't typing

    stdscr.clear()  # Clears any content on screen
    stdscr.addstr(target_text)
    stdscr.refresh()  # Refresh screen

    while True:
        # Get current time difference
        time_elapsed = max((time.time() - start_time), 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # Get the WPM if average length of word is 5

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)  # Stop the delay
            break

        # Loop to update WPM
        try:
            key = stdscr.getkey()
        except:
            continue

        # Get ASCII number of escape key to break
        if ord(key) == 27:
            quit()

        # Deal with backspace
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

# Standard screen
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Arguments are ID, text color, and bg color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

if __name__ == "__main__":
    wrapper(main)
