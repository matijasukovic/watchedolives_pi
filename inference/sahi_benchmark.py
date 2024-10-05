from sahi import AutoDetectionModel
from sahi.predict import get_prediction, get_sliced_prediction
from sahi.utils.file import save_json

import os
import cv2

# Note: In  order to use a NCNN model you need to comment out line 33 from sahi > models > yolov8.py
model_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/models/n_base/weights/best_ncnn_model"
images_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/datasets/rock_detection_v4.5/images/test"
labels_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/datasets/rock_detection_v4.5/labels/test"
export_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/inference/sahi"
visualize = False

def draw_ground_truth(image_path, label_path):
    image = cv2.imread(image_path)
    H, W = image.shape[:2]

    label_file = open(label_path, "r").read()
    labels = [[float(value) for value in label.split()] for label in label_file.split("\n") if label.strip()]

    for label in labels:
        class_id, x_center, y_center, width, height = label
        x1 = int(x_center*W - width*W/2)
        y1 = int(y_center*H - height*H/2)
        x2 = int(x_center*W + width*W/2)
        y2 = int(y_center*H + height*H/2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imwrite(image_path, image)

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=model_path,
    confidence_threshold=0.4,
    device="cpu",
)

result_array = []

for image in os.listdir(images_path):
    image_path = images_path + '/' + image

    filename = str(image)[0:len(str(image)) - 4]
    label_path = labels_path + "/" + filename + '.txt'

    result_sliced = get_sliced_prediction(
        image_path,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0,
        verbose=1
    )

    result_array.append(result_sliced.durations_in_seconds)

    print('Inference time (s): {0}'.format(result_sliced.durations_in_seconds))

    if visualize:
        result_sliced.export_visuals(export_dir=export_path, file_name=filename + '_sliced')
        draw_ground_truth(export_path + "/" + filename + '_sliced.png', label_path)


result_array = result_array[1:]

totalSliceTimeInSeconds = 0
totalPredictionTimeInSeconds = 0

for result in result_array:
    totalSliceTimeInSeconds += result['slice']
    totalPredictionTimeInSeconds += result['prediction']

meanSliceTimeInMilliseconds = totalSliceTimeInSeconds / len(result_array) * 1000
meanPredictionTimeInMilliseconds = totalPredictionTimeInSeconds / len(result_array) * 1000

meanTotalTimeInMilliseconds = meanSliceTimeInMilliseconds + meanPredictionTimeInMilliseconds

print('\nBenchmark results (ms):\n\nSlice: {0}\nPrediction: {1}\nTotal: {2}'.format(
    meanSliceTimeInMilliseconds,
    meanPredictionTimeInMilliseconds,
    meanTotalTimeInMilliseconds
))