from time import sleep
from adafruit_servokit import ServoKit
import math
import sys
import traceback

from classes.laser_head import LaserHead

head = LaserHead()

# Transforms a number from the range [-1, 1] to range [0, 180]
def linear_transform(number):
    try:
        assert number >= -1 and number <= 1
    except AssertionError as e:
        traceback.print_exc()
        print('linear_transform: number ' + str(number) + ' out of range [-1, 1]')
        sys.exit(1)

    return 90 * (number + 1)


head.pan.mid()
head.tilt.max()
sleep(1)

for k in range(0, 3):
    for i in range(0, 360):
        head.pan.setAngle(linear_transform(math.sin(math.radians(i))))
        head.tilt.setAngle(linear_transform(math.cos(math.radians(i))))
        sleep(0.01)

sleep(1)
head.reset()