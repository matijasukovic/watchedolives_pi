from picamera2 import Picamera2, Preview
from signal import pause
from libcamera import controls
from time import sleep

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

from gpiozero import OutputDevice

from pynput import keyboard

#Servo setup

factory = PiGPIOFactory()

# Defaults are 1/1000 and 2/2000
minimumPulseWidth = 0.5/1000
maximumPulseWidth = 2.5/1000

servo1 = Servo(
    12, 
    pin_factory=factory,
    min_pulse_width=minimumPulseWidth,
    max_pulse_width=maximumPulseWidth
)

servo2 = Servo(
    13, 
    pin_factory=factory,
    min_pulse_width=minimumPulseWidth,
    max_pulse_width=maximumPulseWidth
)

#Laser setup
laser = OutputDevice(17)

camera = Picamera2()

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener

    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k in ['left', 'right', 'up', 'down', 'enter', '0']:  # keys of interest
        controlServo(k)
    elif k in ['space']:
        capture()


def controlServo(button):
	increment = 0.01

	if button == "up" and servo2.value + increment < 1:
		servo2.value += increment
	elif button == "down" and servo2.value - increment > -1:
		servo2.value -= increment
	elif button == "left" and servo1.value + increment < 1:
		servo1.value += increment
	elif button == "right" and servo1.value - increment >=-1:
		servo1.value -= increment
	elif button == "enter":
		laser.toggle()
	elif button == '0':
		laser.off()
		servo1.mid()
		servo2.mid()

index = 0
def capture():
    global index

    save_path = 'test_' + str(index) + '.png'
    camera.capture_file(save_path)
    print('saved as: ' ,save_path)

    index = index + 1


def main():
    preview_config = camera.create_preview_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (480, 480),},
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