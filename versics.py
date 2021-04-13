# This class is a verlet integration based physics engine. Each instance of
# the engine takes in points, their old positions, the force they are subject
# to, the binds between points, and the indecies of any point positions to lock.
#
# Creator: Tyler Weir
# Began: December 2020
# Version: In developement


import pygame
from pygame.math import Vector2


class Environment():
    """Represents the environment in which rigid body physics is simulated."""

    def __init__(self, size, entities=[]):
        self.size = Vector2(size)
        self.entities = entities
        self.dt = 1/60

    def add_entity(self, entity):
        """Adds a body to the simulation."""
        self.entities.append(entity)

    def time_step(self):
        for entity in self.entities:
            entity.verlet(self.dt)
            entity.satisfy_contraints(self.size)

    def render(self):
        """Renders the environment and it's entities to the screen."""
        #Surface to do all the drawing to
        canvas = pygame.Surface(self.size)
        canvas.fill((0, 0, 0))

        # Draw in the entities
        for entity in self.entities:
            # Draw the entity onto the environment's surface
            canvas.blit(entity.render(), (0,0))

        return canvas


class Entity():
    """Represents a rigid body structure and it's constraints"""

    def __init__(self, points, old_points, sticks, locked_points=[]):

        # Lists to contain all the points in the system.
        self.points = [Vector2(a, b) for (a, b) in points]
        self.old_points = [Vector2(a, b) for (a, b) in old_points]
        self.sticks = [(a, b, self.points[a].distance_to(self.points[b]))
                       for (a, b) in sticks]
        self.locked_points = locked_points

        self.gravity = Vector2((0, 5.0))  # Should be an environmental force


    def verlet(self, time_step):
        """Verlet integration step."""
        for i in range(len(self.points)):

            if i not in self.locked_points:
                temp = Vector2(self.points[i])
                old_pos = Vector2(self.old_points[i])
                a = Vector2(0, 980)

                self.points[i] += temp - old_pos + a*(time_step**2)
                self.old_points[i].update(temp)

    def find_closest_point_in_range(self, position, r):
        """Find the index of the point closest to a given position."""
        pos = Vector2(position) 
        dist = r
        index = -1 

        for i in range(len(self.points)):
            distance = self.points[i].distance_to(pos)
            if distance < dist:
                dist = distance 
                index = i
             
        return index

    def accumulate_forces(self):
        """Accumulates forces for each particle."""
    #    for force in self.forces:
    #        force = Vector2(self.gravity)

    def satisfy_contraints(self, bounds):
        # 1 = perfectly elastic collision
        # 0 = perfectly inelastic collision
        bounce = 0.25

        # Number of iterations to satisfy contraints
        for j in range(6):
            for i in range(len(self.points)):
                # Make bounces by reflecting the velocity at time of impact
                # accross the wall. velocity is current pos - old pos.
                # Velocity must be stored before the current point is adjusted
                # to the wall boundry or else there is unintentional damping.

                # x bounce
                if self.points[i].x >= bounds.x:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = bounds.x
                    self.old_points[i].x = self.points[i].x+diff*bounce
                if self.points[i].x <= 0:
                    diff = self.points[i].x - self.old_points[i].x
                    self.points[i].x = 0
                    self.old_points[i].x = self.points[i].x + diff*bounce

                # y bounces
                if self.points[i].y >= bounds.y:
                    diff = self.points[i].y - self.old_points[i].y
                    self.points[i].y = bounds.y
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
        # TODO: Figure out way to more efficiently render the entity
        # onto the environment's canvas. Currently makes a giant transparent
        # surface that is blited onto the environment surface at (0, 0).
        canvas = pygame.Surface((900, 900)) # Makes giant surface
        canvas.fill((255, 0, 255))
        canvas.set_colorkey((255, 0, 255))

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

    def make_square(self, pos, size):
        """Returns a rigid square entity."""
        pass

    def make_rope(self, pos, size):
        """Returns a rope-like entity."""
        pass

    def make_cloth(self, pos, size):
        """Returns a cloth like entity."""
        pass

    def force_pos(self, pointIndex, position):
        """Forces a point to a given position."""
        if self.locked_points.count(pointIndex) == 0:
            self.locked_points.append(pointIndex)

        self.points[pointIndex].x = position[0]
        self.points[pointIndex].y = position[1]

    def free_point(self, pointIndex):
       """Unlocks a point for free movement."""
       self.locked_points.remove(pointIndex)
