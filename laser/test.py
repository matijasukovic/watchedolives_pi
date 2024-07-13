from gpiozero import OutputDevice
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

laser = OutputDevice(17)

while True:
    laser.on()
    sleep(1)
    laser.off()
    sleep(1)


