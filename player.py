import pygame

class Player():
    """A class for the red block aka player"""

    def __init__(self, settings, screen) -> None:
        """Initialize the player and set its starting position"""

        self.settings = settings
        self.screen = screen

        #creating a player with an image
        self.image = pygame.image.load('images\lego_block.png')
        self.image = pygame.transform.scale(self.image,
                                             (settings.screen_width // 20, settings.screen_height // 10))
        self.rect = self.image.get_rect()
        

        #creating a player with a surface
        # self.width = settings.screen_width // 40
        # self.height = settings.screen_height // 10
        # self.surface = pygame.Surface((self.width, self.height),
        #                               pygame.SRCALPHA) #needs to make a proper rotation
        # self.surface.fill('Red')
        # self.rect = self.surface.get_rect()

        #position player
        self.rect.bottom = 1000
        self.rect.centerx = 1000


        self.gravity = 0 
        self.rotation_angle = 0


    def update(self):
        """Update the player postionion"""
        pass

    def blitme(self):
        """Draw the player to the screen"""
        self.screen.blit(self.image, self.rect) 

