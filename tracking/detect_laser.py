import cv2
import numpy as np

image_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/test_1.png"

def findLaserPoint(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([160, 70, 242])
    upper_range = np.array([170, 255, 255])

    mask = cv2.inRange(img_hsv, lower_range, upper_range)
    # resized = cv2.resize(mask, (800, 800))
    # cv2.imshow('mask', resized)
    # cv2.waitKey(0)

    points = cv2.findNonZero(mask)

    try:
        meanValues = np.mean(points, axis=0)
        laserPoint = (int(meanValues[0][0]), int(meanValues[0][1]))

    except np.exceptions.AxisError:
        print('Laser point not found.')
        return None

    return laserPoint

def main():
    img = cv2.imread(image_path)

    laserPoint = findLaserPoint(img)

    cv2.circle(img, laserPoint, radius=10, thickness=2, color=(255, 0, 0))

    resized = cv2.resize(img, (800, 800))
    cv2.imshow('img', resized)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()