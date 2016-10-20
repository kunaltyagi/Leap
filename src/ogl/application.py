#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

class Cube(object):
    def __init__(self):
        self.vertices= ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
        self.edges = ( (0,1), (0,3), (0,4),
                (2,1), (2,3), (2,7),
                (6,3), (6,4), (6,7),
                (5,1), (5,4), (5,7))

    def __call__(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


class GLInterface(object):
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption("CAD Demo")

        self.center = [0, 0, 0]
        self.eye = [-50, 0, 0]
        self.up = [0, 0, 1]
        self.fov = 60
        self.near = 0.1
        self.far = 100
        self.bg_color = [0.1, 0.1, 0.5, 0.2]
        self.quadric = gluNewQuadric()
        self.cube = Cube()

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
        elif key == pygame.K_i:
            glRotatef(-15, 0, 1, 0)
        elif key == pygame.K_k:
            glRotatef(15, 0, 1, 0)
        elif key == pygame.K_w:
            glTranslatef(0, 0, 10)
        elif key == pygame.K_s:
            glTranslatef(0, 0, -10)
        else:
            self.unimplemented("Key press for {}".format(key))
        # TODO: buffer of keyboard to poll for key up event

    def mouse_button_up(self, button):
        pass

    def mouse_button_down(self, button):
        pass

    def mouse_motion(self):
        pass

    def init_loop(self):
        glClearColor(*self.bg_color)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def init(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        glDepthFunc(GL_LESS)

        gluLookAt(*(self.eye + self.center + self.up))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, (self.display[0]/self.display[1]), self.near, self.far)
        glMatrixMode(GL_MODELVIEW)

    def display_loop(self):
        self.init_loop()
        # self.cube()
        gluCylinder(self.quadric, 10, 5, 20, 25, 1)

    def unimplemented(self, something):
        print("[GL] {} is not handled as of now".format(something))

    def stop_and_exit(self):
        pygame.quit()
        quit()

    def main_loop(self):
        self.init()
        while True:
            for event in pygame.event.get():
                self.event_handler(event)()
            self.display_loop()
            pygame.display.flip()
            # pygame.time.wait(100)

def main():
    gl_app = GLInterface()
    gl_app.main_loop()

if __name__ == "__main__":
    main()
