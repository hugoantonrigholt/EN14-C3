import os
import yaml
from ultralytics import YOLO

yaml_path = 'data.yaml'
model = YOLO('')

model.train(
    data=yaml_path,
    epochs=50,
    imgsz=800,
    batch=4,
    device=0,
)