#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Actual implementation of application
"""

from interface import GLInterface
from world import World
from sample_elements import Cylinder, Cube

import pygame #pylint: disable=import-error
from OpenGL.GL import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import

class Application(GLInterface):
    """
    Implementation of GLInterface
    """
    def __init__(self):
        GLInterface.__init__(self)
        self.world = World()
        self.world.add_element(Cylinder())
        self.cube = Cube()

    def key_down(self, key):
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
