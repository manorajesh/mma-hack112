import cv2
import mediapipe as mp
import numpy as np
import threading
from cmu_graphics import *

s = '''PLEASE READ: note about our citation
(1) Utilized Google's Mediapipe Algorithm to track hand movement & inputs and copied their
   code to initialize it on python
(2) Referenced ChatGPT for cross-platforming between mediapipe and cmu_graphics, ex. 
    threading and global variables
'''

# Initialize MediaPipe Hands - (1)
mp_hands = mp.solutions.hands

# Global variables to share data between OpenCV and cmu_graphics (2)
avgX_norm = 0.5
avgY_norm = 0.5
state = None
lock = threading.Lock()  # Lock for thread-safe updates (2)

# Function to process the camera feed and update hand positions (1)
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

                # We came up with idea of taking the average of finger inputs to get singular point
                hand_landmarks = results.multi_hand_landmarks[0]
                xs = np.array([lm.x for lm in hand_landmarks.landmark])
                ys = np.array([lm.y for lm in hand_landmarks.landmark])

                thumbX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumbY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                pointerX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                pointerY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                def almost_equal(a, b, epsilon=0.04):
                    return abs(a - b) < epsilon 

                with lock:  # Thread-safe update (2)
                    avgX_norm = np.mean(xs)
                    avgY_norm = np.mean(ys)
                    state = 'write' if almost_equal(thumbX, pointerX) and almost_equal(thumbY, pointerY) else 'none'

    cap.release()

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

# CMU Graphics app functions
def onAppStart(app):
    # Draw parameters
    app.avgX = int(avgX_norm * app.width)
    app.avgY = int(avgY_norm * app.height)
    app.r = 10
    app.stepsPerSecond = 100
    app.circles = []
    app.state = state 
    app.cursorColor = 'black'

    # toolbar parameters
    app.toolX = 200
    app.toolY = 200
    app.toolW = 150
    app.toolH = 740
    app.toolCirs = []
    for i in range(8):
        app.toolCirs.append((295, 300 + 80*i))
    app.toolColors = (['crimson', 'darkOrange', 'gold', 'mediumSpringGreen',
                       'aqua', 'mediumOrchid', 'deepPink', 'black'])

def redrawAll(app):
    # Drawing whiteboard w/ toolbar to change color
    drawRect(0, 0, app.width, app.height, fill='ghostWhite')
    drawRect(app.toolX, app.toolY, app.toolW, app.toolH, fill='lightGray')
    
    for i in range(8):
        drawCircle(295, 300 + 80*i, 30, fill=app.toolColors[i])
    
    # Draw cursor and line logic 
    drawCircle(app.avgX, app.avgY, app.r, fill=app.cursorColor)
    for cx, cy in app.circles:
        drawCircle(cx, cy, app.r, fill=app.cursorColor)

def onStep(app):
    global state
    with lock:  # Thread-safe read (2)
        app.avgX = int(app.width - (avgX_norm * app.width))
        app.avgY = int(avgY_norm * app.height)
        app.state = state

    if ((app.avgX > app.toolX + app.toolW) and (app.state == 'write')):
        app.circles.append((int(app.avgX), int(app.avgY)))

    color = getCircle(app.avgX, app.avgY, app.toolCirs, app.toolColors)
    if (color != None) and (app.state == 'none'):
        app.cursorColor = color

def getCircle(mouseX, mouseY, cirs, colors):
    for i in range(len(cirs)):
        cx, cy = cirs[i]
        if distance(mouseX, mouseY, cx, cy) <= 30:
            return colors[i]
    return None

# Main function to run OpenCV in a separate thread
def main():
    # Start the OpenCV hand tracking in a separate thread (2)
    threading.Thread(target=update_hand_position, daemon=True).start()
    
    # Start the CMU Graphics app
    runApp(width=1920, height=1080)

main()





