# This program is an 2D interactive physics enviornment in which a user can
# define entities by joining points with sticks.
#
# By: Tyler Weir

import pygame
from versics import Entity, Environment

class Program():
    """An interactive physics progam."""

    def __init__(self):
        pygame.init()

        # Set up the progam Window
        self.width = 1000
        self.height = 800

        pygame.display.set_caption("Interactive Physics")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 100, 0))

        # Clock to limit the frame rate
        self.clock = pygame.time.Clock()

        # Set up the physics environment
        self.environment = Environment((800, 800))

        # Set up the swing Entity
        points = [(450, 50), (480, 50), (510, 50), (540, 50), (570, 50), (600, 50),
                  (630, 50), (660, 50), (690, 50), (720, 50), (750, 30), (750, 70),
                  (790, 30), (790, 70)]
        sticks = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
                  (8, 9), (9, 10), (10, 11), (11, 9), (11, 13), (10, 12), (12, 13),
                  (10, 13)]
        locked_points = [0]
        swing = Entity(points, points, sticks, locked_points)
        self.environment.add_entity(swing)


    def main_loop(self):
        running = True

        while running:
            # Loops through the event queue.
            for event in pygame.event.get():
                # Quit if the user clicks exit
                if event.type == pygame.QUIT:
                    running = False
                # Looks for a key pressed event.
                elif event.type == pygame.KEYDOWN:
                    # Quit if the escape key is pressed.
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Paint the background
            self.screen.blit(self.background, (0,0))

            # Update the environment
            self.environment.time_step()

            # draw the envEnvironment
            self.screen.blit(self.environment.render(), (200, 0))

            pygame.display.flip()
            self.clock.tick(60)

program = Program()
program.main_loop()
pygame.quit
