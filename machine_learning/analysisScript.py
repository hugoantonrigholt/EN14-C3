from ultralytics import YOLO

model = YOLO('best.pt')


results = model.predict(source='input_folder', conf=0.2, iou=0.2, save=True, project='.', classes=[0], name='output_folder', exist_ok=True)