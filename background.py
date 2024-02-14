#https://ddorn.gitlab.io/post/2021-04-01-creating-a-retro-sunset-with-pygame/
import pygame
import pygame.gfxdraw

from math import *

from settings import Settings

pygame.init()
settings = Settings()
#SIZE = (640, 360)
W = settings.screen_width
H = settings.screen_height
SIZE = (W, H)

# colors for gradients
SUN_TOP = pygame.Color(255, 218, 69)
SUN_BOTTOM = pygame.Color(255, 79, 105)
SKY_TOP = pygame.Color(73, 231, 236)
SKY_BOTTOM = pygame.Color(171, 31, 101)
LINES = pygame.Color(255, 79, 105)
BG_COLOR = pygame.Color(43, 15, 84)

# band height for sun and sky
BAND_HEIGHT = 3
band_height_sky = W // 100
# sun center
INFINITY = pygame.Vector2(W / 2, H * 0.46 // BAND_HEIGHT * BAND_HEIGHT)


def chrange(x, input_range, output_range):
    """Map the interval input_range to output_range."""
    # Linarly map to [0, 1]
    normalised = (x - input_range[0]) / (input_range[1] - input_range[0])
    # And back to the output range.
    return normalised * (output_range[1] - output_range[0]) + output_range[0]


def from_polar(radius, angle):
    """Convert polar coordinate with the angle in degrees to a pygame vector."""
    v = pygame.Vector2()
    v.from_polar((radius, angle))
    return v


def draw(display, time):
    """Draw each part of the scene on the display."""
    draw_sky(display)
    #draw_sunrays(display, time)
    draw_sun(display)
    #draw_vertical_lines(display)
    #draw_horizontal_lines(display, time)


def draw_sky(display, top=SKY_TOP, bottom=SKY_BOTTOM):
    """Draw the sky gradient in band by band."""

    for band in range(0, H // 2, band_height_sky):
        #For each band, calculates an intermediate color by linearly interpolating (lerp) between the top and bottom colors 
        color = top.lerp(bottom, band / H * 2)
        print(band / H * 2)
        display.fill(color, (0, band, W, band_height_sky))


def draw_sun(display, radius=54, top=SUN_TOP, bottom=SUN_BOTTOM):
    """Draw a sun with a gradient and some stripes."""

    # We add one to make sure the borders of the sun are not cropped
    size = radius * 2 + 1, radius * 2 + 1
    # The gradient is an offscreen surface,
    # as we need to modify it before we blit it
    gradient = pygame.Surface(size)

    # Drawing the gradient
    for y in range(0, size[1], BAND_HEIGHT):
        color = top.lerp(bottom, y / size[1])
        gradient.fill(color, (0, y, size[1], BAND_HEIGHT))

    # Drawing the shape of the sun on an other surface.
    mask = pygame.Surface(size)
    # Defining the shape of the sun, a white circle
    pygame.draw.circle(mask, "white", (radius, radius), radius)

    # Removing bands = drawing in black
    for y in range(BAND_HEIGHT, size[1], BAND_HEIGHT):
        pygame.gfxdraw.hline(mask, 0, size[1], y, (0, 0, 0))

    gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_MULT)
    gradient.set_colorkey((0, 0, 0))

    display.blit(gradient, gradient.get_rect(center=INFINITY))


def draw_vertical_lines(display):
    """Draw vertical lines converging to the sun."""

    # Erase the lower part
    second_half = pygame.Rect(0, H / 2, W, H / 2)
    display.fill(BG_COLOR, second_half)

    # Vertical lines
    n_lines = 17
    for n in range(n_lines):
        n = chrange(n, (0, n_lines - 1), (-pi / 2, pi / 2))
        angle = chrange(sin(n), (-1, 1), (0, pi))

        x = INFINITY[0] + 1000 * cos(angle)
        y = INFINITY[1] + 1000 * sin(angle)

        segment = second_half.clipline(x, y, *INFINITY)
        if segment:
            pygame.draw.line(display, LINES, *segment)


def draw_horizontal_lines(display, time):
    """Draw moving horizontal lines for the ground."""

    anim_h = H - INFINITY[1]
    prop = 3 / 4
    dy = -time % (anim_h * (1 - prop))

    for n in range(100):
        y = INFINITY[1] + (anim_h - dy) * (prop ** n)
        if y < H / 2:
            break
        pygame.gfxdraw.hline(display, 0, W, round(y), LINES)
    pygame.gfxdraw.hline(display, 0, W, H // 2, LINES)


def draw_sunrays(display, time):
    """Draw rotating rays originating at the sun's center."""

    span = 5
    for angle in range(0, 360, span * 2):
        angle += time / 7

        p1 = INFINITY + from_polar(1000, angle)
        p2 = INFINITY + from_polar(1000, angle + span)
        points = [INFINITY, p1, p2]

        color = pygame.Color(SUN_BOTTOM)
        color.a = 50

        pygame.gfxdraw.filled_polygon(display, points, color)


def main():
    """The main loop."""

    display = pygame.display.set_mode(SIZE, pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return

        draw(display, frame)
        pygame.display.update()
        clock.tick(60)
        frame += 1
        print(frame)


if __name__ == "__main__":
    main()