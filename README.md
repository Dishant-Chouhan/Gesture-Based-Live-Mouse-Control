# Gesture-Based Mouse Control Project

An innovative way to control your mouse through simple hand gestures. This project uses computer vision and machine learning techniques to detect hand gestures and control mouse movements in real time.

## Features

### Key Functionalities:
- **Mouse Movement**: Control mouse cursor with smooth hand gestures.
- **Left Click**: Perform a left-click using thumb and index finger gestures.
- **Right Click**: Trigger right-click actions with specific hand movements.
- **Zoom In & Zoom Out**: Use hand gestures to zoom in and out of the screen.
- **Screenshot**: Capture the screen with a simple hand gesture.

## Demo

Experience a live demo of the project that showcases how hand gestures control the mouse in real time. The live feed displays gesture tracking and actions being performed.

## Applications

This project has the potential to be used in various domains:
- **Accessibility**: Provides a hands-free computing experience for people with disabilities or limited mobility.
- **Virtual Reality (VR) and Augmented Reality (AR)**: Enables more immersive and natural interaction experiences.
- **Gaming**: Maps hand gestures to specific in-game actions for interactive gameplay.
- **Presentation Control**: Allows presenters to control slides and navigate content without physical input devices.
- **Medical and Research**: Can be used in robotic surgery or other sterile environments where touch is not ideal.

## Installation

Follow these steps to set up and run the project locally:

### Prerequisites
1. Python 3.7 or higher installed on your system.
2. Install [Flask](https://flask.palletsprojects.com/), [SocketIO](https://python-socketio.readthedocs.io/), and OpenCV.
3. (Optional) Install Docker if you want to run this project in a containerized environment.

### Steps
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/gesture-mouse-control.git
    cd gesture-mouse-control
    ```
2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask server:
    ```bash
    python app.py
    ```
4. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. Start the Flask server to access the live demo.
2. Use hand gestures in front of your camera to perform the following actions:
   - Move your hand to control the mouse cursor.
   - Make specific gestures for left click, right click, zoom in/out, or take screenshots.
3. Use the buttons in the web interface for testing the actions.

## Project Structure

```plaintext
gesture-mouse-control/
│
├── static/
│   ├── images/                # Images used for features and visuals.
│   ├── styles.css             # Custom styles for the web interface.
│   ├── project-files.zip      # Downloadable project files.
│
├── templates/
│   ├── index.html             # Home page.
│   ├── demo.html              # Live demo page.
│
├── app.py                     # Main Flask application.
├── requirements.txt           # Required Python libraries.
└── README.md                  # Project documentation (this file).
