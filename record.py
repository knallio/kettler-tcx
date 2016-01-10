import serial
from time import sleep


from kettler import kettler
from tcx import *

ergo=kettler()
#ergo.reset()

workout=tcx()
workout.add_activity()

def record_workout(intervall=5,timeout=100):

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
				workout.starttime=time()-workouttime
				waiting=False
				recording=True
			workout.add_trackpoint(point)

		#if the workouttime has not changed from last time, the workout is finished. Could be extended to stop/start laps in the future
		if recording and lastworkouttime==workouttime:
			finished=True

		#mainly for developing without workouts
		if time()-workout.starttime>timeout:
			finished=True

		sleep(intervall)


record_workout()

#workout.add_trackpoint({"workouttime":5})
#workout.add_trackpoint({"workouttime":7})
workout.set_id()
workout.set_starttime()
workout.set_totaltime()

workout.write_xml("filename.xml")
