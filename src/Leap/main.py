#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo application for 3D CAD
"""

from Leap.leap.leap_start import Leap as OrigLeap
from Leap.leap.leap_start import LeapListener
from Leap.ogl.application import Application


class Gesture(object):
    """
    Identifies and stores gesture data
    """
    def __init__(self, name='no_gesture', details=None):
        self.type = name
        self.parameters = details if details else dict()
        self.app = None

    def update_gesture(self, gesture_name, details=None):
        """
        Updates the gesture parameters
        """
        self.type = gesture_name
        if details is not None:
            self.parameters.update(details)

    def add_application(self, app):
        """
        Add the application which this gesture is to be passed onto
        """
        self.app = app

    def gesture_data(self):
        """
        Sends details of gesture as a dictionary
        """
        if self.app is not None:
            self.app.leap_gesture(self)


def main():
    """
    Runs the application
    """
    gl_app = Application()

    gestures = Gesture()
    gestures.add_application(gl_app)

    listener = LeapListener()
    listener.add_gesture(gestures)

    controller = OrigLeap.Controller()
    controller.add_listener(listener)

    gl_app.cleanup = lambda: controller.remove_listener(listener)

    print("Press ESC to quit")  # pylint: disable=superfluous-parens
    gl_app.main_loop()
    # try:
    #     sys.stdin.readline()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     controller.remove_listener(listener)
    print("Thank you for trying our program")  # pylint: disable=superfluous-parens

if __name__ == '__main__':
    main()
