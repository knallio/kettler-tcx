#!/usr/bin/env python

from time import sleep

from kettler import *
from tcx import *

class recorder():

	ergo=kettler()
	workout=tcx()

	intervall=5
	timeout=300

	def start(self):
		self.ergo.reset()
		self.wait_for_workout()
		self.record_workout()

	def wait_for_workout(self):
		program_times=self.ergo.read_programs()

		#first wait for recording to start:
		#TODO: distancemode
		#Question: countdown mode?
		starttimes=[0]+[x*60 for x in program_times]
		print(starttimes)
		while True:
			print("waiting for activity")
			point=self.ergo.status()
			print(point)
			workouttime=point["workouttime"]
			if workouttime not in starttimes:
				return True
				break
			sleep(self.intervall)
			#TODO: timeout, 


	def record_workout(self):

		self.workout.add_activity()

		#check if program is selected:
		#TODO: get real starting time, maybe implement in kettler()
		if workouttime>600:
			countdown=True
			#offset by up to intervall seconds
			fromtime=workouttime
			#offset by up to intervall seconds
			self.workout.set_starttime(time())
		else:
			#calculate accurate starttime, could be offset by intervall
			self.workout.set_starttime(time()-workouttime)
			countdown=False

		#start recording
		while True:
			print(str(time())+ "recording")
			if countdown:
				point['workouttime']=fromtime-point['workouttime']
			self.workout.add_trackpoint(point)

			sleep(self.intervall)
			#updating timestamps:
			point=ergo.status()
			print(point)
			lastworkouttime=workouttime
			workouttime=point["workouttime"]

			#if the workouttime has not changed from last time, the workout is finished. Could be extended to stop/start laps in the future
			if lastworkouttime==workouttime:
				print("Stopping recording")
				break

	def kettler_to_tcx(self):
		print("convert kettler status to tcx trackpoint")

	def test_workout(self):
		self.workout.add_activity()
		self.workout.set_starttime(time())
		self.workout.add_trackpoint({"workouttime":5,"DistanceMeters":100,"Speed":10,"Watts":200})
		self.workout.add_trackpoint({"workouttime":7,"DistanceMeters":200,"Speed":20,"Calories":100})

	def save(self):
		self.workout.write_xml("workout.tcx")


def main():
	print("kettler recording script")
	rec=recorder()

	rec.start()
#	rec.save()


if __name__ == "__main__":
	main()





