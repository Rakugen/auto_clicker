# This is a practice implementation for an auto-clicker that can be toggled start/stop/off and will click at high speeds
# for the purpose of auto clicker games like Cookie Clicker but can be expanded/modified to do other things that
# involves mouse clicks and/or keyboard presses.

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# delay controls time between button presses
DELAY = 0.001
# button determines which mouse button to be pressed
BUTTON = Button.left
# start_stop and exit keys will control toggle for on/off and exit program
START_STOP_KEY = KeyCode(char="`")
EXIT_KEY = KeyCode(char="=")


# Creating a new class that inherits from thread. This will allow us to overwrite threads run function with
# our own as well as controlling when to start/stop/exit.
class ClickMouse(threading.Thread):
    # Inherit threads init() as well as adding our own arguments: delay/button from global.
    # self.running and self.program_running will be used as control flow.
    def __init__(self, delay, button):
        super().__init__()
        self.delay = DELAY
        self.button = BUTTON
        self.running = False
        self.program_running = True

    # Following 3 functions allow us to control our thread externally.
    # This function will toggle on when our program starts the clicking functionality.
    def start_clicking(self):
        self.running = True

    # This function will tell our program to stop clicking.
    def stop_clicking(self):
        self.running = False

    # This tells our program to terminate.
    def exit(self):
        self.stop_clicking()
        self.program_running = False

    # This function overwrote threads run() and will execute on thread start, will constantly execute whilst
    # 'program_running' and 'running' is true.
    # Inner loop is what the main program will be doing while it is running, in our case clicking 3 times then delay.
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                mouse.click(self.button)
                mouse.click(self.button)
                time.sleep(self.delay)


# pynput Controller for mouse inputs
mouse = Controller()
# Instantiate and start our ClickMouse class with global variables
mouse_thread = ClickMouse(DELAY, BUTTON)
mouse_thread.start()


# Control flow function that will toggle start/stop/exit on our mouse_thread
def on_press(key):
    # Toggles mouse_thread on/off which will be running the mouse clicks
    if key == START_STOP_KEY:
        if mouse_thread.running:
            mouse_thread.stop_clicking()
        else:
            mouse_thread.start_clicking()
    # Exit mouse_thread and stops listener
    elif key == EXIT_KEY:
        mouse_thread.exit()
        listener.stop()


# Creates a new listener that will monitor for keyboard inputs
with Listener(on_press=on_press) as listener:
    listener.join()
