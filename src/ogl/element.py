#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Make all transformations, handle creation, deletion requests, etc.
"""

import numpy as np
import quaternion

from OpenGL.GL import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import
from OpenGL.GLU import *#pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import

class Element(object):
    def __init__(self):
        self.origin = [0, 0, 0]
        self.pose = {'translate': [0, 0, 0],
                     'rotate': [1, 0, 0, 0]} #np.quaternion(1, 0, 0, 0)}
        self.base_pose = self.pose.copy()
        self.param = dict()

    def create(self):
        pass

    def cleanup(self):
        pass

    def init(self):
        pass

    def draw(self):
        pass

    def modify_pose(self, delta_pose=None):
        if not delta_pose:
            return
        key = 'translate'
        if key not in delta_pose:
            delta_pose[key] = [0, 0, 0]
        self.pose[key] = self.base_pose[key] + delta_pose[key]
        key = 'rotate'
        if key not in delta_pose:
            delta_pose[key] = quaternion.one
        self.pose[key] = delta_pose[key] * self.base_pose[key]

    def fix_pose(self, pose=None):
        if not pose:
            pose = self.pose
        self.base_pose = pose

    def display(self):
        glPushMatrix()
        self.transform()
        self.draw()
        glPopMatrix()

    def adjust(self, parameters=None):
        if not parameters:
            return
        for param in parameters:
            if hasattr(self, param):
                setattr(self, param, parameters[param])

    def transform(self, pose=None):
        if not pose:
            pose = self.pose
        else:
            for key in set(self.pose) - set(pose):
                pose[key] = self.pose[key]
        t = pose['translate']
        glTranslatef(t[0], t[1], t[2])
        # rotate first, then translate
        r = pose['rotate']
        # glRotatef(r.w, r.x, r.y, r.z)
        # TODO rotate properly, use quaternions or smthg
        glTranslatef(-self.origin[0], -self.origin[1], -self.origin[2])

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
