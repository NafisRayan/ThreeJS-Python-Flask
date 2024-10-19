from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("yolov8n.pt")

# Export the model to TF.js format
model.export(format="tfjs")  # creates '/yolo11n_web_model'

# Load the exported TF.js model
tfjs_model = YOLO("./yolo8n_web_model")
print(1)
# Run inference
results = tfjs_model("https://ultralytics.com/images/bus.jpg")
