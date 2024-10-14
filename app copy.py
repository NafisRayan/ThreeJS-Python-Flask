from flask import Flask, render_template
from flask_socketio import SocketIO
from ultralytics import YOLO
import cv2
import base64
import numpy as np

app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO(app)

model = YOLO('yolov8n.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
              "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
              "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
              "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
              "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
              "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model(frame, stream=True)
            detected_objects = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    w, h = x2 - x1, y2 - y1
                    conf = float(box.conf[0].item())  # Convert to Python float
                    cls = int(box.cls[0].item())  # Convert to Python int
                    name = classNames[cls]
                    detected_objects.append({
                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                        'name': name, 'confidence': conf
                    })
            
            if detected_objects:
                socketio.emit('object_detected', {'objects': detected_objects})
            
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('video_frame', {'frame': frame_bytes})

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(generate_frames)

if __name__ == '__main__':
    socketio.run(app)