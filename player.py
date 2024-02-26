# find a good formula for calculating gravity (probably should be correlation with dick heigh)
#print(player.jump_height, player.rect.height, dick.rect.height)


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
        self.width = settings.screen_width // 20
        self.height = settings.screen_height // 5
        self.image = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA) #needs to make a proper rotation
        self.image.fill('Red')
        self.rect = self.image.get_rect()


        # Gravity and jumping
        self.ground_flag = False
        self.gravity = 0 
        self.jump_height = int(self.height * .11) #fckn hard to balance for different screen sizes

        # Weapon rotation
        self.rotation_angle = 0
        self.image_copy = self.image.copy()
        self.image_rotated = pygame.transform.rotate(self.image_copy,
                                                           -self.rotation_angle)
        self.rotated_rect = self.image_rotated.get_rect()
        self.rotated_rect.center = self.rect.center

        # Charge
        self.overheat_event = False
        self.ammo_charge = 100
        self.discharge_speed = 1
        self.charge_speed = 2
        self.overheating = False
        self.recharge_delay = 0
        self.recharge_delay_max = 120 # def 120 - 2 sec

        self.gun_laser()
        
    def place(self, background):
        """Position the dick on the screen"""
        self.rect.bottomleft = background.ground_rect.topleft
        self.rect.x += self.rect.width * 3 # need to adjust if using png       
            
    def draw(self, background):
        """Draw the player to the screen"""
        if self.rect.bottom == background.ground_rect.top:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image_rotated, self.rotated_rect)
        
        self.gun_laser()

    def calculate_aim_angle(self):
        """Calculate the angele between player center and mouse pos to aim the gun"""
        mouse_pos = pygame.mouse.get_pos()
        self.angle = 360 - math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx) * 180 / math.pi

    def gun_laser(self):
        """Make a surface of a laser gun and make a mask for it to rotate properly"""
        self.calculate_aim_angle()

        # Create a surface for the laser gun
        gun_length = self.height # 2 times shorter because of the mask
        gun_height = self.width // 4
        gun_surface = pygame.Surface((gun_length, gun_height), pygame.SRCALPHA)
        
        gun_surface.fill('Black')

        # Creating a mask for the left half of the gun
        self.half_gun_surface = pygame.Surface((gun_length / 2, gun_height), pygame.SRCALPHA)
        # Fill the left half with an opaque color
        #self.half_gun_surface.fill((0, 0, 0, 0))  
        # Apply the mask to the gun surface
        gun_surface.blit(self.half_gun_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Rotate the gun surface
        self.gun_rotated = pygame.transform.rotate(gun_surface, self.angle)
        self.gun_rect = self.gun_rotated.get_rect(center=self.rect.center) 
        """problem is that after rotating i getting a new rect and midright points chnages, it doesnt anchor to the surface"""

        self.screen.blit(self.gun_rotated, self.gun_rect)








        

#DO IT WITH MASK try to do it