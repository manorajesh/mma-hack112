from cmu_graphics import *
import pymunk
import random
import time
from src.circle import *


def onAppStart(app):
    app.time = time.time()
    app.space = pymunk.Space()

    app.space.gravity = (0, 500)  # Gravity in the y-direction

    # Create static walls
    app.walls = WallBoundaries(app.space, app.width, app.height)

    # Create multiple balls
    app.balls = []
    for i in range(6):
        circle = CircleBody(
            100 + i * 20, 100 + random(), 20, app.space, fill='blue')
        app.balls.append(circle)


def onStep(app):
    now = time.time()
    dt = now - app.time
    app.time = now
    app.space.step(dt)


def redrawAll(app):
    app.walls.draw()
    for ball in app.balls:
        ball.draw()


def main():
    runApp(width=800, height=600)


main()
