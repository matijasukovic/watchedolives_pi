from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

pan = kit.servo[0]
tilt = kit.servo[1]

pan.set_pulse_width_range(540, 2640)
tilt.set_pulse_width_range(540, 2640)

def mid(servo):
    servo.angle = 90

mid(kit.servo[0])
mid(kit.servo[1])