import pygame
import math

class Guns():
    """A class for weapons"""

    def __init__(self, settings, player) -> None:
        """Initialize weapon class"""

        #self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()  

        self.weapons = {2 : 'laser', 1 : 'ak47', 3 : 'knife'}

        self.current_weapon = self.weapons[2]

        # wepon unlock flags
        self.weapon_slot_1 = True
        self.weapon_slot_2 = True
        self.weapon_slot_3 = True
        
        # image names
        self.image_ak47 = 'images\\ak47.png'
        self.image_knife = 'images\\knife.png'
        
        # Charge
        self.overheat_event = False
        self.ammo_charge = 100
        self.discharge_speed = 1
        self.charge_speed = 2
        self.overheating = False
        self.recharge_delay = 0
        self.recharge_delay_max = 120 # def 120 - 2 sec
        
        #self.load_image(settings, player)

    def calculate_aim_angle(self, player):
        """Calculate the angele between player center and mouse pos to aim the gun"""
        mouse_pos = pygame.mouse.get_pos()
        self.angle = 360 - math.atan2(mouse_pos[1] - player.rect.centery, mouse_pos[0] - player.rect.centerx) * 180 / math.pi

    def choose_image(self, settings, player):
        """Pick the image according to current wepon"""
        if self.current_weapon == self.weapons[3]:
            self.image_name = self.image_knife
            self.gun(settings, player)
        elif self.current_weapon == self.weapons[2]:
            self.laser(player)
        elif self.current_weapon == self.weapons[1]:
            self.image_name = self.image_ak47
            self.gun(settings, player)
    
    def choose_scale(self, settings, player):
        """Pick the image scale according to the flag"""
        self.image_copy = pygame.transform.scale(self.image_copy,
                                             (settings.screen_rect.width // player.h_divider, settings.screen_rect.height // player.w_divider * 3))
        self.rect = self.image_copy.get_rect()

    def laser(self, player):
        """Make a surface of a laser gun and make a mask for it to rotate properly"""
        self.calculate_aim_angle(player)

        # Create a surface for the laser gun
        gun_length = player.height # 2 times shorter because of the mask
        gun_height = player.width // 4
        gun_surface = pygame.Surface((gun_length, gun_height), pygame.SRCALPHA)
        
        gun_surface.fill('Black')

        # Creating a mask for the left half of the gun
        self.half_gun_surface = pygame.Surface((gun_length / 2, gun_height), pygame.SRCALPHA)
        # Fill the left half with an opaque color
        #self.half_gun_surface.fill((0, 0, 0, 0))  
        # Apply the mask to the gun surface
        gun_surface.blit(self.half_gun_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Rotate the gun surface 
        self.image_copy = pygame.transform.rotate(gun_surface, self.angle)
        self.rect = self.image_copy.get_rect(center=player.rect.center) 
        """problem is that after rotating i getting a new rect and midright points chnages, it doesnt anchor to the surface"""

    def gun(self, settings, player):
        """Make a surface of a gun by loading image"""
        self.calculate_aim_angle(player)

        # Create a surface for the gun
        self.image = pygame.image.load(self.image_name)
        self.image_copy = self.image.copy()
        self.choose_scale(settings, player)

        # Rotate the gun surface 
        self.image_copy = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image_copy.get_rect(center=player.rect.center) 

    def draw(self, settings, player):
        """Draw the weapon to the screen"""
        self.choose_image(settings, player)
        self.screen.blit(self.image_copy, self.rect)




