from picamera2 import Picamera2, Preview
from libcamera import controls

from adafruit_servokit import ServoKit

from gpiozero import OutputDevice

from pynput import keyboard

# Servo setup

kit = ServoKit(channels=16)

pan = kit.servo[0]
tilt = kit.servo[1]

print(pan.angle)

pan.set_pulse_width_range(540, 2640)
tilt.set_pulse_width_range(540, 2640)

def min(servo):
	servo.angle = 0

def mid(servo):
	servo.angle = 90

def max(servo):
	servo.angle = 180

# Laser setup

laser = OutputDevice(17)

# Camera setup

camera = Picamera2()

def capture():
	return camera.capture_array()

index = 0
def captureAndSave():
	global index

	save_path = 'test_' + str(index) + '.png'
	camera.capture_file(save_path)
	print('saved as: ' ,save_path)

	index = index + 1


def on_press(key):
	if key == keyboard.Key.esc:
		laser.off()
		mid(pan)
		mid(tilt)
		return False  # stop listener

	try:
		k = key.char  # single-char keys
	except:
		k = key.name  # other keys

	if k in ['left', 'right', 'up', 'down', 'enter', '0']:  # keys of interest
		controlDevice(k)
	elif k in ['space']:
		captureAndSave()


def controlDevice(button):
	increment = 0.5

	if button == "up" and tilt.angle + increment < 180:
		tilt.angle += increment
		print('tilt up', tilt.angle)
	elif button == "down" and tilt.angle - increment > 0:
		tilt.angle -= increment
		print('tilt down ', tilt.angle)
	elif button == "left" and pan.angle + increment < 180:
		pan.angle += increment
		print('pan left ', pan.angle)
	elif button == "right" and pan.angle - increment > 0:
		pan.angle -= increment
		print('pan right ', pan.angle)
	elif button == "enter":
		laser.toggle()
	elif button == '0':
		laser.off()
		mid(pan)
		mid(tilt)


def main():
	mid(pan)
	mid(tilt)

	preview_config = camera.create_preview_configuration(
		main={"size": (1920, 1920)},
		lores={"size": (1920, 1920)},
		display="lores"
	)
	camera.configure(preview_config)

	camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

	camera.start_preview(Preview.QTGL)
	camera.start()

	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread
	listener.join()  # remove if main thread is polling self.keys   
	
if __name__ == '__main__':
	main()