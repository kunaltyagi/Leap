#!/usr/bin/env python
# -*- coding: utf-8 -*-

from leap.leap_start import Leap, LeapListener
from ogl.application import Application


class Gesture():
    """
    Identifies and stores gesture data
    """

    def __init__(self):
        self.type = 'no_gesture'
        self.parameters = {}

    def update_gesture(self, gesture_type, details=None):
        """
        Updates the gesture parameters
        """
        self.type = gesture_type
        if details is not None:
            self.parameters.update(details)

    def add_application(self, app):
        self.app = app

    def gesture_data(self):
        """
        Sends details of gesture as a dictionary
        """
        with open('gesture_data.txt', 'a') as data:
            data.write("Gesture Type: %s\n" %(self.type))
            details = self.parameters
            if len(details) > 0:
                for param in sorted(details.keys()):
                    data.write("%s : %s\n" %(param, details[param]))
            data.write("\n")


def main():
    """
    Runs the application
    """
    gl_app = Application()

    gestures = Gesture()
    gestures.add_application(gl_app)

    listener = LeapListener()
    listener.add_callback(gestures)

    controller = Leap.Controller()
    controller.add_listener(listener)

    gl_app.cleanup = lambda: controller.remove_listener(listener)

    print("Press ESC to quit")
    gl_app.main_loop()
    # try:
    #     sys.stdin.readline()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     controller.remove_listener(listener)
    print("Thank you for trying our program")

if __name__ == '__main__':
    main()
