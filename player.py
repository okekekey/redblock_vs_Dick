import pygame
import math

class Player():
    """A class for the red block aka player"""

    def __init__(self, settings) -> None:
        """Initialize the player and set its starting position"""

        #self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()   

        # #creating a player with an image
        # self.image = pygame.image.load('images\lego_block.png')
        # self.image.convert_alpha()
        # self.image.set_colorkey('White')
        # self.image = pygame.transform.scale(self.image,
        #                                      (settings.screen_width // 8, settings.screen_height // 4))
        # self.rect = self.image.get_rect()
        

        #creating a player with a surface
        self.w_divider = 40
        self.h_divider = 10
        settings.calculate_ss_variables(self)
        
        self.width = settings.screen_rect.width // self.w_divider # 20
        self.height = settings.screen_rect.height // self.h_divider # 5
        self.image = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA) #needs to make a proper rotation
        self.image.fill('Red')
        self.rect = self.image.get_rect()

        # rotation
        self.rotation_angle = 0
        self.image_copy = self.image.copy()
        self.image_rotated = pygame.transform.rotate(self.image_copy,
                                                           -self.rotation_angle)
        self.rotated_rect = self.image_rotated.get_rect()
        self.rotated_rect.center = self.rect.center

        # Gravity and jumping
        self.ground_flag = False
        self.gravity = 0 




        #self.gun_laser()

    # def calculate_size(self, settings):
    #     """Calculate player sizes, jump heigh and speed of the dick based on the screen size"""
    #     # player width
    #     if settings.screen_rect.width > settings.screen_sizes[1][0]: #1920
    #         self.w_divider = 40
    #     elif settings.screen_rect.width > settings.screen_sizes[2][0]: #1600
    #         self.w_divider = 35
    #     elif settings.screen_rect.width > settings.screen_sizes[3][0]: #1366
    #         self.w_divider = 30
    #     elif settings.screen_rect.width > settings.screen_sizes[4][0]: #1366
    #         self.w_divider = 25
    #     elif settings.screen_rect.width > settings.screen_sizes[5][0]: #1024
    #         self.w_divider = 22
    #     elif settings.screen_rect.width < settings.screen_sizes[5][0]: #1024
    #         self.w_divider = 20
    #     # player height
    #     if settings.screen_rect.height > settings.screen_sizes[1][1]: #1080
    #         self.h_divider = 10
    #     elif settings.screen_rect.height > settings.screen_sizes[2][1]: #900
    #         self.h_divider = 9
    #     elif settings.screen_rect.height > settings.screen_sizes[3][1]: #768
    #         self.h_divider = 8
    #     elif settings.screen_rect.height > settings.screen_sizes[4][1]: #720
    #         self.h_divider = 8
    #     elif settings.screen_rect.height > settings.screen_sizes[5][1]: #576
    #         self.h_divider = 7
    #     elif settings.screen_rect.height < settings.screen_sizes[5][1]: #576
    #         self.h_divider = 6
    #     # jump height
    #     if settings.screen_rect.height > settings.screen_sizes[1][1]: #1080
    #         self.jump_height = 26
    #     elif settings.screen_rect.height > settings.screen_sizes[2][1]: #900
    #         self.jump_height = 23
    #     elif settings.screen_rect.height > settings.screen_sizes[3][1]: #768
    #         self.jump_height = 21
    #     elif settings.screen_rect.height > settings.screen_sizes[4][1]: #720
    #         self.jump_height = 21
    #     elif settings.screen_rect.height > settings.screen_sizes[5][1]: #576
    #         self.jump_height = 19
    #     elif settings.screen_rect.height > 450: #450
    #         self.jump_height = 18
    #     elif settings.screen_rect.height > 350: #350
    #         self.jump_height = 17
    #     elif settings.screen_rect.height < 350: #350
    #         self.jump_height = 16
    #     # game speed

    def resize(self, settings, background):
        """Reajust player size based on the screen size"""
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()   

        settings.calculate_ss_variables(self)
        self.width = settings.screen_rect.width // self.w_divider # 20
        self.height = settings.screen_rect.height // self.h_divider # 5
        self.image = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA) 
        self.image.fill('Red')
        self.rect = self.image.get_rect()
        self.place(background)

    
    def rotated_resize(self, settings, background):
        """Reajust player size based on the screen size"""
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()   

        self.rotation_angle = 0
        self.image_copy = self.image.copy()
        self.image_rotated = pygame.transform.rotate(self.image_copy,
                                                           -self.rotation_angle)
        self.rotated_rect = self.image_rotated.get_rect()
        self.rotated_rect.center = self.rect.center
        self.place(background)

    def place(self, background):
        """Position the dick on the screen"""
        self.rect.midbottom = (self.rect.width * 5, background.ground_rect.top)       
            
    def draw(self, background, guns):
        """Draw the player to the screen"""
        if self.rect.bottom == background.ground_rect.top:
            self.screen.blit(self.image, self.rect)
            self.rotated_rect = self.rect # to avoid wrong collision detection with the dick
        else:
            self.screen.blit(self.image_rotated, self.rotated_rect)
        
        #guns.laser(self)

    








        

#DO IT WITH MASK try to do it