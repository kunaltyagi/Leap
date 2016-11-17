#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stores a sample of possible elemens.
Called sample because it doesn't implement all functionality and does a lot of ad-hoc things
"""

from element import Element

from OpenGL.GL import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import

class Cube(Element): #pylint: disable=too-few-public-methods
    """
    Draws a wireframe cube
    """
    def __init__(self):
        self.vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                         (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
        self.edges = ((0, 1), (0, 3), (0, 4),
                      (2, 1), (2, 3), (2, 7),
                      (6, 3), (6, 4), (6, 7),
                      (5, 1), (5, 4), (5, 7))

    def __call__(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


class Cylinder(Element):
    def __init__(self, top_radius=3, bottom_radius=3, height=5):
        Element.__init__(self)
        # It would be better to share this quadric, but for now, wth
        self.quadric = gluNewQuadric()
        self.top_radius = top_radius
        self.bottom_radius = bottom_radius
        self.height = height
        self.arc_len = 10
        self.adjust()

    def adjust(self, parameters=None):
        Element.adjust(self, parameters)
        self.origin = [0, 0, self.height/2]

    def draw(self):
        gluCylinder(self.quadric, self.bottom_radius, self.top_radius,
                    self.height,
                    (self.top_radius + self.bottom_radius)*self.arc_len, 1)
