#!/usr/bin/env python

from time import sleep,strftime

from kettler import *
from tcx import *

class recorder():

	ergo=kettler()
	workout=tcx()

	intervall=5
	timeout=600

	def start(self):
		self.ergo.reset()
		if (self.wait_for_workout()):
			self.record_workout()

	def wait_for_workout(self):
		starttime=time()
		while True:
			print ("\rWaiting for workout: "+ str(round(time()-starttime)) + "s", end="")
			if self.ergo.is_active():
				print()
				return True
			if time()-starttime > self.timeout:
				print()
				return False
			sleep(self.intervall)

	def record_workout(self):

		starttime=self.ergo.starttime
		self.workout.add_activity(start=starttime)

		#start recording
		while True:
			print("\rRecording: " + str(round(time()-starttime)) + "s",end='')
			tcxpoint=self.kettler_to_tcx(self.ergo.get_state())
			self.workout.add_trackpoint(tcxpoint)

			sleep(self.intervall)
			#is_active reads the state
			if not self.ergo.is_active():
				print()
				break

	def kettler_to_tcx(self,kettlerstate):
		#convert kettler state to tcx trackpoint
		tcxpoint={	"Time"		: 	kettlerstate['time'],
				"HeartRateBpm"	:	kettlerstate['pulse'],
				"Cadence"	:	kettlerstate['rpm'],
				"Speed"		:	kettlerstate['speed']*100/3600,	# 0.1km/h in m/s
				"DistanceMeters":	kettlerstate['distance']*100,		# 0.1 km in m
				"AltitudeMeters":	kettlerstate['power'],			# hack to show Watts in endomondo
				"Calories"	:	kettlerstate['energy']*0.239006,	# kJ in kcal
				"TotalTimeSeconds":	kettlerstate['runtime']		# in seconds
			}
		return tcxpoint


	def test_workout(self):
		self.workout.add_activity()
		self.workout.set_starttime(time())
		self.workout.add_trackpoint({"workouttime":5,"DistanceMeters":100,"Speed":10,"Watts":200})
		self.workout.add_trackpoint({"workouttime":7,"DistanceMeters":200,"Speed":20,"Calories":100})

	def save(self,filename="Ergo_"+strftime("%Y_%m_%d")+".tcx"):
		self.workout.write_xml(filename)


def main():
	print("kettler recording script")
	rec=recorder()
	rec.start()
	rec.save()


if __name__ == "__main__":
	main()





