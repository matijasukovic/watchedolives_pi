from gpiozero import Servo, InputDevice, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from datetime import datetime

# step for each move
# servo position is a value between -1 and 1
increment = 0.1
cm = 0

# ------ Set up servos -------
servoFactory = PiGPIOFactory()

minimumPulseWidth = 0.5/1000
maximumPulseWidth = 2.5/1000

servo1 = Servo(
    12, 
    pin_factory=servoFactory,
    min_pulse_width=minimumPulseWidth,
    max_pulse_width=maximumPulseWidth
)

servo2 = Servo(
    13, 
    pin_factory=servoFactory,
    min_pulse_width=minimumPulseWidth,
    max_pulse_width=maximumPulseWidth
)
# ------ ---------------- -------

# ----------- set up laser ------------

laser = OutputDevice(17)

# ------ Set up and functions of IR remote -------
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
# ------- ----------------------- -------------

# ------- Servo controll ------
def controllServo(button):
	global increment
	global cm

	if button == "up" and servo2.value + increment < 1:
		cm += 1
		
		servo2.value += increment
	elif button == "down" and servo2.value - increment > -1:
		servo2.value -= increment
	elif button == "left" and servo1.value + increment < 1:
		servo1.value += increment
	elif button == "right" and servo1.value - increment >=-1:
		servo1.value -= increment
	elif button == "ok":
		laser.toggle()
	elif button == '0':
		laser.off()
		servo1.mid()
		servo2.mid()
	# else:
	# 	increment = updateIncrement(int(button))

def updateIncrement(number):
	return number/100
# -----------------------------

# Main code

servo1.mid()
servo2.mid()

while True:
	inData = convertHex(getBinary()) # Runs subs to get incoming hex value
	for button in range(len(Buttons)):# Runs through every value in list
		if hex(Buttons[button]) == inData: # Checks this against incoming
			print(ButtonsNames[button]) # Prints corresponding english name for button
			controllServo(ButtonsNames[button])
