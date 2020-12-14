# These classes form a basic 2D physics engine to be used with pygame based
# programs.
import pygame
from pygame.math import Vector2


class Versics(pygame.sprite.Sprite):
    """Class used to give physics to models with structure."""
    pass


class Node():
    """Class used to represent points in the structure of a physics model."""

    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]

    def setX(self, x):
        """Sets the x coorinate of the Node."""
        self.x = x

    def setY(self, y):
        """Sets the y coorindate of the Node."""
        self.y = y

    def setPos(self, position):
        """Sets the position of the Node."""
        self.x = position[0]
        self.y = position[1]

    def getX(self):
        """Returns the x coordinate of the Node."""
        return self.x

    def getY(self):
        """Returns the y coorinate of the Node."""
        return self.y

    def getPos(self):
        """Returns the position of the Node as a tuple (x, y)."""
        return (self.x, self.y)


class Stick():
    """Class used to connect Nodes in the structure of a physics model."""

    def __init__(self, breakpoint=1, node1, node2):
        self.node1 = node1
        self.node2 = node2
