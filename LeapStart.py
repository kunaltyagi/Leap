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
	parameters =[]
	
	def __init__(self, start, stop, details=[]):
		self.start_frame = start
		self.stop_frame = stop
		self.parameters.append(details)

	def is_gesture(frame):
		# Check if the motion corresponds to this particular gesture
		pass
		
	def gesture_details(self):
		# Return parameters of the gesture in a tangible format
		pass
	
		
class ClearSpace(gestures):
	
	def is_gesture(self, frame):
		pass
	
	def gesture_details(self):
		pass

class Point(gestures):
	"""
		Point gesture is to be detected when the index finger is extended
		and is at rest (other than noise).
	"""
	point_from = None
	point_to = None

	def is_gesture(self, frame):
		pass
	
	def gesture_details(self):
		pass



class LeapListener(Leap.Listener):
	"""
	Class to detect and pass on gestures
	"""

	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'INtermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	lastFrameID = 0
	# In on-frame, update self.gestures
	detected_gestures = {'type':'No gesture', 'parameters':{'start':None}}

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

	def update_gesture(self, gesture_type, parameters={}):
		self.detected_gestures['type'] = gesture_type
		if parameters != {}:
			self.detected_getures['parameters'].update(parameters)
	
	def gesture_data(self):
		with open('Gesture_Data.txt', 'a') as data:
			data.write("Gesture Type: %s\n" %(self.detected_gestures['type']))
			gesture_parameters = self.detected_gestures['parameters']
			if len(gesture_parameters) > 0:
				for param in gesture_parameters.keys():
					data.write("%s : %s\n" %(param, gesture_parameters[param]))
		

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


		# Make stabilizer a decorator
		def HandStabilizer(controller, frame, weight=0.7, hand_count={}):
			if( not frame.is_valid):
				return hand_count
			count = len(frame.hands)
			if count in hand_count.keys():
				hand_count[count] += weight + (1-weight)*hand_count[count]
			else:
				hand_count[count] = weight
			return hand_count

		def FingerStabilizer(controller, frame, vel, weight=0.7):
			if( not frame.is_valid):
				return vel
			fingers_list = frame.fingers
			if not fingers_list.is_empty:
				for i in range(5):
					if len(fingers_list.finger_type(i)) > 0:
						curr_vel = fingers_list.finger_type(i)[0].tip_velocity
						vel[i] = curr_vel*weight + vel[i]*(1-weight)
					else:
						vel[i] = vel[i]*(1-weight)
			else:
				for i in range(5):
					vel[i] *= 1 - weight
			return vel

		def FingerTipVelocity(self, controller, window=10):
			tip_vel = [ Leap.Vector.zero]*5
			for i in range(window):
				tip_vel = FingerStabilizer(controller, controller.frame(window-i),vel=tip_vel)
			return tip_vel

		def HandCount(controller, window=10):
			no_of_hands = {0:0, 1:0, 2:0}
			for i in range(window):
				no_of_hands = HandStabilizer(controller, controller.frame(window-i),hand_count=no_of_hands)
			comp = lambda x: no_of_hands[x]
			return max(no_of_hands, key=comp)

		# Gesture detection

		# Add additional gestures here as keys. Each gestures's parameters
		# are stored in its respective value.
		#gestures = {'clearSpace':[], 'point':[]}

		gesture_flag = False
		gesture_name = ""
		hand_count = HandCount(controller)
		parameters = {'Current Frame ID': frame.id}
		print(hand_count)
		if hand_count == 2:
			left, right = frame.hands.leftmost, frame.hands.rightmost
			rel_x_velocity = right.palm_velocity.x - left.palm_velocity.x
			rel_orient = left.palm_normal.x*right.palm_normal.x

			if rel_orient < 0 and rel_x_velocity > 100:
				gesture_flag = True
				gesture_name = "Clear Space"
				if( self.detected_gestures['type'] != gesture_name):
					parameters['start'] = frame.id
				parameters['Left Normal'] = left.palm_normal
				parameters['Left position'] = left.palm_position
				parameters['Right position'] = right.palm_position
				parameters['Right Normal'] = right.palm_normal

				#self.update_gesture("Clear Space", parameters)

				# Define parameters to characterise the gesture.
				
		elif hand_count == 1:
			# Check for the following gestures: point, #to be added soon
			extended_fingers = frame.fingers.extended()
			
			finger_count = len(extended_fingers)
			if finger_count == 1 and extended_fingers[0].type == 1:
				#index_tip_vel = FingerTipVelocity(self, controller)
				gesture_name = "Point"
				if self.detected_gestures['type'] != gesture_name:
					parameters['start'] = frame.id	
				gesture_flag = True

				forward_finger = extended_fingers[0]
				point_from = forward_finger.stabilized_tip_position
				point_to = forward_finger.direction.normalized
				parameters = {'current frame': frame.id, 'from':point_from, 'to':point_to}
				# Return the position on screen being pointed by the
				# forward most finger
			
		print('Frame: %d' %(frame.id))
		if( not gesture_flag):
			none_gesture = {'type': "No gesture", 'parameters':{'start':None} }
			self.detected_gestures.update(none_gesture)
		else:
			self.detected_gestures['type'] = gesture_name
			self.detected_gestures['parameters'].update(parameters)
			self.gesture_data()

#		if self.detected_gestures['type'] == "Clear Space":
#			print("Frame: %d Current Gesture: %s" %(frame.id, gesture_detected))
#			# Send the relevant parameters across to openGL
#		elif self.detected_gestures['type'] == "Point":
#			print("Frame: %d Current Gesture: %s, Finger type: %s,"
#			%(frame.id, self.detected_gesture['type'], self.finger_names[forward_finger.type]))
#			print("Finger-tip-position:", point_from.to_tuple())
#			print("Pointing to:", point_to.to_tuple()) 


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
		print("Thank you for trying our program")

if __name__ == '__main__':
	main()
