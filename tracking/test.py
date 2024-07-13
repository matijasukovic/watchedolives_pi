# -- Servos set-up
from gpiozero import Servo, OutputDevice
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

laser = OutputDevice(17)

factory = PiGPIOFactory()

# Defaults are 1/1000 and 2/2000
minimumPulseWidth = 0.5/1000
maximumPulseWidth = 2.5/1000

servo1 = Servo(12, pin_factory=factory,min_pulse_width=minimumPulseWidth,max_pulse_width=maximumPulseWidth)
servo2 = Servo(13, pin_factory=factory,min_pulse_width=minimumPulseWidth,max_pulse_width=maximumPulseWidth)

# -- Camera set-up
from picamera2 import Picamera2
from libcamera import controls

camera = Picamera2()

preview_config = camera.create_preview_configuration(
    main={"size": (1920, 1080)},
    lores={"size": (854, 480),},
    display="lores"
)

camera.configure(preview_config)
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

def capture():
    camera.start()
    camera.capture_file('./image.png')
    print('image captured')

# -- App
import cv2
import numpy as np
import math

def findTargetPointAruco(img):
    imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    arucoDetectionParams = cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoDetectionParams)

    corners, ids, rejected_img_points = arucoDetector.detectMarkers(imgGrayscale)

    if np.all(ids is not None): # If there are markers found by detector
        for i in range(0, len(ids)):
            cv2.aruco.drawDetectedMarkers(img, corners)

        targetPoint = (int(corners[0][0][0][0]), int(corners[0][0][0][1]))

        cv2.circle(img, targetPoint, radius=10, thickness=2, color=(255, 0, 0))

        return targetPoint

def findTargetPointChessboard(img):
    num_intersections_in_x = 6
    num_intersections_in_y = 4

    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(img_grayscale, (num_intersections_in_x, num_intersections_in_y), None)

    if not ret:
        print('Chessboard not found!')
        return None
    
    # drawn_img = cv2.drawChessboardCorners(img, (num_intersections_in_x, num_intersections_in_y), corners, ret)
    # cv2.namedWindow("main", cv2.WINDOW_NORMAL)
    # cv2.imshow("main", drawn_img)
    # cv2.waitKey(0)

    corner1 = (int(corners[0][0][0]), int(corners[0][0][1]))
    corner2 = (int(corners[num_intersections_in_x * num_intersections_in_y - 1][0][0]), int(corners[num_intersections_in_x * num_intersections_in_y - 1][0][1]))
    targetPoint = (int((corner1[0] + corner2[0]) / 2), int((corner1[1] + corner2[1]) / 2))

    cv2.circle(img, corner1, radius=10, thickness=2, color=(255, 0, 0))
    cv2.circle(img, corner2, radius=10, thickness=2, color=(255, 0, 0))
    cv2.circle(img, targetPoint, radius=10, thickness=2, color=(255, 255, 255))

    return targetPoint

def findLaserPoint(img):
    # img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower_range = np.array([240,0,254])
    # upper_range = np.array([255,255,255])

    # mask = cv2.inRange(img_hsv, lower_range, upper_range)

    # points = cv2.findNonZero(mask)

    # try:
    #     #meanVelues will be an array containing the mean x and mean y velues
    #     meanValues = np.mean(points, axis=0)

    #     laserPoint = (int(meanValues[0][0]), int(meanValues[0][1]))
    # except np.exceptions.AxisError:
    #     print('Laser point not found. Returning default')
    #     laserPoint = (795, 522)

    laserPoint = (761, 553)

    cv2.circle(img, laserPoint, radius=10, thickness=2, color=(255, 0, 0))

    return laserPoint

def movePanServo(laserPoint, targetPoint):
    angle_radians = math.atan2(targetPoint[0] - laserPoint[0], laserPoint[1] - targetPoint[1])
    angle_degrees = math.degrees(angle_radians)

    print('pan angle in degrees ',angle_degrees)

    if 0 < angle_degrees < 90:
        # topRight, angle is correct
        normalised_angle = (angle_degrees) / 90.0
    elif -90 < angle_degrees < 0:
        normalised_angle = (angle_degrees) / 90.0
    elif angle_degrees <= -90 :
        # bottomLeft: add 180 degrees to get the opposite angle
        normalised_angle = (angle_degrees + 180) / 90.0
    else:
        # bottomRight: reduce 180 degrees to get the opposite angle
        normalised_angle = (angle_degrees - 180) / 90.0

    print('Pan servo value: ', normalised_angle)
    servo1.value = normalised_angle

def moveTiltServo(laserPoint, targetPoint):
    distance = math.sqrt((laserPoint[0] - targetPoint[0])**2 + (laserPoint[1] - targetPoint[1])**2)

    print(distance)

    #calculated manually
    height = 1300
    
    angle_radians = math.atan2(distance, height)
    angle_degrees = math.degrees(angle_radians)

    if targetPoint[1] < laserPoint[1]:
        angle_degrees *= -1

    normalised_angle = (angle_degrees) / 90.0

    print('Tilt servo value: ', normalised_angle)
    servo2.value = normalised_angle

def main():
    servo1.mid()
    servo2.mid()
    laser.on()

    while True:
        capture()

        img = cv2.imread('image.png')

        laserPoint = findLaserPoint(img)
        targetPoint = findTargetPointAruco(img)

        if not laserPoint or not targetPoint:
            print('Points were not found.')

            print('laserPoint: ', laserPoint)
            print('targetPoint: ', targetPoint)

            # cv2.imshow('image', img)
            # cv2.waitKey(0)
            laser.off()

            continue

        laser.on()
        print('Laser point: ', laserPoint)
        print('Target point: ', targetPoint)

        movePanServo(laserPoint, targetPoint)
        moveTiltServo(laserPoint, targetPoint)

        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # break


        


if __name__ == '__main__':
    main()