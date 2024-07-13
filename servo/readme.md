Because we are using PiGPIOFactory to enable hardware timed PMW, we need to run 'sudo pigpiod' before running the servo code.
Alternatively, we can enable this on boot of our Raspberry, using 'sudo systemctl enable pigpiod'.

Default minimum and maximum pulse width for SG90 servos are 0.001 and 0.002 respectively.
However, it isn't common for these to be badly calibrated in a servo. If your servo is not rotating all the way,
decrease the minimumPulseWidth variable, and increase maximumPulseWidth.