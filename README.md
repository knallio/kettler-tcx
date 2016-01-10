# kettler-tcx
Generate tcx files from Kettler ergometer

#Status
Proof of principle. Basic functionality is implemented, still some parts missing. 

#Installation
Nothing fancy. Download in some folder...

#Usage
Connect Kettler Ergometer with usb or serial port. Set serial port in source code, if necessary. Defaults to '/dev/ttyUSB0'.

Start record.py. The script resets the ergometer and waits for activity (timer on ergometer starts running). The script records until activity stops (timer on ergometer does not 
change for 5 seconds). Afterwards the workout is saved to workout.tcx (will be changed later)
