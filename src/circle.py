import pymunk
from cmu_graphics import *


class CircleBody:
    def __init__(self, x, y, radius, space, fill='black'):
        self.radius = radius
        self.fill = fill

        self.body = pymunk.Body(
            mass=1, moment=pymunk.moment_for_circle(1, 0, radius))
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, radius=radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def draw(self):
        drawCircle(self.body.position.x, self.body.position.y,
                   self.radius, fill=self.fill)


class WallBoundaries:
    def __init__(self, space, width, height):
        self.space = space
        self.width = width
        self.height = height

        self.walls = [
            pymunk.Segment(space.static_body, (0, 0),
                           (width, 0), 5),  # Bottom wall
            pymunk.Segment(space.static_body, (0, 0),
                           (0, height), 5),  # Left wall
            pymunk.Segment(space.static_body, (width, 0),
                           (width, height), 5),  # Right wall
            pymunk.Segment(space.static_body, (0, height),
                           (width, height), 5)  # Top wall
        ]

        for wall in self.walls:
            wall.elasticity = 0.8
            space.add(wall)

    def draw(self):
        for wall in self.walls:
            drawLine(wall.a.x, wall.a.y, wall.b.x,
                     wall.b.y, fill='black', lineWidth=5)
