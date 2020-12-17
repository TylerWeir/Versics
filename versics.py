# This class is a verlet integration based physics engine. Each instance of
# the engine takes in points, their old positions, the force they are subject
# to, the binds between points, and the indecies of any point positions to lock.
#
# Creator: Tyler Weir
# Date:
# Version: In developement

import pygame
from pygame.math import Vector2


class Versics(pygame.sprite.Sprite):
    """Class used to give physics to models with structure."""

    def __init__(self, points, old_points, forces, sticks, locked_points=[]):
        # Lists to contain all the points in the system.
        self.points = [Vector2(a, b) for (a, b) in points]
        self.old_points = [Vector2(a, b) for (a, b) in old_points]
        self.forces = [Vector2(a, b) for (a, b) in forces]
        self.sticks = [(a, b, self.points[a].distance_to(self.points[b]))
                       for (a, b) in sticks]
        self.locked_points=locked_points

        self.gravity = Vector2((0, 5.0))
        self.time_step = 1/60

    def timeStep(self):
        self.accumulate_forces()
        self.verlet()
        self.satisfy_contraints()

    def verlet(self):
        """Verlet integration step."""
        for i in range(len(self.points)):

            if i not in self.locked_points:
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

        # Number of iterations to satisfy contraints
        for j in range(1):
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

                # Stick contstraint
                for stick in self.sticks:
                    x1 = Vector2(self.points[stick[0]])
                    x2 = Vector2(self.points[stick[1]])
                    delta = x2-x1
                    delta_length = delta.length()
                    diff = (delta_length-stick[2])/delta_length

                    if stick[0] not in self.locked_points:
                        self.points[stick[0]] += delta*0.5*diff
                    if stick[1] not in self.locked_points:
                        self.points[stick[1]] -= delta*0.5*diff


# Test program ########################################################
pygame.init()

# Screen setup
pygame.display.set_caption("Verlet Physics Simulation")
screen = pygame.display.set_mode((1000, 1000))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Clock to limit frame rate
clock = pygame.time.Clock()

# Set up the physics objects
points = [(500, 50), (530, 50), (560, 50), (590, 50), (620, 50), (650, 50),
          (680, 50), (710, 50), (740, 50), (770, 50), (830, 20), (830, 70)]
old_points = [(500, 50), (530, 50), (560, 50), (590, 50), (620, 50), (650, 50),
              (680, 50), (710, 50), (740, 50), (770, 50), (830, 20), (830, 70)]
forces = [(0, 980), (0, 980), (0, 980), (0, 980), (0, 980), (0, 980), (0, 980),
          (0, 980), (0, 980), (0, 980), (0, 980), (0, 980)]
sticks = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
          (8, 9), (9, 10), (10, 11), (11, 9)]
locked_points = [0]
balls = Versics(points, old_points, forces, sticks, locked_points)


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

    # Make the surface and blit to screen
    stickSurf = pygame.Surface((1000, 1000))
    stickSurf.fill((255, 0, 255))
    stickSurf.set_colorkey((255, 0, 255))
    pygame.draw.line(stickSurf, (255, 255, 255), pt1, pt2)
    screen.blit(stickSurf, (0, 0))


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

    # update the balls
    balls.timeStep()

    # draw the balls
    for ball in balls.points:
        render_ball(ball)

    # draw the sticks
    for stick in balls.sticks:
        render_stick(stick)

    pygame.display.flip()
    clock.tick(60)

pygame.QUIT
