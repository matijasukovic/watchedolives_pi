#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Original Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#

from gpiozero import InputDevice
from datetime import datetime
from time import sleep

pin = 27

Buttons = [
	0x300ff18e7, 
    0x300ff4ab5, 
    0x300ff10ef, 
    0x300ff5aa5, 
    0x300ff38c7, 
    0x300ffa25d, 
    0x300ff629d, 
    0x300ffe21d, 
	0x300ff22dd,
	0x300ff02fd,
	0x300ffc23d,
	0x300ffe01f,
	0x300ffa857,
	0x300ff906f,
	0x300ff9867,
	0x300ff6897,
	0x300ffb04f
]

ButtonsNames = [
	"up", 
	"down", 
	"left",
	"right",
	"ok",
	"1",
	"2",
	"3",
	"4",
	"5",
	"6",
	"7",
	"8",
	"9",
	"0",
	"star",
	"hash"
]

# Sets up GPIO
ir_receiver = InputDevice(pin)

# Gets binary value


def getBinary():
	num1s = 0  # Number of consecutive 1s read
	binary = 1  # The binary value
	command = []  # The list to store pulse times in
	previousValue = 0 
	value = ir_receiver.value

	# Waits for the sensor to pull pin low
	while value:
		sleep(0.0001) # This sleep decreases CPU utilization immensely
		value = ir_receiver.value
		
	startTime = datetime.now()
	
	while True:
		# If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime # Calculate the time of pulse
			startTime = now # Reset start time
			command.append((previousValue, pulseTime.microseconds)) # Store recorded data
			
		# Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		# Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		# Re-reads pin
		previousValue = value
		value = ir_receiver.value
		
	# Converts times to binary
	for (type, time) in command:
		if type == 1: # If looking at rest period
			if time > 1000: # If pulse greater than 1000us
				binary = binary *10 +1 # Must be 1
			else:
				binary *= 10 # Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
# Convert value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
	return hex(tmpB2)
	
while True:
	inData = convertHex(getBinary()) # Runs subs to get incoming hex value
	for button in range(len(Buttons)):# Runs through every value in list
		if hex(Buttons[button]) == inData: # Checks this against incoming
			print(ButtonsNames[button]) # Prints corresponding english name for button