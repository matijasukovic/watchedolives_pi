from gpiozero import OutputDevice
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

laser = OutputDevice(17)

laser.on()
while True:
    sleep(1)

