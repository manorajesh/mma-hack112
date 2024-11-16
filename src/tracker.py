import cv2
import mediapipe as mp
import numpy as np


class Hand:
    def __init__(self, label):
        self.label = label
        self.smoothedX = None
        self.smoothedY = None
        self.detected = False


class HandTracker:
    def __init__(self, smoothing=0.5, frame_width=640, frame_height=480):
        self.videoCap = cv2.VideoCapture(0)

        handSolution = mp.solutions.hands
        self.hands = handSolution.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.leftHand = Hand('Left')
        self.rightHand = Hand('Right')
        self.smoothing = smoothing

    def getHands(self):
        success, img = self.videoCap.read()
        if not success:
            return None

        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        recHands = self.hands.process(imgRgb)

        h, w, _ = img.shape

        # Reset detection status
        self.leftHand.detected = False
        self.rightHand.detected = False

        if recHands.multi_hand_landmarks and recHands.multi_handedness:
            for hand_landmarks, handedness in zip(recHands.multi_hand_landmarks, recHands.multi_handedness):
                label = handedness.classification[0].label  # 'Left' or 'Right'

                xs = np.array([lm.x for lm in hand_landmarks.landmark])
                ys = np.array([lm.y for lm in hand_landmarks.landmark])

                avgX_norm = np.mean(xs)
                avgY_norm = np.mean(ys)

                # Convert normalized to pixel coordinates
                currentX = int(w - (avgX_norm * w))
                currentY = int(avgY_norm * h)

                # Get the Hand instance corresponding to the label
                if label == 'Left':
                    hand = self.leftHand
                else:
                    hand = self.rightHand

                # Initialize smoothed positions if None
                if hand.smoothedX is None:
                    hand.smoothedX = currentX
                    hand.smoothedY = currentY
                else:
                    # Apply smoothing
                    hand.smoothedX += (currentX -
                                       hand.smoothedX) * self.smoothing
                    hand.smoothedY += (currentY -
                                       hand.smoothedY) * self.smoothing

                hand.detected = True

        return (self.leftHand, self.rightHand)

    def close(self):
        self.videoCap.release()

    def __del__(self):
        self.close()