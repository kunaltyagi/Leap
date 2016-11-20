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
            pygame.event.post(pygame.event.Event(pygame.USEREVENT+1,
                              parameter=gesture.parameters,
                              gesture="swipe"))
            # self.camera_move(gesture)

    def other_events(self, event):
        print(event.type)
        if event.gesture == "swipe":
            delta = [x - y for x, y in zip(event.parameter['position'],
                                           event.parameter['start_position'])]
            self.camera_move(delta)

    def camera_move(self, delta):
        t = self.del_camera['translate']
        glTranslatef(-t[0], -t[1], -t[2])
        for i in range(0, 3):
            self.del_camera['translate'][i] += delta[i]
        t = self.del_camera['translate']
        glTranslatef(t[0], t[1], t[2])

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
        # elif key == pygame.K_7:
        #     class Gesture():
        #         def __init__(self):
        #             self.type = 'swipe'
        #             self.parameters={'start_position': [0, 2, 4],
        #                              'position': [0, 5, 8]}
        #     self.leap_gesture(Gesture())
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
