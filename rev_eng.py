import serial
import time

RESET=b'RS\r\n'
ID=b'ID\r\n'
FIRMWARE=b've\r\n'
STATUS=b'ST\r\n'

PROGRAMS=b'RP\r\n'
#COMMANDMODE=b'CM\r\n'
#PW x
#Request power of x watts
#PT mmss
#Request time of mmss
#PD x
#Request x/10 km distance


ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.timeout = 2

ser.open()
print(ser)

ser.write(FIRMWARE)
firmware=ser.readline()
print(firmware)

#single char:
for i in range(ord('A'), ord('Z')+1):
	commandcode=chr(i)
	command=bytearray(commandcode+'\r\n','UTF-8')
	ser.write(command)
	response=ser.readline()
	response_string=response.decode('utf-8')
	if 'ERROR' not in response_string:
		print(commandcode)
		print(response_string)

	for j in range(ord('A'), ord('Z')+1):
		commandcode=chr(i)+chr(j)
		command=bytearray(commandcode+'\r\n','UTF-8')
		ser.write(command)
		response=ser.readline()
		response_string=response.decode('utf-8')
		if 'ERROR' not in response_string:
			print(commandcode)
			print(response_string)
		for k in range(ord('A'), ord('Z')+1):
			commandcode=chr(i)+chr(j)+chr(k)
			command=bytearray(commandcode+'\r\n','UTF-8')
			ser.write(command)
			response=ser.readline()
			response_string=response.decode('utf-8')
			if 'ERROR' not in response_string:
				print(commandcode)
				print(response_string)
