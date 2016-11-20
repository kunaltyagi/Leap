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
    """
    Stores an element (something to be drawn on the screen)
    """
    def __init__(self):
        self.origin = [0, 0, 0]
        assert np.quaternion(1, 0, 0, 0) == quaternion.one
        self.pose = {'translate': [0, 0, 0],
                     'rotate': [1, 0, 0, 0]}
                     # 'rotate': np.quaternion(1, 0, 0, 0)}
        self.base_pose = self.pose.copy()
        self.param = dict()

    def create(self):
        """
        Any setup required
        """
        pass

    def cleanup(self):
        """
        Any memory to be freed (like quadrics)
        """
        pass

    def init(self):
        """
        Don't quite know the use right now
        """
        pass

    def display(self):
        """
        Display onto the screen
        """
        glPushMatrix()
        self.transform()
        self.draw()
        glPopMatrix()

    def draw(self):
        """
        Draw here, not anywhere else
        """
        pass

    def modify_pose(self, delta_pose=None):
        """
        Edit the position and rotation of the element
        """
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
        """
        Save the current position for future use
        """
        if not pose:
            pose = self.pose
        self.base_pose = pose

    def adjust(self, parameters=None):
        """
        Edit the parameters
        """
        if not parameters:
            return
        for param in parameters:
            if hasattr(self, param):
                setattr(self, param, parameters[param])

    def transform(self, pose=None):
        """
        Moves the object around on the screen
        """
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
    """
    Joins two elements by invisible bonds
    """
    def __init__(self, parent, child):  # allow child to be a list?
        Element.__init__(self)
        assert isinstance(parent, Element)
        assert isinstance(child, Element)
        self.parent = parent
        self.child = child
        self.child_rel_pose = None  # this is constant
        self.joint_pose = None  # change this to move the joint

    def draw(self):
        """
        Draws the child element wrt the parent element
        """
        self.transform(self.joint_pose)
        self.transform(self.child_rel_pose)
        self.child.draw()

    def cleanup(self):
        """
        Performs proper cleanup
        """
        self.child.cleanup()
