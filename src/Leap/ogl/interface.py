#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper around PyOpenGL and PyGame
"""

# import OpenGL

import pygame  # pylint: disable=import-error
from OpenGL.GL import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
# from OpenGL.arrays import vbo


class GLInterface(object):  # pylint: disable=too-many-instance-attributes
    """
    Creates a screen, and allows easy evaluation of events
    """
    def __init__(self):
        self.display = (800, 600)
        self.center = [0, 0, 0]
        self.eye = [-40, 0, 0]
        self.up = [0, 0, 1]  # pylint: disable=invalid-name
        self.fov = 60
        self.near = 0.1
        self.far = 300
        self.bg_color = [0.1, 0.1, 0.5, 0.2]
        self.keys = {}  # 133 keys in PyGame
        self.cleanup = None

        pygame.init()
        pygame.display.set_mode(self.display,
                                pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("CAD Demo")

    def event_handler(self, event):
        """
        A big switch case function for input event
        Args:
            event: pygame.Event, used to check for events
        """
        handlers = {
            pygame.QUIT: self.stop_and_exit,
            pygame.KEYDOWN: lambda: self.key_down(event.key),
            pygame.KEYUP: lambda: self.key_up(event.key),
            pygame.MOUSEBUTTONDOWN: self.mouse_motion,
            pygame.MOUSEBUTTONUP: lambda: self.mouse_button_up(event),
            pygame.MOUSEMOTION: lambda: self.mouse_button_down(event)
        }
        return handlers.get(event.type,
                            lambda: self.unimplemented("Event {}".\
                                    format(event.type)))

    def key_up(self, key):
        """
        Args:
            key: key unpressed
        """
        self.keys[key] = False

    def key_down(self, key):
        """
        Args:
            key: key pressed
        """
        if key == pygame.K_ESCAPE:
            self.stop_and_exit()
        self.keys[key] = True

    def mouse_button_up(self, event):
        """
        Args:
            event: directly passes from event-handler
        """
        self.unimplemented("Mouse click up {}").format(event)

    def mouse_button_down(self, event):
        """
        Args:
            event: directly passes from event-handler
        """
        self.unimplemented("Mouse click down {}".format(event))

    def mouse_motion(self):
        """
        Detect motion of mouse
        """
        self.unimplemented("Mouse motion")

    def init_loop(self):
        """
        It is called before drawing on the screen each time
        """
        glClearColor(*self.bg_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def init(self):
        """
        Sets the env settings for the application in the beginning
        """
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        glDepthFunc(GL_LESS)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, (self.display[0]/self.display[1]),
                       self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(*(self.eye + self.center + self.up))

    def display_loop(self):
        """
        Main display function, called every iteration
        """
        self.init_loop()

    def unimplemented(self, something):  # pylint: disable=no-self-use
        """
        Simple wrapper apund print for ease
        """
        print("[GL] {} is not handled as of now".format(something))

    def stop_and_exit(self):  # pylint: disable=no-self-use
        """
        Quit the application properly
        """
        if self.cleanup is not None:
            self.cleanup()
        pygame.quit()
        quit()

    def main_loop(self):
        """
        Blocking loop, as per the convention of opengl
        """
        self.init()
        while True:
            for event in pygame.event.get():
                self.event_handler(event)()
            self.display_loop()
            pygame.display.flip()
            # pygame.time.wait(100)
