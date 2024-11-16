from cmu_graphics import *
from trackerv2 import XYAvg

def onAppStart(app):
    x, y = XYAvg.getCenter()
    app.avgX = x
    app.avgY = y

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    drawCircle(app.avgX, app.avgY, 20, fill='purple')

def main():
    runApp()

main()