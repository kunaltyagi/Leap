#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Make all transformations, handle creation, deletion requests, etc.
"""

class Element(object):
    def __init__(self):
        pass

    def create(self):
        pass

    def cleanup(self):
        pass

    def init(self):
        pass

    def draw(self):
        pass

    def transform(self, pose=None):
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
