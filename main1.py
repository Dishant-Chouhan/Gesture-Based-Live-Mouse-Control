import cv2
import mediapipe as mp
import pyautogui
import random
import util
from pynput.mouse import Button, Controller

# Initialize mouse controller
mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# Constants for zoom detection
ZOOM_IN_THRESHOLD = 30
ZOOM_OUT_THRESHOLD = -30

prev_thumb_index_dist = None

def find_finger_tip(processed): 
    """Find the index finger tip position."""
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None

def move_mouse(index_finger_tip):
    """Move the mouse cursor based on the position of the index finger tip."""
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmark_list, thumb_index_dist):
    """Detect if left click gesture is performed."""
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    """Detect if right click gesture is performed."""
    return (
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        thumb_index_dist > 50
    )

def is_double_click(landmark_list, thumb_index_dist):
    """Detect if double click gesture is performed."""
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmark_list, thumb_index_dist):
    """Detect if screenshot gesture is performed."""
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist < 50
    )

def detect_zoom(thumb_index_dist):
    """Detect zoom in and out based on thumb and index finger distance."""
    global prev_thumb_index_dist

    if prev_thumb_index_dist is not None:
        distance_change = thumb_index_dist - prev_thumb_index_dist
        print(f"Previous Distance: {prev_thumb_index_dist}, Current Distance: {thumb_index_dist}")

        if distance_change > ZOOM_IN_THRESHOLD:
            pyautogui.hotkey('ctrl', '+')  # Zoom in
            print("Zoom In Detected")
        elif distance_change < ZOOM_OUT_THRESHOLD:
            pyautogui.hotkey('ctrl', '-')  # Zoom out
            print("Zoom Out Detected")

    prev_thumb_index_dist = thumb_index_dist

def detect_gesture(frame, landmark_list, processed):
    """Detect hand gestures for mouse control and other actions."""
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[8]])

        # Move the mouse cursor
        move_mouse(index_finger_tip)

        # Detect various gestures
        if thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            cv2.putText(frame, "Moving Mouse", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        else:
            detect_zoom(thumb_index_dist)

def main():
    """Main function to run the gesture detection and mouse control."""
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
