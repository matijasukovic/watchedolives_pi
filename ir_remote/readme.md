Each button of an IR remote outputs a hex code. To download a piece of software that helps map these codes to more meaningful names, do:

git clone https://github.com/Lime-Parallelogram/IR-Code-Decoder--.git
cd IR-Code-Decoder--
python3 GUI.py

A window will pop up, first asking you to type the receiver pin your IR sensor is connected to. Have in mind that developer is asking for the positional number, not the GPIO number. For example, if you connect the IR sensor to GPIO 17, its position on the Raspberry Pi 4 board is 11, so you need to type that number.

