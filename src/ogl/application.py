#!/usr/bin/env python
# -*- coding: utf-8 -*-

from interface import GLInterface
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


class Application(GLInterface):
    def __init__(self):
        GLInterface.__init__(self)
        self.quadric = gluNewQuadric()
        self.cube = Cube()

    def key_up(self, key):
        pass

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.stop_and_exit()
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
        else:
            GLInterface.key_down(self, key)
        # TODO: buffer of keyboard to poll for key up event

    def mouse_button_up(self, button):
        pass

    def mouse_button_down(self, button):
        pass

    def mouse_motion(self):
        pass

    def display_loop(self):
        GLInterface.display_loop(self)
        gluCylinder(self.quadric, 4, 2, 5, 25, 1)

def main():
    gl_app = Application()
    gl_app.main_loop()

if __name__ == "__main__":
    main()
