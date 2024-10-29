# ThreeJS-Python-Flask

This project combines Three.js, Python, and Flask to create an interactive 3D web application with real-time object detection using YOLO (You Only Look Once).

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [InShort](#inshort)

## Project Overview

This repository showcases an innovative integration of Three.js for 3D visualization, Python for backend processing, and Flask for creating a web application. The project demonstrates how to combine these technologies to build an interactive environment with real-time object detection capabilities.

### Features

- Interactive 3D scene rendered using Three.js
- Real-time object detection using YOLO algorithm
- Web-based interface built with Flask
- Support for multiple .gltf models
- XR (Augmented Reality) support with hand tracking
- Responsive design for desktop and mobile devices

## Technologies Used

- Frontend: Three.js
- Backend: Python
- Web Framework: Flask
- Object Detection: YOLO (You Only Look Once)
- Additional Dependencies:
  - Ultralytics for YOLO integration
  - OpenCV for video processing
  - Tailwind CSS for styling

## Setup Instructions

To run this project locally, follow these steps:

1. Clone the repository:
git clone https://github.com/NafisRayan/ThreeJS-Python-Flask.git


2. Install dependencies:
pip install flask opencv-python ultralytics numpy

3. Ensure you have Node.js installed on your system.

4. Navigate to the project directory:
cd ThreeJS-Python-Flask

5. Run the Flask server:
python app.py

6. Access the application by opening a web browser and navigating to `http://localhost:5000`.

## Usage

Once the application is running, you'll see a live video feed with real-time object detection overlaid on a 3D scene. You can interact with the scene using keyboard controls or XR controllers if available.

- Use arrow keys or WASD to move the camera
- Press Space to jump
- Left-click and drag to rotate the camera
- Right-click and drag to pan the camera

For a more immersive experience, use a VR headset and controllers to explore the 3D environment.

## Inshort

This application is a comprehensive web-based 3D environment that integrates various features to create an interactive experience. Below is a detailed breakdown of its main components:

1. 3D Scene with THREE.js
- **3D Environment**: Built using THREE.js for rendering 3D graphics.
- **Model Loading**: Supports loading 3D models in GLTF format.
- **Camera Controls**: Includes controls for user navigation through the scene.
- **VR Support**: Offers Virtual Reality capabilities for immersive experiences.
- **Hand Tracking**: Implements hand tracking features for VR interactions.

2. Video Background
- **Video Feed**: Displays a live video feed (likely from a camera) behind the 3D scene.
- **Transparency**: The 3D scene is rendered with transparency to allow visibility of the video background.

3. UI Components
- **Map Interface**: 
  - Shows a map in the bottom-left corner using MapLibreGL.
- **Chat Interface**: 
  - Displays a chat system in the bottom-right corner.
- **Menu System**: 
  - Includes a dropdown menu with options to:
    - Toggle the video background.
    - Toggle the map.
    - Toggle the chat.

4. Visual Elements
- **Status Bar**: 
  - Displays date, time, and weather information.
- **Navigation Bar**: 
  - Features a semi-transparent styling for better aesthetics.
- **3D Models**: 
  - Includes models such as a "Squid Game" figure.

5. Responsive Design
- **Styling**: 
  - Utilizes Tailwind CSS for modern styling.
- **Adaptability**: 
  - Adapts to various screen sizes and devices.
- **Hover Effects**: 
  - Incorporates hover effects and transitions for enhanced interactivity.

## Conclusion
This application functions as an interactive dashboard or interface, merging real-world video feeds with 3D elements and practical widgets. It employs modern web technologies and supports both desktop and VR interactions, making it suitable for monitoring or interactive systems.
