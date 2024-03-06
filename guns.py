import pygame
import math

class Guns():
    """A class for weapons"""

    def __init__(self, settings, player) -> None:
        """Initialize weapon class"""

        #self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()  

        self.weapons = {1 : 'ak47', 2 : 'laser', 3 : 'knife', 0 : 'none'}

        self.none_stats = {'index' : 0, 'name' : 'none', 'ammo_capacity' : 0, 'dmg': 0, 'discharge_speed' : 0, 'charge_speed' : 0, 'recharge_delay': 0}
        self.ak47_stats = {'index' : 1, 'name' : 'ak47', 'ammo_capacity' : 30, 'dmg': 20, 'discharge_speed' : 1, 'charge_speed' : 30, 'recharge_delay': 120}
        self.laser_stats = {'index' : 2, 'name' : 'laser', 'ammo_capacity' : 100, 'dmg': 5, 'discharge_speed' : 1, 'charge_speed' : 1, 'recharge_delay': 220}
        self.knife_stats = {'index' : 3, 'name' : 'knife', 'ammo_capacity' : 100, 'dmg': 100, 'discharge_speed' : 0, 'charge_speed' : 0, 'recharge_delay': 0}


        self.current_weapon = self.weapons[0]
        self.current_weapon_stats = self.none_stats

        # wepon unlock flags
        self.weapon_slot_1 = True
        self.weapon_slot_2 = True
        self.weapon_slot_3 = True
        
        # image names
        self.image_ak47 = 'images\\ak47.png'
        self.image_knife = 'images\\knife.png'
        
        # Charge
        self.overheat_event = False
        self.ammo_capacity = 100
        self.discharge_speed = 1
        self.charge_speed = 2
        self.overheating_flag = False
        self.recharge_delay = 0



        self.image = pygame.image.load(self.image_knife)
        self.rect = self.image.get_rect()


    def calculate_aim_angle(self, player):
        """Calculate the angele between player center and mouse pos to aim the gun"""
        mouse_pos = pygame.mouse.get_pos()
        self.angle = 360 - math.atan2(mouse_pos[1] - player.rect.centery, mouse_pos[0] - player.rect.centerx) * 180 / math.pi

    def choose_image(self, settings, player):
        """Pick the image according to current wepon"""
        if self.current_weapon == self.weapons[3]:
            self.image_name = self.image_knife
            self.gun_load(settings, player)
        elif self.current_weapon == self.weapons[2]:
            self.laser_load(player)
        elif self.current_weapon == self.weapons[1]:
            self.image_name = self.image_ak47
            self.gun_load(settings, player)

    def laod_weapon_stats(self):
        """loads weapon stats for current weapon"""
        if self.current_weapon == self.weapons[3]:
            self.current_weapon_stats = self.knife_stats
        elif self.current_weapon == self.weapons[2]:
            self.current_weapon_stats = self.laser_stats
        elif self.current_weapon == self.weapons[1]:
            self.current_weapon_stats = self.ak47_stats
   
    def choose_scale(self, settings, player):
        """Pick the image scale according to the flag"""
        self.image_copy = pygame.transform.scale(self.image_copy,
                                             (settings.screen_rect.width // player.h_divider, settings.screen_rect.height // player.w_divider * 3))
        self.rect = self.image_copy.get_rect()

    def laser_load(self, player):
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
        
    def shoot_laser(self, settings):
        """Draw laser beam """
        if self.current_weapon == self.weapons[2]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button_pressed = pygame.mouse.get_pressed()
            if mouse_button_pressed[0] and not self.overheating_flag:
                pygame.draw.line(settings.screen, 'Red', self.rect.center,
                                mouse_pos, 3)

    def gun_load(self, settings, player):
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
        if not self.current_weapon == self.weapons[0]:
            self.choose_image(settings, player)
            self.screen.blit(self.image_copy, self.rect)

    def discharge_charge_weapon(self):
        """Unload and reload weapon"""
        self.overheating()
        self.overheat_cooldown()
        mouse_button_pressed = pygame.mouse.get_pressed()
        # discharge/ unload
        if mouse_button_pressed[0] and self.ammo_capacity >= 0 and not self.overheating_flag:
            self.ammo_capacity -= self.current_weapon_stats['discharge_speed']
        # laser recharge
        elif self.ammo_capacity < self.current_weapon_stats['ammo_capacity'] and self.recharge_delay == 0 and self.current_weapon == self.weapons[2]:
            self.ammo_capacity += self.current_weapon_stats['charge_speed']
        # ak47 reload //charge_speed = ammo_capacity wont work in other way
        elif self.ammo_capacity == 0 and self.recharge_delay == 0 and self.current_weapon == self.weapons[1]:
            self.ammo_capacity += self.current_weapon_stats['charge_speed']
        # max ammo    
        elif self.ammo_capacity > self.current_weapon_stats['ammo_capacity']:
            self.ammo_capacity = self.current_weapon_stats['ammo_capacity']
        
    def overheating(self):
        """Checks if a weapon is overheated"""
        if self.ammo_capacity < 0:
            self.overheating_flag = True
            self.recharge_delay = self.current_weapon_stats['recharge_delay']
            self.ammo_capacity = 0 # need to assigne to stop dead loop

    def overheat_cooldown(self):
        """Delays reloading weapon when overheated"""
        if self.recharge_delay > 0:
            self.recharge_delay -= 1 ######### add to weapon stats?
        elif self.recharge_delay == 0:
            self.overheating_flag = False 
        