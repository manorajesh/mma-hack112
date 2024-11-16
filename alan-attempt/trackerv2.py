import cv2
import mediapipe as mp
import numpy as np
import threading
from cmu_graphics import *

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands

# Global variables to share data between OpenCV and cmu_graphics
avgX_norm = 0.5
avgY_norm = 0.5
state = None
lock = threading.Lock()  # Lock for thread-safe updates

# Function to process the camera feed and update hand positions
def update_hand_position():
    global avgX_norm, avgY_norm, state
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image and detect hands
            results = hands.process(image)

            # Update hand position if a hand is detected
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                xs = np.array([lm.x for lm in hand_landmarks.landmark])
                ys = np.array([lm.y for lm in hand_landmarks.landmark])

                thumbX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumbY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                pointerX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                pointerY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                def almost_equal(a, b, epsilon=0.04):
                    return abs(a - b) < epsilon 

                with lock:  # Thread-safe update
                    avgX_norm = np.mean(xs)
                    avgY_norm = np.mean(ys)
                    state = 'write' if almost_equal(thumbX, pointerX) and almost_equal(thumbY, pointerY) else 'none'

    cap.release()

# CMU Graphics app functions
def onAppStart(app):
    app.avgX = avgX_norm * app.width
    app.avgY = avgY_norm * app.height
    app.r = 10
    app.stepsPerSecond = 100
    app.circles = []
    app.state = state 

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    drawCircle(int(app.avgX), int(app.avgY), app.r, fill='purple')
    for cx, cy in app.circles:
        drawCircle(cx, cy, app.r, fill='purple')

def onStep(app):
    global state
    with lock:  # Thread-safe read
        app.avgX = app.width - (avgX_norm * app.width)
        app.avgY = avgY_norm * app.height
        app.state = state

    if app.state == 'write':
        app.circles.append((int(app.avgX), int(app.avgY)))

# Main function to run OpenCV in a separate thread
def main():
    # Start the OpenCV hand tracking in a separate thread
    threading.Thread(target=update_hand_position, daemon=True).start()
    
    # Start the CMU Graphics app
    runApp(width=1920, height=1080)

main()





