from flask import Flask, render_template, Response, send_file
from ultralytics import YOLO
import cv2
import os
import math
import datetime
import numpy as np
import random

app = Flask(__name__, static_url_path='/static')

# Load the YOLO model (adjust the path as needed)
model = YOLO("yolov8n.pt")  # Replace with your model path

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
              "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
              "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
              "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
              "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
              "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]


randomColors = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Define the center, axes, and angle of the ellipse
center = (640, 0)  # Adjusted center coordinates
axes = (int(np.sqrt(1280**2 + 720**2) / 2), 50)
angle = 0

# Initialize status bar parameters
status_bar_height = 50
status_bar_color = (0, 0, 0)

# Set the curvature variable for the curved line
curvature = 30

# Initialize the video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
cap.set(4, 720)   # CV_CAP_PROP_FRAME_HEIGHT

def gen_frames():
    while True:
        success, frame = cap.read()  # Read the camera frame
        if not success:
            break
        
        # Draw status bar with curved underline
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        status_bar = f'Time: {time_str} | Date: {date_str} | Weather: Sunny, 29c'
        text_size = cv2.getTextSize(status_bar, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        image_height, image_width, _ = frame.shape
        
        # Draw the curved line
        cv2.ellipse(frame, (image_width // 2, status_bar_height - curvature), (image_width // 2, curvature), 0, 0, 180, (255, 255, 255), 1)
        
        # Draw the status bar text
        cv2.putText(frame, status_bar, ((image_width - text_size[0]) // 2, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # # Draw three horizontal lines in the center
        # line_y = frame.shape[0] // 2  # Y-coordinate for the center of the image
        # cv2.line(frame, (frame.shape[1]//4, line_y - 20), (frame.shape[1]*3//4, line_y - 20), (255, 255, 255), 1)
        # cv2.line(frame, (frame.shape[1]//3, line_y), (frame.shape[1]*2//3, line_y), (255, 255, 255), 1)
        # cv2.line(frame, (frame.shape[1]//4, line_y + 20), (frame.shape[1]*3//4, line_y + 20), (255, 255, 255), 1)
        
        # Process the frame with YOLO
        results = model(frame)
        
        # Draw results (adjust as needed)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1

                # Find the center of the object and the center of the text
                object_center = ((x1 + x2) // 2, (y1 + y2) // 2)
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                name = classNames[cls]

                # Generate colors based on confidence
                color_intensity = int(conf * 255)
                randomColors = (
                    random.randint(50, min(color_intensity, 255)),
                    random.randint(50, min(color_intensity, 255)),
                    random.randint(50, min(color_intensity, 255))
                )

                textPos = (max(0, x1), max(24, y1))
                x, y = textPos
                text = f"{name} {conf}"

                text_scale = 0.7  # to control all the sizes

                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, 1)[0]
                text_center = (max(0, x1) + text_size[0] // 2, max(24, y1) - text_size[1] // 2)

                fontScale = text_scale
                textThickness = 2 
                textColor = (0, 0, 0)
                bgColor = randomColors
                # (255, 255, 255)
                pad_x, pad_y = int(10 * text_scale), int(10 * text_scale)
                Opacity = 0.7
                (t_w, t_h) = text_size

                overlay = frame.copy()  # copying the image

                # Draw 
                cv2.circle(overlay, object_center, int(4 * text_scale), (0, 0, 0), -1)  
                cv2.line(overlay, object_center, text_center, (0, 0, 0), 1) 
                cv2.rectangle(overlay, (x - pad_x, y + pad_y), (x + t_w + pad_x, y - t_h - pad_y), bgColor, -1)  # draw rectangle
                cv2.putText(overlay, text, (max(0, x1), max(24, y1)), cv2.FONT_HERSHEY_SIMPLEX, fontScale, textColor, textThickness)  # draw text
                cv2.rectangle(overlay, (max(0, x1) - pad_x, max(24, y1) - t_h - pad_y), (max(0, x1) + t_w + pad_x, max(24, y1) + pad_y), (0, 25, 30), int(2 * text_scale), cv2.LINE_AA)

                frame = cv2.addWeighted(overlay, Opacity, frame, 1 - Opacity, 0)  # overlaying on the image.

                
                
        # # Encode the frame in JPEG format
        # _, buffer = cv2.imencode('.jpg', frame)
        # frame = buffer.tobytes()
        
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

@app.route('/assets/<path:path>')
def serve_assets(path):
    if path.endswith('.ttf') or path.endswith('.otf'):
        return send_file(os.path.join('fonts', path), mimetype='application/font-ttf')
    elif path.endswith('.gltf'):  
        return send_file(os.path.join('assets', path), mimetype='model/gltf')
    elif path.endswith('.html'):  # New condition for HTML files
        return send_file(os.path.join('assets', path), mimetype='text/html')
    else:
        return send_file(os.path.join('assets', path), mimetype='application/octet-stream')
if __name__ == '__main__':
    app.run(debug=True)