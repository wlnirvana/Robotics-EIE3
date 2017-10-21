import brickpi
import time
import json
import math

class Robot:
	def __init__(self, interface, config_file="config.json"):
		self.motors = [0,1]
		self.motorParams = {}
		self.interface = interface
		self.left_speed = 0
		self.right_speed = 0
		self.wheel_diameter = 5.3 #cm
		self.circumference = self.wheel_diameter * math.pi

		#Enabling the motors
		self.interface.motorEnable(self.motors[0])
		self.interface.motorEnable(self.motors[1])

		#Open the config file
		data = None
	    	with open("config.json") as data_file:
    			data = json.load(data_file)
		# Configure motor calibration constants
		self.distance_calibration = data.get("distance_calibration", 3.05)
		self.angle_calibration = data.get("angle_calibration", 0.13)

		#Configuring the left motor
		self.motorParams["left"] = self.interface.MotorAngleControllerParameters()
		self.motorParams["left"].maxRotationAcceleration = data["left"]["maxRotationAcceleration"]
		self.motorParams["left"].maxRotationSpeed = data["left"]["maxRotationSpeed"]
		self.motorParams["left"].feedForwardGain = data["left"]["feedForwardGain"]
		self.motorParams["left"].minPWM = data["left"]["minPWM"]
		self.motorParams["left"].pidParameters.minOutput = data["left"]["minOutput"]
		self.motorParams["left"].pidParameters.maxOutput = data["left"]["maxOutput"]
		self.motorParams["left"].pidParameters.k_p = data["left"]["k_p"]
		self.motorParams["left"].pidParameters.k_i = data["left"]["k_i"]
		self.motorParams["left"].pidParameters.k_d = data["left"]["k_d"]

		#Configure the right motor
		self.motorParams["right"] = self.interface.MotorAngleControllerParameters()
		self.motorParams["right"].maxRotationAcceleration = data["right"]["maxRotationAcceleration"]
		self.motorParams["right"].maxRotationSpeed = data["right"]["maxRotationSpeed"]
		self.motorParams["right"].feedForwardGain = data["right"]["feedForwardGain"]
		self.motorParams["right"].minPWM = data["right"]["minPWM"]
		self.motorParams["right"].pidParameters.minOutput = data["right"]["minOutput"]
		self.motorParams["right"].pidParameters.maxOutput = data["right"]["maxOutput"]
		self.motorParams["right"].pidParameters.k_p = data["right"]["k_p"]
		self.motorParams["right"].pidParameters.k_i = data["right"]["k_i"]
		self.motorParams["right"].pidParameters.k_d = data["right"]["k_d"]

		self.interface.setMotorAngleControllerParameters(self.motors[0],self.motorParams["left"])
		self.interface.setMotorAngleControllerParameters(self.motors[1],self.motorParams["right"])

		self.interface.setMotorRotationSpeedReferences(self.motors,[self.left_speed,self.right_speed])

	# Move specified wheel a certain distance
	def move_wheels(self, distances=[1,1], wheels=[0,1]):
		print("Distance to move wheels: {}".format(distances))

		# Retrieve start angle of motors
		motorAngles_start = self.interface.getMotorAngles(wheels)
		print("Start Angles: {}".format(motorAngles_start))

		# Set the reference angles to reach
		circular_distances = [round((2*x*self.distance_calibration)/self.circumference,2) for x in distances]
		print("Distance in radians: {}".format(circular_distances))
		motorAngles_end = []

		motorAngles_end.append(round(motorAngles_start[0][0] + circular_distances[0],2))
		motorAngles_end.append(round(motorAngles_start[1][0] + circular_distances[1],2))
		print("Angles to end at: {}".format(motorAngles_end))

		self.interface.increaseMotorAngleReferences(wheels, circular_distances)

		# This function does PID control until angle references are reached
		while not self.interface.motorAngleReferencesReached(wheels):
			time.sleep(0.1)
			print(self.interface.getMotorAngles(wheels))
			if (round(self.interface.getMotorAngles(wheels)[0][0],2)==motorAngles_end[0] or round(self.interface.getMotorAngles(wheels)[1][0],2)==motorAngles_end[1]):
				return True
		return True

	#Takes the distance in centimeters and moves it forward
	def travel_straight(self, distance):
		return self.move_wheels([distance,distance], [0,1])

	#Takes the angle in degrees and rotates the robot right
	def rotate_right(self, angle):
		dist = self.angle_calibration*angle
		return self.move_wheels([-dist,dist])

	#Takes the angle in degrees and rotates the robot left
	def rotate_left(self, angle):
		self.rotate_right(-angle)

	def calibrate(self, radians,angle):
		#So that we always start calibrating approximately at zero
		motorAngles = self.interface.getMotorAngles(self.motors)
		motorAngles_zero = (round(0-motorAngles[0][0],2), round(0-motorAngles[1][0],2))
		self.interface.increaseMotorAngleReferences(self.motors,[motorAngles_zero[0],motorAngles_zero[1]])
		while not self.interface.motorAngleReferencesReached(self.motors):
			motorAngles = self.interface.getMotorAngles(self.motors)
			if motorAngles:
				print "Motor angles calibrating to 0: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)

		self.interface.startLogging("motor_position_0_"+str(int(angle))+".log")
		self.interface.increaseMotorAngleReferences(self.motors,[radians,radians])
         	while not self.interface.motorAngleReferencesReached(self.motors):
			motorAngles = self.interface.getMotorAngles(self.motors)
			if motorAngles:
		    	    print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)
		self.interface.stopLogging()
