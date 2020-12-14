# These classes form a basic 2D physics engine to be used with pygame based
# programs.
import pygame
from pygame.math import Vector2


class Versics(pygame.sprite.Sprite):
    """Class used to give physics to models with structure."""

    def __init__(self, points, old_points, forces):
        # Lists to contain all the points in the system.
        self.points = []
        self.old_points = []
        self.forces = []


        self.gravity = Vector2((0, -1.0))
        self.time_step = 0.0

        # Fill in the lists
        for i in range(len(points)):
            self.points.append(Vector2(points[i]))
            self.old_points.append(Vector2(old_points[i]))
            self.forces.append(Vector2(forces[i]))

    def timeStep(self):
        accumulate_forces()
        verlet()
        satisfy_contraints()

    def verlet(self):
        """Verlet integration step."""
        for i in range(len(points)):
            temp = Vector2(self.points[i])
            old_pos = Vector2(self.old_points[i])
            a = Vector2(self.forces[i])

            self.points[i] += temp - old_pos + a*(self.time_step**2)
            self.old_points[i].update(temp)

    def accumulate_forces(self):
        """Accumulates forces for each particle."""
        for force in self.forces:
            force = Vector2(self.gravity)

    def satisfy_contraints(self):
        # Kepps the points inside a box
        for point in self.points:
            point.x = min(max(point.x, 0), 1000)
            point.y = min(max(point.y, 0), 1000)

        # Keeps the points a distance apart



#Test program
pygame.init()

screen = pygame.display.set_mode((1000, 1000))

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
