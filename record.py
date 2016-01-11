#!/usr/bin/env python

from time import sleep


from kettler import *
from tcx import *

ergo=kettler()
workout=tcx()

def record_workout(intervall=5,timeout=300):
	ergo.reset()
	program_times=ergo.read_programs()

	#first wait for recording to start:
	#TODO: distancemode
	#Question: countdown mode?
	starttimes=[0]+[x*60 for x in program_times]
	print(starttimes)
	while True:
		print("waiting for activity")
		point=ergo.status()
		print(point)
		workouttime=point["workouttime"]
		if workouttime not in starttimes:
			break
		sleep(intervall)
		#TODO: timeout

	workout.add_activity()

	#check if program is selected:
	#TODO: get real starting time, maybe implement in kettler()
	if workouttime>600:
		countdown=True
		#offset by up to intervall seconds
		fromtime=workouttime
		#offset by up to intervall seconds
		workout.set_starttime(time())
	else:
		#calculate accurate starttime, could be offset by intervall
		workout.set_starttime(time()-workouttime)
		countdown=False

	#start recording
	while True:
		print(str(time())+ "recording")
		if countdown:
			point['workouttime']=fromtime-point['workouttime']
		workout.add_trackpoint(point)

		sleep(intervall)
		#updating timestamps:
		point=ergo.status()
		print(point)
		lastworkouttime=workouttime
		workouttime=point["workouttime"]

		#if the workouttime has not changed from last time, the workout is finished. Could be extended to stop/start laps in the future
		if lastworkouttime==workouttime:
			print("Stopping recording")
			break



def test_workout():
	workout.add_activity()
	workout.set_starttime(time())
	workout.add_trackpoint({"workouttime":5,"DistanceMeters":100,"Speed":10,"Watts":200})
	workout.add_trackpoint({"workouttime":7,"DistanceMeters":200,"Speed":20,"Calories":100})

#test_workout()
record_workout()

workout.write_xml("workout.tcx")
