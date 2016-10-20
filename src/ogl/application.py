#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

class GLInterface(object):
    def __init__(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
        self.center = [0, 0, 0]
        self.eye = [-10, 0, 0]
        self.up = [0, 0, 1]

    def event_handler(self, event):
        handlers = {
            pygame.QUIT: self.stop_and_exit,
            pygame.KEYDOWN: lambda: self.key_down(event.key)
            # pygame.KEYUP: lambda: self.key_up(event.key),
            # pygame.MOUSEBUTTONDOWN: lambda: self.mouse_motion(),
            # pygame.MOUSEBUTTONUP: lambda: self.mouse_button_up(event.button),
            # pyfame.MOUSEMOTION: lambda self.mouse_button_down(event.button)
        }
        return handlers.get(event.type,
                lambda: self.unimplemented("Event {}".format(event.type)))

    def key_up(self, key):
        pass

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.stop_and_exit()
        else:
            self.unimplemented("Key press for {}".format(key))

    def mouse_button_up(self, button):
        pass

    def mouse_button_down(self, button):
        pass

    def mouse_motion(self):
        pass

    def init_loop(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # gluLookAt(*self.eye, *self.center, *self.up)

    def display(self):
        self.init_loop()
        self.unimplemented("Display")

    def unimplemented(self, something):
        print("[GL] {} is not handled as of now".format(something))

    def stop_and_exit(self):
        pygame.quit()
        quit()

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                self.event_handler(event)()
            self.display()
            pygame.display.flip()
            pygame.time.wait(100)

def main():
    gl_app = GLInterface()
    gl_app.main_loop()

if __name__ == "__main__":
    main()
