# These classes form a basic 2D physics engine to be used with pygame based
# programs.
import pygame
from pygame.math import Vector2


class Versics(pygame.sprite.Sprite):
    """Class used to give physics to models with structure."""

    def __init__(self, points, old_points, forces, sticks):
        # Lists to contain all the points in the system.
        self.points = []
        self.old_points = []
        self.forces = []
        self.sticks = sticks

        self.gravity = Vector2((0, 5.0))
        self.time_step = 1/60

        # Fill in the lists
        for i in range(len(points)):
            self.points.append(Vector2(points[i]))
            self.old_points.append(Vector2(old_points[i]))
            self.forces.append(Vector2(forces[i]))

    def timeStep(self):
        self.accumulate_forces()
        self.verlet()
        self.satisfy_contraints()

    def verlet(self):
        """Verlet integration step."""
        for i in range(len(self.points)):
            temp = Vector2(self.points[i])
            old_pos = Vector2(self.old_points[i])
            a = Vector2(self.forces[i])

            self.points[i] += temp - old_pos + a*(self.time_step**2)
            self.old_points[i].update(temp)

    def accumulate_forces(self):
        """Accumulates forces for each particle."""
    #    for force in self.forces:
    #        force = Vector2(self.gravity)

    def satisfy_contraints(self):
        # 1 = perfectly elastic collision
        # 0 = perfectly inelastic collision
        bounce = 0.9

        for j in range(1):
            # Keeps the points inside a box
            # for point in self.points:
            #    point.x = min(max(point.x, 0), 900)
            #    point.y = min(max(point.y, 0), 900)
            # Keeps the points a distance apart

            for i in range(len(self.points)):
                # Make bounces by reflecting the velocity at time of impact
                # accross the wall. velocity is current pos - old pos.
                # Velocity must be stored before the current point is adjusted
                # to the wall boundry or else there is unintentional damping.

                # x bounce
                if self.points[i].x >= 900:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = 900
                    self.old_points[i].x = self.points[i].x+diff*bounce
                if self.points[i].x <= 0:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = 0
                    self.old_points[i].x = self.points[i].x + diff*bounce

                # y bounces
                if self.points[i].y >= 900:
                    diff = self.points[i].y - self.old_points[i].y
                    self.points[i].y = 900
                    self.old_points[i].y = self.points[i].y+diff*bounce
                if self.points[i].y <= 0:
                    diff = self.points[i].y - self.old_points[i].y
                    self.points[i].y = 0
                    self.old_points[i].y = self.points[i].y+diff*bounce

                for stick in self.sticks:
                    x1 = Vector2(self.points[stick[0]])
                    x2 = Vector2(self.points[stick[1]])
                    delta = x2-x1
                    delta_length = delta.length()
                    diff = (delta_length-100)/delta_length
                    self.points[stick[0]] += delta*0.5*diff
                    self.points[stick[1]] -= delta*0.5*diff


# Test program
pygame.init()

# Screen setup
pygame.display.set_caption("Verlet Physics Simulation")
screen = pygame.display.set_mode((1000, 1000))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Clock to limit frame rate
clock = pygame.time.Clock()


# Set up the physics objects
points = [(30, 100), (30, 200), (30, 300)]
old_points = [(22, 110), (20,210), (20, 310)]
forces = (Vector2(0, 980), Vector2(0, 980), Vector2(0, 980))
sticks = [(0, 1), (1, 2)]

balls = Versics(points, old_points, forces, sticks)


def render_ball(ball):
    # Create a surface that will represent the ball
    ballSurf = pygame.Surface((8, 8))

    # blite the circle onto the Surface
    ballSurf.fill((255, 0, 255))
    ballSurf.set_colorkey((255, 0, 255))
    pygame.draw.circle(ballSurf, (255, 255, 255), (4, 4), 4)
    screen.blit(ballSurf, (ball.x-4, ball.y-4))

def render_stick(stick):
    pt1 = balls.points[stick[0]]
    pt2 = balls.points[stick[1]]

    # Find the dimensions of the Surface
    # dx = abs(pt1.x-pt2.x)
    # dy = abs(pt1.y-pt2.y)

    # Make the surface
    stickSurf = pygame.Surface((1000, 1000))
    stickSurf.fill((255, 0, 255))
    stickSurf.set_colorkey((255, 0, 255))
    pygame.draw.line(stickSurf, (255, 255, 255), pt1, pt2)
    screen.blit(stickSurf, (0, 0))

    # blite the line onto the Surface



running = True
while running:
    # Loops through the event queue.
    for event in pygame.event.get():
        # Quit if the user clicks the quit button.
        if event.type == pygame.QUIT:
            running = False
        # Looks for a key pressed event.
        elif event.type == pygame.KEYDOWN:
            # Quit if the escape key is pressed.
            if event.key == pygame.K_ESCAPE:
                running = False

    # Paint the background
    screen.blit(background, (0, 0))

    balls.timeStep()

    for ball in balls.points:
        render_ball(ball)

    for stick in balls.sticks:
        render_stick(stick)

    pygame.display.flip()
    clock.tick(60)
