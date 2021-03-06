#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Module to detect gestures from Leap Motion Controller
"""

import inspect
import os
import sys

SRC_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
LIB_DIR = os.path.abspath(os.path.join(SRC_DIR, '../../../lib'))
sys.path.insert(0, LIB_DIR)

import Leap     # pylint: disable=import-error, wrong-import-position
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# Stabilizer can be made into a decorator
def hand_stabilizer(frame, count, weight=0.7):
    """
    Updates the windowed average of number of visible hands.
    Args:
        frame: current frame
        weight: relative weight to the data in current frame
        count: object to be updated;
               currently the number of hands
    """
    if not frame.is_valid:
        return count

    for key in count.keys():
        count[key] = (1-weight)*count[key]
        if key == len(frame.hands):
            count[key] += weight
    return count

def hand_count(controller, window=10):
    """
    Accounts for errors in detection and delay from the sensor by
    means of a windowed average
    Args:
        controller: controller ID to get sensed data
        window: size of the window
    """
    no_of_hands = {0:0, 1:0, 2:0, 3:0}
    for i in range(window):
        no_of_hands = hand_stabilizer(controller.frame(window-i), count=no_of_hands)
    comp = lambda x: no_of_hands[x]
    return max(no_of_hands, key=comp)

class LeapListener(Leap.Listener):
    """
    Implementation of a listener to detect and pass on gestures
    """
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'INtermediate', 'Distal']

    # Add additional gestures here as keys. Each gestures's parameters
    def add_gesture(self, gesture):
        self.gesture = gesture

    def on_init(self, controller):
        """
        Detects controller initialisation
        Args:
            controller: ID to operate upon
        """
        print("Listener Initialised")

    def on_connect(self, controller):
        """
        Detects connection of Leap Motion sensor
        Args:
            controller: ID to operate upon
        """
        print("Motion Sensor Connected")

        # Enable Gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        controller.config.set("Gesture.Swipe.MinLength", 10.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 4)
        controller.config.set("Gesture.ScreenTap.MinForwardVelocity", 1.0)
        controller.config.set("Gesture.ScreenTap.MinDistance", 0.5)
        controller.config.set("Gesture.Circle.MinRadius", 5.0)
        controller.config.set("Gesture.Circle.MinArc", 0.5)
        controller.config.save()

    def on_disconnect(self, controller):
        """
        Detects loss of connection the controller
        Args:
            controller: ID to operate upon
        """
        print("Leap Motion disconnected")

    def on_exit(self, controller):
        """
        Args:
            controller: ID to operate upon
        """
        print("Exited")

    def on_frame(self, controller):
        """
        Fetches data from the current frame. Called repeatedly until
        controller is exited
        Args:
            controller: ID to operate upon
        """
        frame = controller.frame()

        # Gesture detection
        # are stored in its respective value.

        flag = False
        gesture_name = ""
        count = hand_count(controller)

        details = {'frame_id': frame.id}
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                gesture_name = 'circle'

                details['center'] = circle.center
                details['radius'] = circle.radius
                details['tip'] = circle.pointable.stabilized_tip_position

                if gesture.state is Leap.Gesture.STATE_START:
                    details['start'] = frame.id
                    details['start_position'] = details['tip']
                flag = True
                continue

            elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
                scr_tap = Leap.ScreenTapGesture(gesture)
                gesture_name = 'select'
                details['tip'] = scr_tap.position
                details['direction'] = scr_tap.direction
                flag = True
                continue

            elif gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                gesture_name = 'swipe'
                details['position'] = swipe.position
                details['direction'] = swipe.direction

                if gesture.state is Leap.Gesture.STATE_START:
                    details['start'] = frame.id
                    details['start_position'] = swipe.position
                    details['prev_position'] = details['start_position']
                else:
                    details['prev_position'] = self.gesture.parameters['position']
                flag = True
                continue

        if count == 2 and not flag:
            left, right = frame.hands.leftmost, frame.hands.rightmost
            rel_x_velocity = right.palm_velocity.x - left.palm_velocity.x
            rel_orient = left.palm_normal.x*right.palm_normal.x

            if rel_orient < 0 and rel_x_velocity > 100:
                flag = True
                gesture_name = "clear_space"
                #details['Left Normal'] = left.palm_normal
                #details['Left position'] = left.palm_position
                #details['Right position'] = right.palm_position
                #details['Right Normal'] = right.palm_normal

            # Define parameters to characterise the gesture.

        # Point gesture
        #elif count == 1 and not flag:
        #    # Check for the following gestures: point, #to be added soon
        #    extended_fingers = frame.fingers.extended()

        #    finger_count = len(extended_fingers)
        #    if finger_count == 1 and extended_fingers[0].type == 1:
        #        gesture_name = "point"
        #        flag = True
        #        if self.gesture.type != gesture_name:
        #            details['start'] = frame.id

        #        forward_finger = extended_fingers[0]
        #        details['tip'] = forward_finger.stabilized_tip_position
        #        details['to'] = forward_finger.direction.normalized
        #        # Return the position on screen being pointed by the
        #        # forward most finger

        if flag:
            self.gesture.update_gesture(gesture_name, details)
            self.gesture.gesture_data()
            print("Gesture name: %s" %(gesture_name))
        else:
            self.gesture.type = 'no_gesture'
            self.gesture.parameters = {}
