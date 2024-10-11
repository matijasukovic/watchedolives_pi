from time import sleep
from pynput import keyboard
from gpiozero import OutputDevice

laser = OutputDevice(17)

from classes.laser_head import LaserHead

head = LaserHead()

pan_minRange = 540
pan_maxRange = 2640

tilt_minRange = 540
tilt_maxRange = 2640

step = 0

def on_press(key):
	global pan_minRange
	global pan_maxRange
	global tilt_minRange
	global tilt_maxRange

	global step
	
	increment = 5

	if key == keyboard.Key.esc:
		laser.off()
		head.pan.mid()
		head.tilt.mid()
		return False  # stop listener

	try:
		k = key.char  # single-char keys
	except:
		k = key.name  # other keys

	if step == 0:
		head.pan.mid()
		sleep(0.25)
		if k == 'down':
			pan_minRange -= increment
			head.pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			head.pan.min()
			print('Pan minimum Reduced: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'up':
			pan_minRange += increment
			head.pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			head.pan.min()
			print('Pan minimum Increased: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'enter':
			print('Pan minimum Saved. ({0}, {1})'.format(pan_minRange, pan_maxRange))

			step += 1
			print('Starting step {0} - Setting pan maximum.'.format(step))
	elif step == 1:
		head.pan.mid()
		sleep(0.25)
		if k == 'down':
			pan_maxRange -= increment
			head.pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			head.pan.max()
			print('Pan maximum Reduced: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'up':
			pan_maxRange += increment
			head.pan.set_pulse_width_range(pan_minRange, pan_maxRange)
			head.pan.max()
			print('Pan maximum Increased: ({0}, {1})'.format(pan_minRange, pan_maxRange))
		elif k == 'enter':
			print('Pan maximum Saved. ({0}, {1})'.format(pan_minRange, pan_maxRange))

			step += 1
			print('Starting step {0} - Setting tilt minimum.'.format(step))
	elif step == 2:
		head.tilt.mid()
		sleep(0.25)
		if k == 'down':
			tilt_minRange -= increment
			head.tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			head.tilt.min()
			print('Tilt minimum Reduced: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'up':
			tilt_minRange += increment
			head.tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			head.tilt.min()
			print('Tilt minimum Increased: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'enter':
			print('Tilt minimum Saved. ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

			step += 1
			print('Starting step {0} - Setting tilt maximum.'.format(step))
	elif step == 3:
		head.tilt.mid()
		sleep(0.25)
		if k == 'down':
			tilt_maxRange -= increment
			head.tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			head.tilt.max()
			print('Tilt maximum Reduced: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'up':
			tilt_maxRange += increment
			head.tilt.set_pulse_width_range(tilt_minRange, tilt_maxRange)
			head.tilt.max()
			print('Tilt maximum Increased: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))
		elif k == 'enter':
			print('Tilt maximum Saved. ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

			print()
			print('Pan range: ({0}, {1})'.format(pan_minRange, pan_maxRange))
			print('Tilt range: ({0}, {1})'.format(tilt_minRange, tilt_maxRange))

	

head.pan.mid()
head.tilt.mid()

def main():
	global pan_minRange
	global pan_maxRange
	global tilt_minRange
	global tilt_maxRange

	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread
	listener.join()  # remove if main thread is polling self.keys





if __name__ == '__main__':
	main()