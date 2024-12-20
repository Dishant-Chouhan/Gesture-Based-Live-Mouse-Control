from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pyautogui
import math
import time
import logging
from pynput.mouse import Button, Controller
import util

# Initialize Flask app
app = Flask(__name__)

# Initialize Logging
logging.basicConfig(level=logging.INFO)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize Mouse Controller
mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Global variables for zoom detection
prev_thumb_index_dist = None
ZOOM_IN_THRESHOLD = 30
ZOOM_OUT_THRESHOLD = -30

# Function to detect zoom gestures and simulate zoom in/out based on thumb and index finger distance
def detect_zoom(thumb_index_dist):
    global prev_thumb_index_dist
    if prev_thumb_index_dist is not None:
        distance_change = thumb_index_dist - prev_thumb_index_dist
        if distance_change > ZOOM_IN_THRESHOLD:
            logging.info("Zooming In")
            pyautogui.hotkey('ctrl', '+')  # Simulate zoom in
        elif distance_change < ZOOM_OUT_THRESHOLD:
            logging.info("Zooming Out")
            pyautogui.hotkey('ctrl', '-')  # Simulate zoom out
    prev_thumb_index_dist = thumb_index_dist

# Function to detect left-click gesture
def some_condition_for_left_click(landmarks):
    # Example condition: Check if the thumb and index fingers are close together (for left click)
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    # Calculate the Euclidean distance between the thumb and index tip
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    
    # If the distance is small enough, consider it a left-click gesture
    if distance < 0.05:  # Adjust threshold based on your needs
        return True
    return False

# Function to detect right-click gesture
def some_condition_for_right_click(landmarks):
    # Example condition: Check if the index finger is extended while others are folded (for right click)
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    
    # Check if index is extended and other fingers are folded (you can adjust the threshold values)
    if index_tip.y < middle_tip.y and index_tip.y < ring_tip.y:  # Adjust the threshold if needed
        return True
    return False

# Function to generate the video feed
def generate_camera_feed():
    """Generate webcam frames and perform hand gesture-based controls."""
    global prev_thumb_index_dist
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow for Windows to avoid conflicts
    try:
        while cap.isOpened():
            time.sleep(0.03)  # Limit FPS to reduce CPU load
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to capture frame from webcam")
                break

            # Flip the frame and convert it to RGB
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Process detected hands
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract thumb and index finger tip positions
                    landmarks = hand_landmarks.landmark
                    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Calculate distance between thumb and index finger
                    thumb_index_dist = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)

                    # Map index finger tip to screen coordinates
                    cursor_x = max(0, min(int(index_tip.x * screen_width), screen_width - 1))
                    cursor_y = max(0, min(int(index_tip.y * screen_height), screen_height - 1))
                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                    # Detect zoom gestures
                    detect_zoom(thumb_index_dist)

                    # Detect left and right-click gestures
                    if some_condition_for_left_click(landmarks):
                        mouse.press(Button.left)
                        mouse.release(Button.left)
                        logging.info("Left Click Detected")
                    elif some_condition_for_right_click(landmarks):
                        mouse.press(Button.right)
                        mouse.release(Button.right)
                        logging.info("Right Click Detected")

            # Encode frame for streaming
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    except Exception as e:
        logging.error(f"Error during video processing: {e}")
    finally:
        cap.release()
        logging.info("Webcam resources released.")

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/live-demo')
def live_demo():
    """Render the live demo page."""
    return render_template('live_demo.html')

@app.route('/video-feed')
def video_feed():
    """Stream webcam video feed to the browser."""
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    logging.info("Starting the Flask app...")
    app.run(debug=True, threaded=True)
