import cv2
import mediapipe as mp
import numpy as np
import math


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and detect hands.
        results = hands.process(image)

        # Draw hand landmarks on the image.
        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Averages all points in hand to coordinate movement
                xs = np.array([lm.x for lm in hand_landmarks.landmark])
                ys = np.array([lm.y for lm in hand_landmarks.landmark])

                avgX_norm = np.mean(xs)
                avgY_norm = np.mean(ys)

                # print(avgX_norm, avgY_norm)

            
                # Gets thumb/index finger indices to see if making 'ok' sign
                thumbX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumbY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                pointerX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                pointerY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                def almost_equal(a, b, epsilon=0.05):
                    return abs(a-b) < epsilon 

                if almost_equal(thumbX, pointerX) and almost_equal(thumbY, pointerY):
                    state = 'write'
                else:
                    state = 'none'

                print(state)
              
                # index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x

                # # Get normalized coordinates
                # x = index_finger_tip.x
                # y = index_finger_tip.y
                # z = index_finger_tip.z

                # print(f"Index Finger Tip - x: {x}, y: {y}, z: {z}")

        # Display the resulting frame
        cv2.imshow('Hand Tracker', frame)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
