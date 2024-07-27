from time import sleep
from adafruit_servokit import ServoKit

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

def testServo(servo):
    min(servo)
    print(servo.angle)
    sleep(2)
    max(servo)
    print(servo.angle)
    sleep(2)
    mid(servo)
    print(servo.angle)
    sleep(2)

testServo(pan)
testServo(tilt)

mid(pan)
mid(tilt)

