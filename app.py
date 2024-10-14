from flask import Flask, render_template, Response, send_file
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__, static_url_path='/static')

# Load the YOLO model (adjust the path as needed)
model = YOLO("yolov8n.pt")  # Replace with your model path

# Initialize the video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

def gen_frames():
    while True:
        success, frame = cap.read()  # Read the camera frame
        if not success:
            break
        
        # Process the frame with YOLO
        results = model(frame)
        
        # Draw results (adjust as needed)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/models/<path:path>')
def serve_gltf(path):
    return send_file(os.path.join('models', path), mimetype='model/gltf')

if __name__ == '__main__':
    app.run(debug=True)