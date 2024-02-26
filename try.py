import pygame
import sys
from pygame.locals import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Create the first surface
    surface1 = pygame.Surface((100, 50), pygame.SRCALPHA)
    surface1.fill('Red')
    surface1_rect = surface1.get_rect(center=(400, 300))

    # Rotate the first surface
    angle = 125  # Example rotation angle
    rotated_surface1 = pygame.transform.rotate(surface1, angle)

    # Calculate the midright point of the rotated surface
    midright_point = rotated_surface1.get_rect().midright

    # Create the second surface
    surface2 = pygame.Surface((50, 20), pygame.SRCALPHA)
    surface2.fill('Blue')

    # Set the position of surface2 to the midright point of the rotated surface
    surface2_rect = surface2.get_rect(midright=midright_point)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        screen.blit(rotated_surface1, surface1_rect)
        screen.blit(surface2, surface2_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
