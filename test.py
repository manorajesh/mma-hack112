from cmu_graphics import *
import pymunk

# Initialize Pymunk space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity in the y-direction

# Create static walls
walls = [
    pymunk.Segment(space.static_body, (0, 0), (400, 0), 5),  # Bottom wall
    pymunk.Segment(space.static_body, (0, 0), (0, 400), 5),  # Left wall
    pymunk.Segment(space.static_body, (400, 0), (400, 400), 5),  # Right wall
    pymunk.Segment(space.static_body, (0, 400), (400, 400), 5)  # Top wall
]
for wall in walls:
    wall.elasticity = 0.8  # Make walls bouncy
    wall.filter = pymunk.ShapeFilter(categories=1, mask=1)
    space.add(wall)

# Create multiple balls
balls = []
for i in range(5):
    # Create a dynamic ball
    ball_body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, 20))
    ball_body.position = (100 + i * 20, 100)  # Staggered positions
    ball_shape = pymunk.Circle(ball_body, radius=20)
    ball_shape.elasticity = 0.9  # Make balls bouncy
    ball_shape.friction = 0.5
    space.add(ball_body, ball_shape)
    balls.append(ball_body)

# Create box
box_body = pymunk.Body(mass=5, moment=pymunk.moment_for_box(1, (2.0, 3.0)))
box_body.position = (200, 200)
box_shape = pymunk.Poly.create_box(box_body, (20, 30))
box_shape.elasticity = 0.6
box_shape.filter = pymunk.ShapeFilter(categories=1, mask=1)
space.add(box_body, box_shape)

# Draw function
def draw():
    app.group.clear()
    # Draw the walls
    for wall in walls:
        Line(wall.a.x, wall.a.y, wall.b.x, wall.b.y, fill='black', lineWidth=5)
    # Draw the balls
    for ball in balls:
        Circle(ball.position.x, ball.position.y, 20, fill='blue')
    # Draw box
    Rect(box_body.position.x, box_body.position.y, 20, 30, fill='red')


# Update the simulation
def onStep():
    space.step(1 / 60)  # Advance the simulation
    draw()

# Set app properties
app.stepsPerSecond = 60
cmu_graphics.run()

