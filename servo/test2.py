from time import sleep
from adafruit_servokit import ServoKit
import math
import sys
import traceback

kit = ServoKit(channels=16)

pan = kit.servo[0]
tilt = kit.servo[1]

pan.set_pulse_width_range(540, 2640)
tilt.set_pulse_width_range(540, 2640)

def min(servo):
    servo.angle = 0

def mid(servo):
    servo.angle = 90

def max(servo):
    servo.angle = 180

# Transforms a number from the range [-1, 1] to range [0, 180]
def linear_transform(number):
    try:
        assert number >= -1 and number <= 1
    except AssertionError as e:
        traceback.print_exc()
        print('linear_transform: number ' + str(number) + ' out of range [-1, 1]')
        sys.exit(1)

    return 90 * (number + 1)


mid(pan)
max(tilt)
sleep(2)

while True:
    for i in range(0, 360):
        pan.angle = linear_transform(math.sin(math.radians(i)))
        tilt.angle = linear_transform(math.cos(math.radians(i)))
        sleep(0.01)