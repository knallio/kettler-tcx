#!/usr/bin/env python

import serial
import time

class kettler():

	commands={
		'RESET':('RS',"reset device"),
		'ID': ('ID',"Get device ID"),
		'FIRMWARE':('VE',"Get device firmware"),
		'STATUS':('ST',"Get status (relevant for recording)"),
		'PROGRAMS':('RP',"Get programs"),
		'COMMANDMODE':('CM',"Enter command mode"),
		'SET_POWER':('PW',"Request power of x watts"),
		'SET_TIME':('PT', "Request time of mmss"),
		'SET_DISTANCE':('PD',"Request x/10 km distance")
	}


	def __init__(self,port='/dev/ttyUSB0'):
		self.ser = serial.Serial()
		self.ser.baudrate = 9600
		self.ser.port = port
		self.ser.timeout = 20
		self.ser.open()

	def reset(self):
		print("Reset: " + self.send_command(self.commands['RESET'][0]).decode('utf-8'))
		print(self.ser.readline())

	def send_command(self,command_code=None,command_string=None):
		if not command_code:
			command_code=self.commands(command_string)(0)
		self.ser.write(bytearray(command_code+'\r\n','UTF-8'))
		response=self.ser.readline()
		#TODO: error-code
		return response

	def status(self):
		state=self.send_command(self.commands['STATUS'][0])
		numbers=state.decode('utf-8').split('\t')
		state={	"HeartRateBpm" :	int(numbers[0]),
			"Cadence"	:	int(numbers[1]),
			"Speed"	:	int(numbers[2])*100/3600, # 0.1km/h in m/s
			"DistanceMeters":	int(numbers[3])*100, # 0.1 km in m
			"Watts"	:	int(numbers[4]),
			"Calories":	int(numbers[5])*0.239006, # kJ in kcal
			"workouttime"	:	60*int(numbers[6].split(':')[0])+int(numbers[6].split(':')[1]), # in seconds
			"act_power":	int(numbers[7])}
		return state

def main():
	ergo=kettler()

if __name__ == "__main__":
	main()
