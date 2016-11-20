#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Actual implementation of application
"""

from interface import GLInterface
from world import World
from sample_elements import Cylinder, Cube

import pygame  # pylint: disable=import-error
from OpenGL.GL import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import


class Application(GLInterface):
    """
    Implementation of GLInterface
    """
    def __init__(self):
        GLInterface.__init__(self)
        self.world = World()
        self.world.add_element(Cylinder())
        self.cube = Cube()
        self.del_camera = {'translate': [0, 0, 0],
                           'rotate': [1, 0, 0, 0]}

    def leap_gesture(self, gesture):
        """
        Captures gestures from leap-motion and performs required functionality

        :param gestures: any input gesture, differentiated based on gestures.type
        """
        if gesture is None:
            return
        elif gesture.type == 'no_gesture':
            print('No gesture received')
            return
        elif gesture.type == 'clear_space':
            self.world.clear()
        elif gesture.type == "swipe":
            self.camera_move(gesture)

    def camera_move(self, gesture):
        print(gesture.parameter)

    def key_down(self, key):
        """
        Caputes key-down events and performs required functionality

        :param key: the key pressed
        """
        # Move this out of key_down function
        if key == pygame.K_UP:
            glRotatef(15, 0, 1, 0)
        elif key == pygame.K_DOWN:
            glRotatef(-15, 0, 1, 0)
        elif key == pygame.K_i:
            glTranslatef(*[-1*x for x in self.eye])
            glRotatef(15, 0, 1, 0)
            glTranslatef(*self.eye)
        elif key == pygame.K_k:
            glTranslatef(*[-1*x for x in self.eye])
            glRotatef(-15, 0, 1, 0)
            glTranslatef(*self.eye)
        elif key == pygame.K_w:
            glTranslatef(0, 0, 10)
        elif key == pygame.K_s:
            glTranslatef(0, 0, -10)
        # Handle <Esc> specially if you don't want the program to end here
        GLInterface.key_down(self, key)

    def display_loop(self):
        """
        called everytime OpenGL refreshes
        """
        GLInterface.display_loop(self)
        self.world.display()


def main():
    """
    Function to setup and run the application
    """
    gl_app = Application()
    gl_app.main_loop()

if __name__ == "__main__":
    main()
