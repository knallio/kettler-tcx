#!/usr/bin/env python

from time import sleep


from kettler import *
from tcx import *

ergo=kettler()
workout=tcx()

def record_workout(intervall=5,timeout=300):
	ergo.reset()

	workout.add_activity()

	waiting=True
	recording=False
	finished=False
	workouttime=0
	while (waiting or recording) and not finished:
		print(time())
		if waiting:
			print("waiting for activity")

		point=ergo.status()
		#updating timestamps:
		lastworkouttime=workouttime
		workouttime=point["workouttime"]

		#workouttime has to be greater than 0 to start recording
		if workouttime>0:
			if waiting:
				print("Start recording workout")
				#calculate accurate starttime, could be offset by intervall
				workout.set_starttime(time()-workouttime)
				waiting=False
				recording=True
			workout.add_trackpoint(point)

		#if the workouttime has not changed from last time, the workout is finished. Could be extended to stop/start laps in the future
		if recording and lastworkouttime==workouttime:
			finished=True

		#mainly for developing without workouts
		if waiting and time()-workout.starttime>timeout:
			finished=True

		sleep(intervall)



def test_workout():
	workout.add_activity()
	workout.set_starttime(time())
	workout.add_trackpoint({"workouttime":5,"DistanceMeters":100,"Speed":10,"Watts":200})
	workout.add_trackpoint({"workouttime":7,"DistanceMeters":200,"Speed":20,"Calories":100})

#test_workout()
record_workout()


#workout.set_id()
#workout.set_starttime()
#workout.set_totaltime()


workout.write_xml("filename.xml")
