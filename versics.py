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

    def __init__(self, bounds, points, old_points, sticks, locked_points=[]):
        self.bounds = Vector2(bounds)

        # Lists to contain all the points in the system.
        self.points = [Vector2(a, b) for (a, b) in points]
        self.old_points = [Vector2(a, b) for (a, b) in old_points]
        self.sticks = [(a, b, self.points[a].distance_to(self.points[b]))
                       for (a, b) in sticks]
        self.locked_points = locked_points

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
                a = Vector2(0, 980)

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
                if self.points[i].x >= self.bounds.x:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = self.bounds.x
                    self.old_points[i].x = self.points[i].x+diff*bounce
                if self.points[i].x <= 0:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = 0
                    self.old_points[i].x = self.points[i].x + diff*bounce

                # y bounces
                if self.points[i].y >= self.bounds.y:
                    diff = self.points[i].y - self.old_points[i].y
                    self.points[i].y = self.bounds.y
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

    def render(self):
        # Surface to do all the drawing to
        canvas = pygame.Surface(self.bounds)
        canvas.fill((255, 0, 255))
        canvas.set_colorkey((225, 0, 255))

        # Draw in the points
        for point in self.points:
            pygame.draw.circle(canvas, (255, 255, 255), point, 4)

        # draw in the sticks
        for stick in self.sticks:
            # End points of the stick
            pt1 = self.points[stick[0]]
            pt2 = self.points[stick[1]]

            pygame.draw.line(canvas, (255, 255, 255), pt1, pt2)

        return canvas


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
points = [(450, 50), (480, 50), (510, 50), (540, 50), (570, 50), (600, 50),
          (630, 50), (660, 50), (690, 50), (720, 50), (750, 30), (750, 70)]
sticks = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
          (8, 9), (9, 10), (10, 11), (11, 9)]
locked_points = [0]
swing = Versics((900, 900), points, points, sticks, locked_points)


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
    swing.timeStep()

    screen.blit(swing.render(), (50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.QUIT
