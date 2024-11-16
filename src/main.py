import cv2
import mediapipe as mp
from cmu_graphics import *

INDEX_FINGER_IDX = 8
THUMB_IDX = 4


def onAppStart(app):
    app.background = "black"
    app.stepsPerSecond = 1000

    app.videoCap = cv2.VideoCapture(0)
    app.lastFrameTime = 0

    handSolution = mp.solutions.hands
    app.hands = handSolution.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    app.smoothedX = None
    app.smoothedY = None
    app.alpha = 0.5

    app.handsDetected = False


def onStep(app):
    success, img = app.videoCap.read()
    if not success:
        return

    imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    recHands = app.hands.process(imgRgb)

    totalX = 0
    totalY = 0
    num_hands = 0

    if recHands.multi_hand_landmarks:
        for hand in recHands.multi_hand_landmarks:
            avgY = 0
            avgX = 0
            num_landmarks = len(hand.landmark)
            for point in hand.landmark:
                avgY += point.y
                avgX += point.x
            avgY /= num_landmarks
            avgX /= num_landmarks

            h, w, _ = img.shape
            currentX = int(w - (avgX * w))
            currentY = int(avgY * h)

            totalX += currentX
            totalY += currentY
            num_hands += 1

    if num_hands > 0:
        currentX = totalX // num_hands
        currentY = totalY // num_hands

        if app.smoothedX is None:
            app.smoothedX = currentX
        if app.smoothedY is None:
            app.smoothedY = currentY

        dx = currentX - app.smoothedX
        dy = currentY - app.smoothedY
        app.smoothedX += int(dx * app.alpha)
        app.smoothedY += int(dy * app.alpha)

        app.handsDetected = True
    else:
        app.handsDetected = False


def redrawAll(app):
    if app.smoothedX is not None and app.smoothedY is not None:
        drawCircle(
            app.smoothedX,
            app.smoothedY,
            20,
            fill="white" if app.handsDetected else "red",
        )


def onAppStop(app):
    app.videoCap.release()


def main():
    runApp(width=1920, height=1080)


main()
