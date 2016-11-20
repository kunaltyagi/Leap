#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Module to detect gestures from Leap Motion Controller
"""

import inspect
import os
import sys

SRC_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
LIB_DIR = os.path.abspath(os.path.join(SRC_DIR, '../../lib'))
sys.path.insert(0, LIB_DIR)

import Leap #pylint: disable=import-error, wrong-import-position
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from ..ogl.application import Application

class Gesture(object):
    """
    Identifies and stores gesture data
    """

    def __init__(self):
        self.type = 'no_gesture'
        self.parameters = {}

    def update_gesture(self, gesture_type, details=None):
        """
        Updates the gesture parameters
        """
        self.type = gesture_type
        if details is not None:
            self.parameters.update(details)

    def gesture_data(self):
        """
        Sends details of gesture as a dictionary
        """
        with open('gesture_data.txt', 'a') as data:
            data.write("Gesture Type: %s\n" %(self.type))
            details = self.parameters
            if len(details) > 0:
                for param in sorted(details.keys()):
                    data.write("%s : %s\n" %(param, details[param]))
            data.write("\n")


# Stabilizer can be made into a decorator
def HandStabilizer(frame, weight=0.7, hand_count={}):
    """
    Updates the windowed average of number of visible hands.
    Args:
        frame: current frame
        weight: relative weight to the data in current frame
        hand_count: object to be updated;
                    currently the number of hands
    """
    if( not frame.is_valid):
        return hand_count
    count = len(frame.hands)
    if count in hand_count.keys():
        hand_count[count] += weight + (1-weight)*hand_count[count]
    else:
            hand_count[count] = weight
    return hand_count

def HandCount(controller, window=10):
    """
    Accounts for errors in detection and delay from the sensor by
    means of a windowed average
    Args:
        controller: controller ID to get sensed data
        window: size of the window
    """
    no_of_hands = {0:0, 1:0, 2:0}
    for i in range(window):
        no_of_hands = HandStabilizer(controller.frame(window-i),hand_count=no_of_hands)
    comp = lambda x: no_of_hands[x]
    return max(no_of_hands, key=comp)

def detect_gesture(self, frame, ):
    """
    Detects gestures from the frame data
    """
    # Add more gestures and corresponding rules
    gesture_types = ['clear_space', 'point']

    left, right = frame.hands.leftmost, frame.hands.rightmost
    rel_x_velocity = right.palm_velocity.x - left.palm_velocity.x
    rel_orient = left.palm_normal.x*right.palm_normal.x

    if rel_orient < 0 and rel_x_velocity > 100:
        return True
    else:
        return False



class LeapListener(Leap.Listener):
    """
    Implementation of a listener to detect and pass on gestures
    """
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'INtermediate', 'Distal']

    # Add additional gestures here as keys. Each gestures's parameters
    gesture = Gesture()

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
        hand_count = HandCount(controller)
        details = {'frame_id': frame.id}
        print(hand_count)
        if hand_count == 2:
            left, right = frame.hands.leftmost, frame.hands.rightmost
            rel_x_velocity = right.palm_velocity.x - left.palm_velocity.x
            rel_orient = left.palm_normal.x*right.palm_normal.x

            if rel_orient < 0 and rel_x_velocity > 100:
                flag = True
                gesture_name = "clear_space"
                if( self.gesture.type != gesture_name):
                    details['start'] = frame.id
                details['Left Normal'] = left.palm_normal
                details['Left position'] = left.palm_position
                details['Right position'] = right.palm_position
                details['Right Normal'] = right.palm_normal

            # Define parameters to characterise the gesture.

        elif hand_count == 1:
            # Check for the following gestures: point, #to be added soon
            extended_fingers = frame.fingers.extended()

            finger_count = len(extended_fingers)
            if finger_count == 1 and extended_fingers[0].type == 1:
                gesture_name = "point"
                if self.gesture.type != gesture_name:
                    details['start'] = frame.id    
                flag = True

                forward_finger = extended_fingers[0]
                details['from'] = forward_finger.stabilized_tip_position
                details['to'] = forward_finger.direction.normalized
                # Return the position on screen being pointed by the
                # forward most finger

        print('Frame: %d' %(frame.id))
        if flag:
            self.gesture.update_gesture(gesture_name, details)
            self.gesture.gesture_data()
            print("Gesture name: %s" %(gesture_name))
        else:
            self.gesture = Gesture()


def main():
    """
    Runs the application
    """
    listener = LeapListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press enter to quit")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        #print("Thank you for trying our program")

if __name__ == '__main__':
    main()
