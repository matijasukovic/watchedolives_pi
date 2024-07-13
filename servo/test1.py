from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

def testServo(servo):
    servo.min()
    print(servo.value)
    sleep(2)
    servo.max()
    print(servo.value)
    sleep(2)
    servo.mid()
    print(servo.value)
    sleep(2)

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

testServo(servo1)
testServo(servo2)

servo1.value = None
servo2.value = None

