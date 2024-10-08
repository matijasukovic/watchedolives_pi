from time import sleep
from adafruit_servokit import ServoKit
from pynput import keyboard
from gpiozero import OutputDevice

# Laser setup

laser = OutputDevice(17)

kit = ServoKit(channels=16)

pan = kit.servo[0]
tilt = kit.servo[1]

pan.set_pulse_width_range(540, 2640)
tilt.set_pulse_width_range(540, 2640)

pan_minRange = 540
pan_maxRange = 2640

tilt_minRange = 540
tilt_maxRange = 2640

step = 0

def min(servo):
    servo.angle = 0

def mid(servo):
    servo.angle = 90

def max(servo):
    servo.angle = 180

def on_press(key):
	global pan_minRange
	global pan_maxRange
	global tilt_minRange
	global tilt_maxRange
	
	increment = 10

	if key == keyboard.Key.esc:
		laser.off()
		mid(pan)
		mid(tilt)
		return False  # stop listener

	try:
		k = key.char  # single-char keys
	except:
		k = key.name  # other keys


	if k == 'left':
		pan_minRange -= increment
		min(pan)
		tilt.angle = 45
	elif k == 'right':
		pan_maxRange += increment
		max(pan)
		tilt.angle = 45
	elif k == 'down':
		tilt_minRange -= increment
		min(tilt)
	elif k == 'up':
		tilt_maxRange += increment
		max(tilt)
	elif k == '0':
		laser.toggle()

	pan.set_pulse_width_range(pan_minRange, pan_maxRange)
	tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
	print('pan: (', pan_minRange, ', ', pan_maxRange, ')')
	print('tilt: (', tilt_minRange, ', ', tilt_maxRange, ')')

def newListener(key):
	global pan_minRange
	global pan_maxRange
	global tilt_minRange
	global tilt_maxRange

	global step
	
	increment = 10

	if key == keyboard.Key.esc:
		laser.off()
		mid(pan)
		mid(tilt)
		return False  # stop listener

	try:
		k = key.char  # single-char keys
	except:
		k = key.name  # other keys

	if step == 0:
		mid(pan)
		sleep(0.25)
		if k == 'down':
			pan_minRange -= increment
			pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			min(pan)
			print('Pan minimum Reduced: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'up':
			pan_minRange += increment
			pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			min(pan)
			print('Pan minimum Increased: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'enter':
			print('Pan minimum Saved. ({0}, {1})'.format(pan_minRange, pan_maxRange))

			step += 1
			print('Starting step {0} - Setting pan maximum.'.format(step))
	elif step == 1:
		mid(pan)
		sleep(0.25)
		if k == 'down':
			pan_maxRange -= increment
			pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			max(pan)
			print('Pan maximum Reduced: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'up':
			pan_maxRange += increment
			pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			max(pan)
			print('Pan maximum Increased: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'enter':
			print('Pan maximum Saved. ({0}, {1})'.format(pan_minRange, pan_maxRange))

			step += 1
			print('Starting step {0} - Setting tilt minimum.'.format(step))
	elif step == 2:
		mid(tilt)
		sleep(0.25)
		if k == 'down':
			tilt_minRange -= increment
			tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			min(tilt)
			print('Tilt minimum Reduced: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'up':
			tilt_minRange += increment
			tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			min(tilt)
			print('Tilt minimum Increased: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'enter':
			print('Tilt minimum Saved. ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

			step += 1
			print('Starting step {0} - Setting tilt maximum.'.format(step))
	elif step == 3:
		mid(tilt)
		sleep(0.25)
		if k == 'down':
			tilt_maxRange -= increment
			tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			max(tilt)
			print('Tilt maximum Reduced: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'up':
			tilt_maxRange += increment
			tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			max(tilt)
			print('Tilt maximum Increased: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'enter':
			print('Tilt maximum Saved. ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

			print()
			print('Pan range: ({0}, {1})'.format(pan_minRange, pan_maxRange))
			print('Tilt range: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

	

mid(pan)
mid(tilt)

def main():
	global pan_minRange
	global pan_maxRange
	global tilt_minRange
	global tilt_maxRange

	listener = keyboard.Listener(on_press=newListener)
	listener.start()  # start to listen on a separate thread
	listener.join()  # remove if main thread is polling self.keys





if __name__ == '__main__':
	main()