#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Module to detect gestures from Leap Motion Controller
"""

import inspect
import os
import sys

SRC_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
LIB_DIR = os.path.abspath(os.path.join(SRC_DIR, './lib'))
sys.path.insert(0, LIB_DIR)

import Leap #pylint: disable=import-error, wrong-import-position
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture




class gestures():
	parameters[]
	
	def __init__(self, start, stop, details=[]):
		self.start_frame = start
		self.stop_frame = stop
		self.parameters.append(details)

	def is_gesture():
		# Check if the motion corresponds to this particular gesture
		pass
		
	def gesture_details(self):
		# Return parameters of the gesture in a tangible format
		pass
	
		
class ClearSpace(gestures):
	
	def is_gesture():
		

	
class LeapListener(Leap.Listener):
	"""
	Class to detect and pass on gestures
	"""

	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'INtermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	lastFrameID = 0

	def on_init(self, controller):
		"""
		Args:
			controller: ID to operate upon
		"""
		print("Listener Initialised")

	def on_connect(self, controller):
		"""
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
		Args:
			controller: ID to operate upon
		"""
		frame = controller.frame()

		for hand in frame.hands:

			hand_type = "Left Hand" if hand.is_left else "Right Hand"
				#print("Hand type: %s, palm x velocity: %s," %(hand_type, hand.palm_velocity.x))
				#print("Hand type: %s, palm normal: %s, palm position: %s"
					#%(hand_type, hand.palm_normal, hand.palm_position))

		def processFrame(frame, weight, hand_count={}):
			if( not frame.is_valid):
				return hand_count
			count = len(frame.hands)
			if count in hand_count.keys():
				hand_count[count] += weight + (1-weight)*hand_count[count]
			else:
				hand_count[count] = weight
			return hand_count

		def HandCount(self, controller, window=10):
			no_of_hands = {0:0, 1:0, 2:0}
			for i in range(window):
				no_of_hands = processFrame(controller.frame(window-i), 0.9, no_of_hands)
			comp = lambda x: no_of_hands[x]
			return max(no_of_hands, key=comp)

		# Gesture detection

		# Add additional gestures here as keys. Each gestures's parameters
		# are stored in its respective value.
		gestures = {'clearSpace':[], 'point':[]}

		hand_count = HandCount(self, controller)
		if hand_count == 2:
			left, right = frame.hands.leftmost, frame.hands.rightmost
			rel_x_velocity = right.palm_velocity.x - left.palm_velocity.x
			rel_orient = left.palm_normal.x*right.palm_normal.x

			if rel_orient < 0 and rel_x_velocity > 100:
				gesture_detected = "Clear Space"
				# Define parameters to characterise the gesture.
				
		elif hand_count == 1:
			pointing_fingers = frame.fingers.extended()

			if not pointing_fingers.is_empty:
				gesture_detected = "Point"
				forward_finger = pointing_fingers.frontmost
				# Return the position on screen being pointed by the forward most finger

		if gesture_detected == "Clear Space":
			print("Frame: %d Current Gesture: %s" %(frame.id, gesture_detected))
			# Send the relevant parameters across to openGL
		elif gesture_detected == "Point":
			print("Frame: %d Current Gesture: %s, fingertype: %s "
			%(frame.id, gesture_detected, self.finger_names[forward_finger.type]))


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

if __name__ == '__main__':
	main()
