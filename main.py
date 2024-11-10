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

# WPM test
def wpm_test(stdscr):
    data = [
        "The quick brown fox jumps over the lazy dog. It's a classic pangram that uses every letter of the alphabet.",
        "Pack my box with five dozen liquor jugs. This sentence has been a favorite for typing tests for years.",
        "A journey of a thousand miles begins with a single step. Every great accomplishment starts with the first action.",
        "To be or not to be, that is the question. It is one of the most famous lines in literature from Shakespeare's Hamlet.",
        "All that glitters is not gold. Appearances can be deceiving, and value is often found beneath the surface.",
        "In the middle of difficulty lies opportunity. Challenges bring growth, and hardship can lead to great achievements.",
        "An apple a day keeps the doctor away. This saying emphasizes the importance of eating healthy and staying active.",
        "The early bird catches the worm. Being proactive and starting early often leads to success.",
        "Actions speak louder than words. What you do is more important than what you say.",
        "Better late than never. It's always good to make an effort, no matter how delayed it may be.",
        "Knowledge is power. The more you learn, the better equipped you are to handle the world's challenges.",
        "Time is money. Efficiency and productivity can save both time and resources.",
        "When in doubt, leave it out. If you're unsure about something, it's often better to leave it behind than make a mistake.",
        "You miss 100% of the shots you don't take. Taking risks is necessary if you want to achieve something great.",
        "This is a simple typing test for WPM games. It's designed to help you improve your typing speed and accuracy.",
        "Consistency is key to success. Achieving long-term goals requires persistence and dedication, even through tough times.",
        "Don't count the days, make the days count. Focus on making the most of your time rather than just passing it.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. Persistence is what truly matters.",
        "Life is what happens when you're busy making other plans. Sometimes, you have to embrace the unexpected.",
        "The only way to do great work is to love what you do. Passion and dedication are essential for outstanding results.",
        "The best way to predict the future is to create it. Instead of waiting for things to happen, take control and make it happen."
    ]

    # Text to type
    target_text = random.choice(data)
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
            break

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
