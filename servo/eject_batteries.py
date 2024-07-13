from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

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

servo1.value = -1
servo2.value = 1
sleep(2)

for i in range(100):
    servo1.value = -0.5
    servo2.value=0.95
    sleep(0.01)
    servo1.value = -1
    servo2.value = 1
    sleep(0.01)

sleep(1)
servo1.mid()
servo2.mid()