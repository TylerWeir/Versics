# This program is an 2D interactive physics enviornment in which a user can
# define entities by joining points with sticks.
#
# By: Tyler Weir

import pygame
import pygame.mouse
from versics import Entity, Environment

# Set up the swing Entity
points = [(450, 50), (480, 50), (510, 50), (540, 50), (570, 50), (600, 50),
          (630, 50), (660, 50), (690, 50), (720, 50), (750, 30), (750, 70),
          (790, 30), (790, 70)]
sticks = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
          (8, 9), (9, 10), (10, 11), (11, 9), (11, 13), (10, 12), (12, 13),
          (10, 13)]
locked_points = [0]
swing = Entity(points, points, sticks, locked_points)


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
        self.background.fill((28, 28, 28))

        # Clock to limit the frame rate
        self.clock = pygame.time.Clock()

        # Set up the physics environment
        self.environment = Environment((800, 800))

        self.environment.add_entity(swing)
    
    def render_menu(self, surface):
        # Render the title
        title_font = pygame.font.Font('freesansbold.ttf', 32)
        title = title_font.render('Versics', True, (0,250,0))
        titleRect = title.get_rect()
        titleRect.center = (100, 20)
        surface.blit(title, titleRect)
        
        # Render the menu options
        menu_options = ['p = pause', 'c = create', 'd = delete', 's = save', 'q = quit']
        menu_font = pygame.font.Font('freesansbold.ttf', 20)
        
        for i, option in enumerate(menu_options):
            element = menu_font.render(f'{option}', True, (0,250,0))
            element_rect = element.get_rect()
            element_rect.center = (100, 60+40*i)
            surface.blit(element, element_rect)
        
        
        # Render the author's name
        author = menu_font.render('Tyler Weir', True, (0, 250, 0))
        author_rect = author.get_rect()
        author_rect.center = (100, 780)
        surface.blit(author, author_rect)
    
    def render_create_canvas(self, surface):
        canvas = pygame.Surface((800, 800))  
        canvas.fill((0,0,0))
        surface.blit(canvas, (200,0)) 
            
    
    def render_create_menu(self, surface):
         # Render the title
        title_font = pygame.font.Font('freesansbold.ttf', 32)
        title = title_font.render('Versics', True, (0,250,0))
        titleRect = title.get_rect()
        titleRect.center = (100, 20)
        surface.blit(title, titleRect)
        
        # Render the menu options
        menu_options = ['esc = normal mode', 'n = new entity', 'option 2', 'option 3', 'option 4']
        menu_font = pygame.font.Font('freesansbold.ttf', 20)
        
        for i, option in enumerate(menu_options):
            element = menu_font.render(f'{option}', True, (0,250,0))
            element_rect = element.get_rect()
            element_rect.center = (100, 60+40*i)
            surface.blit(element, element_rect)
        
        
        # Render the author's name
        author = menu_font.render('Tyler Weir', True, (0, 250, 0))
        author_rect = author.get_rect()
        author_rect.center = (100, 780)
        surface.blit(author, author_rect)

    def create_loop(self):
        creating = True
        
        points = []
        sticks = []
        locked_points = []
        newEntity = Entity(points, points, sticks, locked_points)
        self.environment.add_entity(newEntity)

        while creating:
            # Loops through the event queue.
            for event in pygame.event.get():
                # Quit if the user clicks exit
                if event.type == pygame.QUIT:
                    creating = False 
                # Looks for a key pressed event.
                elif event.type == pygame.KEYDOWN:
                    # Quit if the escape key is pressed.
                    if event.key == pygame.K_ESCAPE:
                        creating = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    # If the user presses the releases the left mouse button.
                    x, y = event.pos
                    x -= 200
                    print('adding point')
                    newEntity.add_point((x,y))

            # Paint the background
            self.screen.blit(self.background, (0,0))

            # Paint the menu
            self.render_create_menu(self.screen)
        
            # Paint the environment
            self.screen.blit(self.environment.render(), (200, 0))

            pygame.display.flip()
            self.clock.tick(60)

        
    def main_loop(self):
        running = True
        index = -1

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
                    if event.key == pygame.K_c:
                        self.create_loop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x -= 200
                    index = swing.find_closest_point_in_range((x,y), 20)
                    if index != -1:
                        swing.force_pos(index, (x,y))
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if index != -1:
                        swing.free_point(index)
                        index = -1

            if index != -1:
                x, y = pygame.mouse.get_pos()
                swing.force_pos(index, (x-200, y))

            # Paint the background
            self.screen.blit(self.background, (0,0))

            # Paint the menu
            self.render_menu(self.screen)
            
            # Update the environment
            self.environment.time_step()

            # draw the envEnvironment
            self.screen.blit(self.environment.render(), (200, 0))

            pygame.display.flip()
            self.clock.tick(60)


if (__name__ == '__main__'):
    program = Program()
    program.main_loop()
    pygame.quit
