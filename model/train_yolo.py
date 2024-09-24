from ultralytics import YOLO

data_yaml = '/path_to../YOLODataset/dataset.yaml'
model_weights = 'yolov8s.pt' 
epochs = 30 
imgsz = 640  

model = YOLO(model_weights)

model.train(data=data_yaml, epochs=epochs, imgsz=imgsz,batch=10)

model.save('trained_model.pt')
