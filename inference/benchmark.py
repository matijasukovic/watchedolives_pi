from ultralytics import YOLO

model_path = r"/home/matijasukovic_pi5/projects/watchedolives_pi/models/v45_p2s_bs40_264epoch_params/weights/best.pt"
dataset_path=r"/home/matijasukovic_pi5/projects/watchedolives_pi/datasets/rock_detection_v4.5/config.yaml"

model = YOLO(model_path)

results = model.benchmark(data=dataset_path, imgsz=640, device="cpu")