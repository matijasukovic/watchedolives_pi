from gpiozero import OutputDevice
from time import sleep

laser = OutputDevice(17)

laser.on()
while True:
    sleep(1)

