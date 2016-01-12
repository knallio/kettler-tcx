#!/usr/bin/env python

import serial
from time import time,sleep

class kettler():

	commands={
		#ALIAS:('COMMANDCODE',"description",'example response')
		'RESET':('RS',"reset device",'ACK'),
		'ID': ('ID',"Get device ID",'SDFB3026'),
		'FIRMWARE':('VE',"Get device firmware",'130'),
		'MODEL':('KI','get model name','SDFB    X3'),
		'STATUS':('ST',"Get status (relevant for recording)",'000     000     000     000     025     0000    00:00   000'),
		'RPM':('VS','get current rpm','070'),
		'PROGRAMS':('RP',"Get programs",'32	025	025	050	050	075	075	100	100	125	125	150	150	175	175	200	200	225	225	250	250	275	275	300	300	325	325	350	350	375	375	400	400	27	025	025	050	050	075	075	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	075	075	050	050	025	025	30	050	050	075	075	100	100	125	125	125	125	125	125	125	100	100	100	100	125	125	125	125	125	125	125	100	100	075	075	050	050	36	050	050	075	075	100	100	125	125	150	150	150	150	150	100	100	100	150	150	150	150	150	100	100	100	100	150	150	150	150	150	125	125	100	100	075	075	38	050	050	075	075	100	100	125	125	150	200	100	100	200	100	100	200	100	100	200	100	100	200	100	100	200	100	100	200	100	100	200	175	150	125	100	100	075	075	36	075	075	100	100	125	125	175	100	200	175	225	125	150	175	200	225	300	150	150	175	200	225	200	175	150	125	175	125	175	125	175	150	125	125	100	100	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00'),
		'COMMANDMODE':('CM',"Enter command mode",'ACK or RUN when already active'),
		'COMMANDMODE2':('CD','Enter command mode','ACK or RUN when already active'),
		'SET_POWER':('PW',"set power of x watts",'000     000     000     000     025     0000    00:00   000'),
		'SET_TIME':('PT', "set time of mmss",'000     000     000     000     025     0000    00:00   000'),
		'SET_DISTANCE':('PD',"set x/10 km distance",'000     000     000     000     025     0000    00:00   000'),
		'SET_ENERGY':('PE','set energy of x kJ','000     000     000     000     025     0000    00:00   000'),
		'RESET2':('CP','reset?CP? works after COMMANDMODE','ACK'),
		'UNKNOWN0':('CA','unknown','326'),
		'UNKNOWN1':('ES','unknown',''),
		'UNKNOWN2':('GB','unknown','00000   00000   00000'),
		'UNKNOWN3':('RD','unknown','2	326	1	0	0	0	0	0	1	0	0	1	-1	-1	-1	-1	-1	-1	0	0	025	400	075	030	020	030	040	050	060	070	080	100	120	140	000	040	080	120	180	220	320	400	460	511	003	004	006	010	017	022	033	041	046	048	005	006	011	017	030	040	063	080	089	097	007	009	015	025	044	059	097	124	142	155	009	012	020	034	060	080	133	173	199	219	011	015	025	043	076	102	170	223	260	287	013	019	031	053	094	124	209	275	322	359	016	023	037	063	110	148	250	328	385	430	022	030	050	083	146	194	329	435	514	577	028	038	063	104	181	241	410	545	647	729	035	046	077	127	220	293	496	658	781	882	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1	-1'),
		'UNKNOWN4':('SB','unknown','ACK')
	}

	def __init__(self,port='/dev/ttyUSB0'):
		self.ser = serial.Serial()
		self.ser.baudrate = 9600
		self.ser.port = port
		self.ser.timeout = 20
		self.ser.open()

	def reset(self):
		print("Reset: " + self.send_command('RESET'))
		print(self.ser.readline())

	def send_command(self,command_string=None,command_code=None):
		if not command_code:
			command_code=self.commands[command_string][0]
		self.ser.write(bytearray(command_code+'\r\n','utf-8'))
		response=self.ser.readline()
		#TODO: error-code
		return response.decode('utf-8')

	def read_programs(self):
		response=self.send_command('PROGRAMS')
		response=response.split('\t')
		self.programs=[]
		#not very elegant but works for now
		i=0
		while i<len(response) and int(response[i])>0:
			m=int(response[i])
			self.programs.append((m,[]))
			for x in range(m):
				i+=1
				self.programs[-1][1].append(int(response[i]))
			i+=1
		return list(map(lambda x: x[0],self.programs))

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

	def testmode(self,intervall=5,timeout=60):
		starttime=time()
		while True:
			print("----- "+str(time()-starttime)+ " -----")
			for command in sorted(self.commands):
				if 'RESET' in command:
					continue
				if 'COMMANDMODE' in command:
					continue
				if 'SET_' in command:
					continue
				if command=='PROGRAMS':
					continue
				print(command + " (" + self.commands[command][0]+ "): " + self.send_command(command))
			if time()-starttime>timeout:
				break
			sleep(intervall)


def main():
	print("kettler test script")
	ergo=kettler()

#	print(ergo.read_programs())
#	print(ergo.send_command('UNKNOWN0'))
#	print(ergo.send_command('RESET2'))
#	ergo.testmode(timeout=60)

if __name__ == "__main__":
	main()
