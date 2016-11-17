#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Make all transformations, handle creation, deletion requests, etc.
"""

from OpenGL.GL import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import

class Element(object):
    def __init__(self):
        self.origin = [0, 0, 0]
        self.pose = [0, 0, 0]

    def create(self):
        pass

    def cleanup(self):
        pass

    def init(self):
        pass

    def display(self):
        glPushMatrix()
        self.transform()
        self.draw()
        glPopMatrix()

    def draw(self):
        pass

    def adjust(self, parameters=None):
        if not parameters:
            return
        for param in parameters:
            if hasattr(self, param):
                setattr(self, param, parameters[param])

    def transform(self, pose=None):
        glTranslatef(-self.origin[0], -self.origin[1], -self.origin[2])
        # rotate first, then translate
        if not pose:
            pose = self.pose
        # TODO rotate properly, use quaternions or smthg
        glTranslatef(pose[0], pose[1], pose[2])

class Joint(Element):
    def __init__(self, parent, child):  # allow child to be a list?
        assert isinstance(parent, Element)
        assert isinstance(child, Element)
        self.parent = parent
        self.child = child
        self.child_rel_pose = None  # this is constant
        self.joint_pose = None  # change this to move the joint

    def draw(self):
        self.transform(self.joint_pose)
        self.transform(self.child_rel_pose)
        child.draw()
        pass

    def cleanup(self):
        self.child.cleanup()
