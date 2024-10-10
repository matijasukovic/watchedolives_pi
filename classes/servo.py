from time import sleep

class Servo:
    def __init__(self, servo):
        # takes in a servo from adafruit_servokit's ServoKit.servo[] 
        self.servo = servo

    def set_pulse_width_range(self, min_pulse, max_pulse):
        self.servo.set_pulse_width_range(min_pulse, max_pulse)

    def min(self):
        self.servo.angle = 0

    def mid(self):
        self.servo.angle = 90

    def max(self):
        self.servo.angle = 180

    def getAngle(self):
        return self.servo.angle
    
    def setAngle(self, angle):
        self.servo.angle = angle