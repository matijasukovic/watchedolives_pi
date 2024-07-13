from picamera2 import Picamera2, Preview
from gpiozero import Button
from signal import pause
from libcamera import controls
from time import sleep
from threading import Event
import argparse

INDEX = 0
PATH = "/home/matijasukovic/projects/WatchedOlives/datagen/pictures/"
FILENAME = "image"
EXTENSION = ".png"
AUTOPLAY_DELAY = 1

autoplay = Event()

camera = Picamera2()

singleShotButton = Button(17)

autoplayButton = Button(27)

def main():
    global FILENAME

    parser = argparse.ArgumentParser()
    parser.add_argument("-op", "--output-path", help="Path to the output directory.", required=True)
    parser.add_argument("-f", "--filename", help="Filename for the images. If not set, defaults to the directory name.")
    parser.add_argument("-e", "--extension", help="File format to save the images as.", choices=['png', 'jpg'],default="png")
    parser.add_argument("-ad", "--autoplay-delay", help="Delay between taking photos during autoplay.", type=float, default=1)

    args = parser.parse_args()

    if not args.filename:
        args.filename = getFilenameFromOutputPath(args.output_path)

    # Show low-res in preview, save as full HD
    preview_config = camera.create_preview_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (854, 480),},
        display="lores"
    )
    camera.configure(preview_config)

    camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    FILENAME = input("Enter name of saved files: ")

    camera.start_preview(Preview.QTGL)
    camera.start()

    runAutoplay()

    singleShotButton.when_pressed = capture
    autoplayButton.when_pressed = runAutoplay

    pause()

def getFilenameFromOutputPath(output_path):
    print(output_path)

def capture():
    global INDEX

    save_path = PATH + FILENAME + '_' + str(INDEX) + EXTENSION
    camera.capture_file(save_path)
    print('saved as: ' ,save_path)

    INDEX = INDEX + 1

def runAutoplay():
    
    capture()
    sleep(AUTOPLAY_DELAY)
    runAutoplay()

if __name__ == '__main__':
    main()