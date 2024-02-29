import pygame

class Dick():
    """A class for Dick"""

    def __init__(self, settings, background) -> None:
        """Initialize Dick and set its starting position"""

        #self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()

        # creating Dick with an image
        self.small_dick_flag = False
        self.image_thanos = 'images\Richard.png'
        self.image_kirby = 'images\Small_Richard.png'
        
        self.load_image(settings)
        self.initial_postion(background)
   
        self.health = 100

        # #creating Dick with a surface
        # self.size = settings.screen_height // 20
        # self.image = pygame.Surface((self.size, self.size),
        #                               pygame.SRCALPHA) #needs to make a proper rotation
        # self.image.fill('Pink')
        # self.rect = self.image.get_rect()
        self.resize(settings, background)

    def choose_image(self):
        """Pick the image according to the flag"""
        if not self.small_dick_flag:
            self.image_name = self.image_thanos
        else:
            self.image_name = self.image_kirby
    
    def choose_scale(self, settings):
        """Pick the image scale according to the flag"""
        if not self.small_dick_flag:
            self.image_copy = pygame.transform.scale(self.image_copy,
                                             (settings.screen_rect.width // 20, settings.screen_rect.height // 10))
        else:    
            self.image_copy = pygame.transform.scale(self.image_copy,
                                             (settings.screen_rect.width // 25, settings.screen_rect.height // 15))
        self.rect = self.image_copy.get_rect()

    def load_image(self, settings):
        """Loade image"""
        self.choose_image()
        self.image = pygame.image.load(self.image_name)
        self.image_copy = self.image.copy()
        self.choose_scale(settings)
        #self.image_copy.convert_alpha()
        #self.image_copy.set_colorkey('White')
        
    def drop_flag(self):
        """Drop small_dick_flag back to False"""
        self.small_dick_flag = False
        
    def initial_postion(self, background):
        """1st position of the dick on the screen"""
        self.rect.midbottom = (background.ground_rect.right - self.rect.width * 4, background.ground_rect.top)

    def replace(self, settings, background):
        """Reposition dick to the right of the screen"""
        self.rect.left = settings.screen_rect.right
        self.rect.bottom = background.ground_rect.top

    def reset_hp(self):
        """Reset dick HP"""
        self.health = 100

    def resize(self, settings, background):
        """Reajust dick size based on the screen size"""
        # store postion
        if settings.game_active_flag:
            midbottom = self.rect.midbottom

        
        self.load_image(settings)
        self.initial_postion(background)

        # restore position
        if settings.game_active_flag:
            self.rect.midbottom = midbottom

    def reset(self, settings, background):
        """Reset flags and images for new run"""
        if settings.current_lives >= 0:
            settings.self_pass_flag = False
            settings.start_timer_flag = False
            self.drop_flag()
            self.reset_hp()
            self.choose_image()
            self.load_image(settings)
            self.replace(settings, background)
    
    def draw(self, settings):
        """Draw the Dick to the screen"""
        self.screen.blit(self.image_copy, self.rect)
        #pygame.draw.rect(self.screen, 'White', self.rect)




    
