from picamera2 import Picamera2, Preview
from signal import pause
from libcamera import controls
from time import sleep

camera = Picamera2()

def main():
    preview_config = camera.create_preview_configuration(
        main={"size": (1920, 1920)},
        lores={"size": (480, 480),},
        display="lores"
    )
    camera.configure(preview_config)

    camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    camera.start_preview(Preview.QTGL)
    camera.start()
    pause()

if __name__ == '__main__':
    main()