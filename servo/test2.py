from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import math

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

servo1.mid()
servo2.max()
sleep(2)

while True:
    for i in range(0, 360):
        servo1.value = math.sin(math.radians(i))
        servo2.value = math.cos(math.radians(i))
        sleep(0.01)