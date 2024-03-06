import pygame
import math


class Bullets(pygame.sprite.Sprite):
    """A class to manage bullets fired from wepons"""
    
    def __init__(self, guns, player) -> None:
        """Create bullet object, should have image and rect here"""
        super().__init__()

        # Group should have image and rect 
        self.image = pygame.Surface((10, 3), pygame.SRCALPHA)
        self.image.fill('Black')

        guns.calculate_aim_angle(player)

        self.image = pygame.transform.rotate(self.image, guns.angle)
        self.rect = self.image.get_rect(center=player.rect.center) 

    def update(self):
        """Move the bullet toward mouse pointer"""

        self.rect.x += self.bullet_vel_x
        self.rect.y += self.bullet_vel_y
