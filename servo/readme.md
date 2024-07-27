# Raspberry Pi 4B

Because we are using PiGPIOFactory to enable hardware timed PMW, we need to run 'sudo pigpiod' before running the servo code.
Alternatively, we can enable this on boot of our Raspberry, using 'sudo systemctl enable pigpiod'.

Default minimum and maximum pulse width for SG90 servos are 0.001 and 0.002 respectively.
However, it isn't common for these to be badly calibrated in a servo. If your servo is not rotating all the way,
decrease the minimumPulseWidth variable, and increase maximumPulseWidth.

Code with the suffix 'legacy' can be used with Pi 4 in the above described way.


# Raspberry Pi 5

Because pigpio is not developed anymore and does not work on Pi 5 currently, we need a PCA9685 module in order to generate hardware
timed PMW. If external power is not available, plug the V+ pin of the PCA into the 5V pin of the Raspberry. With two servos attached
to PCA, it seems to be working okay. 