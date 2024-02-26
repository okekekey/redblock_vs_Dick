import pygame
import sys
import math
from pygame.locals import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 1200))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    # Create player and gun surfaces
    player = pygame.Surface((50, 100), pygame.SRCALPHA)
    player_rect = player.get_rect()
    player_rect.center = screen_rect.center
    player.fill('Red')
    gun = pygame.Surface((100, 10), pygame.SRCALPHA)
    gun_rect = gun.get_rect(center=player_rect.center)  # Corrected rotation center
    gun.fill('DarkGrey')  # Fill the gun surface with a color

    #mask
    half_gun = pygame.Surface((50, 10), pygame.SRCALPHA)
    half_gun_rect = half_gun.get_rect(midright=gun_rect.center)
    mask = pygame.mask.from_surface(half_gun)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Calculate angle between player center and mouse position
        angle = math.atan2(mouse_pos[1] - player_rect.centery, mouse_pos[0] - player_rect.centerx) * 180 / math.pi

        # Rotate the gun surface
        gun_rotated = pygame.transform.rotate(gun, angle)

        # Set the midleft point of the gun at the center of the player
        gun_rect = gun_rotated.get_rect(center=player_rect.center)

        # Draw everything
        screen.fill((255, 255, 255))
        screen.blit(player, player_rect)  # Draw player (you can replace this with your actual player image)
        screen.blit(gun_rotated, gun_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
