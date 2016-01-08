import serial
import time

RESET=b'RS\r\n'
ID=b'ID\r\n'
FIRMWARE=b'VE\r\n'
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
ser.timeout = 10


print(ser)
ser.open()
print(ser)

#ser.write(RESET)


ser.write(ID)
id=ser.readline()
print(id)

ser.write(FIRMWARE)
firmware=ser.readline()
print(firmware)


ser.write(PROGRAMS)
programs=ser.readline()
print(programs)

running=True


#while running:
#	ser.write(STATUS)
#	status=ser.readline()
#	print(status)
#	time.sleep(5)
