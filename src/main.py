from cmu_graphics import *
from tracker import HandTracker


def onAppStart(app):
    app.background = "black"
    app.tracker = HandTracker()


def onStep(app):
    pass


def redrawAll(app):
    hands = app.tracker.getHands()

    for hand in hands:
        if hand and hand.smoothedX and hand.smoothedY:
            if hand.detected:
                fill = "green" if hand.label == "Left" else "blue"
            else:
                fill = "red"
            drawCircle(hand.smoothedX, hand.smoothedY, 10, fill=fill)


def onAppStop(app):
    app.tracker.close()


def main():
    runApp(width=1920, height=1080)


main()