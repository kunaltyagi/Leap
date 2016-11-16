#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Analogue to Stage in a typical application
"""

class World:
    def __init__(self):
        self.elements = list()
        self.activeElements = list()

    def display(self):
        for element in self.elements:
            element.display()

    def add_element(self, element):
        self.elements.append(element)
        self.activeElements = [self.elements[-1]]

    def transform(self, pose=None):
        for element in self.activeElements:
            element.transform(pose)

