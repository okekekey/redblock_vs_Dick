import pygame.display

class Settings():
    """A class to store all setting to the red block vs dick game"""

    def __init__(self) -> None:
        """Initialize all settings for the game"""
        
        # Screen settings
        
        # getting user screen width and height
        self.desktop_size = pygame.display.get_desktop_sizes()
        for tuple in self.desktop_size:
               self.screen_width = tuple[0]
               self.screen_height = tuple[1]







        
        
