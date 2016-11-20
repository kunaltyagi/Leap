#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Analogue to Stage in a typical application
"""

from OpenGL.GL import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *  # pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import


class World:
    """
    holds all the elements, and interface to modify any element
    """
    def __init__(self):
        self.elements = list()
        self.active_elements = list()

    def display(self):
        """
        displays the elements to the screen
        """
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for element in self.elements:
            element.display()

    def add_element(self, element):
        """
        adds an element onto the screen
        """
        self.elements.append(element)
        self.active_elements = [self.elements[-1]]

    def clear(self):
        """
        removes all the elements
        """
        self.__init__()

    def transform(self, pose=None):
        """
        modifies the elements selected
        """
        for element in self.active_elements:
            element.transform(pose)
