import pygame
from random import randint


class BonusLive():
    """A class for bonus live"""

    def __init__(self, settings) -> None:
        """Initialize bonus and set its random position"""

        #self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()

        self.spawn_rate = self.screen_rect.width * 10 #default 10

        # creating bonus live with an image
        self.image_name = 'images\heart.png'
        self.load_image(settings)
        
        self.place_postion()

    
    def choose_scale(self, settings):
        """Pick the image scale according to the flag"""
        self.image_copy = pygame.transform.scale(self.image_copy,
                                             (settings.screen_width // 25, settings.screen_height // 15))

    def load_image(self, settings):
        """Loade image"""
        self.image = pygame.image.load(self.image_name)
        self.image_copy = self.image.copy()
        self.choose_scale(settings)
        self.image_copy.convert_alpha()
        self.rect = self.image_copy.get_rect()

    # def drop_flag(self):
    #     """Drop small_dick_flag back to False"""
    #     self.small_dick_flag = False
        
    def place_postion(self):
        """Position BL on the screen"""
        self.rect.left = randint(self.spawn_rate, int(self.spawn_rate * 2)) # 2
        self.rect.bottom = randint(self.rect.height, self.screen_rect.centery)
    
    def reset(self):
        """Reset flags and images for new run"""
        self.place_postion()
    
    def draw(self):
        """Draw the Dick to the screen"""
        self.screen.blit(self.image_copy, self.rect)
        #pygame.draw.rect(self.screen, 'White', self.rect)




    
