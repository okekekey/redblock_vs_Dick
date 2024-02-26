#https://ddorn.gitlab.io/post/2021-04-01-creating-a-retro-sunset-with-pygame/
#add mountains to the sides like hd pics maybe

import pygame
import pygame.gfxdraw
import random

from math import cos, sin, pi

from settings import Settings

class Background():
    """A class to draw background and UI elements"""
    
    def __init__(self, settings) -> None:
        """Initialize all elements of background"""
        self.settings = settings
        self.screen = settings.screen 
        self.screen_rect = self.screen.get_rect() 

        # screen size
        self.screen_width = settings.screen_width
        self.screen_height = settings.screen_height

        # colors for gradient effects
        self.sun_top_color = pygame.Color(255, 218, 69)
        self.sun_bottom_color = pygame.Color(255, 79, 105)
        self.sky_top_color = pygame.Color(33, 81, 86)
        self.sky_bottom_color = pygame.Color(131, 31, 81)
        self.starry_sky_stars = pygame.Color(255, 255, 255)
        self.lines_color = pygame.Color(5, 5, 5) #try black
        self.bg_color = pygame.Color(43, 15, 84)

        # sun settings
        self.sun_band_height = 7
        self.sun_radius = self.screen_height // 25
        self.sun_center = pygame.Vector2(self.screen_width / 2, 
                                         self.screen_height * 0.46 // self.sun_band_height * self.sun_band_height) # idk why so complcted

        # sky settings
        self.sky_band_height = self.screen_height // 50
        self.stars_number = self.screen_height // 100

        # line settings 
        self.vertical_lines_center = self.sun_center.copy()
        self.vertical_lines_center[1] = self.sun_center[1] + self.sun_radius

        # pause blink
        self.blink_interval = 1000 # def 1000
        self.show_text = True
        self.blink_event = pygame.USEREVENT+11
        pygame.time.set_timer(self.blink_event, self.blink_interval)

        self.draw_ground()

    def draw_pause_screen(self, time, settings, stats):
        """Draw selekted parts to the display."""
        self.draw_ground()
        self.draw_sky()
        self.draw_starry_sky()
        self.draw_sunrays(time)
        self.draw_sun()
        self.draw_vertical_lines()
        #self.draw_horizontal_lines(time)
        self.draw_horizontal_lines_freezed()
        # Texts
        self.draw_game_name()
        self.draw_game_over(settings)
        self.draw_lives(settings)
        self.draw_score(settings)
        self.draw_high_score(settings, stats)
        self.draw_pause(settings)
        #self.draw_pause(settings)
          
    def draw_game_screen(self, time, settings, stats):
        """Draw selekted parts to the display."""
        self.draw_sky()
        self.draw_starry_sky()
        self.draw_sunrays(time)
        self.draw_sun()
        self.draw_vertical_lines()
        self.draw_horizontal_lines(time)     
        self.draw_ground()
        # Texts
        self.draw_lives(settings)
        self.draw_score(settings)
        self.draw_high_score(settings, stats)
        self.draw_timer(settings)
        self.draw_game_over(settings)
        
        
               
    def draw_sky(self):
        """Draw the sky gradient band by band."""
        top = self.sky_top_color
        bottom = self.sky_bottom_color
        
        for band in range(0, self.screen_height // 2,
                           self.sky_band_height):
            #For each band, calculates an intermediate color by linearly interpolating (lerp) between the top and bottom colors 
            color = top.lerp(bottom, band / self.screen_height * 2)
            self.screen.fill(color, 
                        (0, band, self.screen_width, self.sky_band_height))

    def draw_starry_sky(self):
        """Draw the starry sky """

        # Generate random stars
        stars = [(random.randint(0, self.screen_width), random.randint(0, self.screen_height//2)) for star in range(self.stars_number)]
        # stars = []
        # for star in range(self.stars_number):
        #     star = (random.randint(0, self.screen_width), random.randint(0, self.screen_height//2))
        #     stars.append(star)

        for star in stars:
            pygame.draw.circle(self.screen, self.starry_sky_stars, star, random.randint(1,3))  # Small white dots for stars

    def draw_sun(self):
        """Draw a sun with a gradient and some stripes."""
        top = self.sun_top_color
        bottom = self.sun_bottom_color
        # We add one to make sure the borders of the sun are not cropped
        size = self.sun_radius * 2 + 1, self.sun_radius * 2 + 1
        # The gradient is an offscreen surface,
        # as we need to modify it before we blit it
        gradient = pygame.Surface(size)

        # Drawing the gradient
        for band in range(0, size[1], self.sun_band_height):
            color = top.lerp(bottom, band / size[1])
            gradient.fill(color, (0, band, size[1], self.sun_band_height))

        # Drawing the shape of the sun on an other surface.
        mask = pygame.Surface(size)
        # Defining the shape of the sun, a white circle
        pygame.draw.circle(mask, "white", (self.sun_radius, self.sun_radius), self.sun_radius)

        # Removing bands = drawing in black
        for band in range(self.sun_band_height, size[1], self.sun_band_height):
            pygame.gfxdraw.hline(mask, 0, size[1], band, (0, 0, 0))

        gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_MULT)
        gradient.set_colorkey((0, 0, 0))

        self.screen.blit(gradient, gradient.get_rect(center=self.sun_center))
    
    def chrange(self, x, input_range, output_range):
        """Map the interval input_range to output_range."""
        # Linarly map to [0, 1]
        normalised = (x - input_range[0]) / (input_range[1] - input_range[0])
        # And back to the output range.
        return normalised * (output_range[1] - output_range[0]) + output_range[0]

    def draw_vertical_lines(self):
        """Draw vertical lines converging to the sun."""

        # Erase the lower part
        second_half = pygame.Rect(0, self.screen_height / 2, self.screen_width, self.screen_height / 2)
        self.screen.fill(self.bg_color, second_half)

        # Vertical lines
        lines_number = 18
        for line in range(lines_number):
            line = self.chrange(line, (0, lines_number - 1), (-pi / 2, pi / 2))
            angle = self.chrange(sin(line), (-1, 1), (0, pi))

            #line length and center
            x_length = self.vertical_lines_center[0] + (self.screen_width / 2) * cos(angle)
            y_length = self.vertical_lines_center[1] + (self.screen_height / 2) * sin(angle)

            segment = second_half.clipline(x_length, y_length, *self.vertical_lines_center)
            if segment:
                pygame.draw.line(self.screen, self.lines_color, *segment)

    def draw_horizontal_lines(self, time):
        """Draw moving horizontal lines for the ground."""

        travel_distance = self.screen_height / 2.6
        frequency = 0.7 # [0 - 0.99]
        speed = 0.01 # [0.01-1000] fast - static
        dy = -time / speed % (travel_distance * (1 - frequency)) 
        
        for n in range(50):
            y = self.sun_center[1] + (travel_distance - dy) * (frequency ** n)
            if y < self.screen_height / 2:
                break
            pygame.gfxdraw.hline(self.screen, 0, self.screen_width, round(y),
                                  self.lines_color)
        pygame.gfxdraw.hline(self.screen, 0, self.screen_width, 
                             self.screen_height // 2, self.lines_color)

    def draw_horizontal_lines_freezed(self):
            """Draw moving horizontal lines for the ground."""

            travel_distance = self.screen_height / 2.6
            frequency = 0.7 # [0 - 0.99]
            speed = 0.01 # [0.01-1000] fast - static
            dy = - 10 / speed % (travel_distance * (1 - frequency)) 
            
            for n in range(50):
                y = self.sun_center[1] + (travel_distance - dy) * (frequency ** n)
                if y < self.screen_height / 2:
                    break
                pygame.gfxdraw.hline(self.screen, 0, self.screen_width, round(y),
                                    self.lines_color)
            pygame.gfxdraw.hline(self.screen, 0, self.screen_width, 
                                self.screen_height // 2, self.lines_color)
        
    def from_polar(self, radius, angle):
        """Convert polar coordinate with the angle in degrees to a pygame vector."""
        vector = pygame.Vector2()
        vector.from_polar((radius, angle))
        return vector

    def draw_sunrays(self, time):
        """Draw rotating rays originating at the sun's center."""

        ray_width = 4
        for angle in range(0, 360, ray_width * 2):
            angle += time / 10

            p1 = self.sun_center + self.from_polar(self.screen_width/1.5, angle)
            p2 = self.sun_center + self.from_polar(self.screen_width/1.5, angle + ray_width)
            points = [self.sun_center, p1, p2]
            
            color = pygame.Color(self.sun_bottom_color)
            #transparency
            color.a = 50

            pygame.gfxdraw.filled_polygon(self.screen, points, color)

    def draw_ground(self):
        """Draw ground for dick and player"""
        self.ground = pygame.Surface((self.screen_width, self.screen_height // 7))
        self.ground.fill('Green')
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.bottom = self.screen_rect.bottom
        self.screen.blit(self.ground, self.ground_rect)              

        self.ground2 = pygame.Surface((self.screen_width, self.ground_rect.height // 7 * 6))
        self.ground2.fill((150, 75, 50))
        self.ground2_rect = self.ground2.get_rect()
        self.ground2_rect.bottom = self.screen_rect.bottom
        self.screen.blit(self.ground2, self.ground2_rect)

## TEXTS
# try to make class Texts
        
    def draw_game_name(self):
        """Draw game name on the first screen"""
        game_name_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 10)
        text_game_name = game_name_font.render('Red Block vs Richard!', True, 'Pink')
        text_game_name_rect = text_game_name.get_rect()
        text_game_name_rect.center = (self.screen_rect.centerx, 
                                      self.screen_rect.centery)
        self.screen.blit(text_game_name, text_game_name_rect)

    def draw_lives(self, settings):
        """Displays lives left"""
        lives_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 50)
        text_lives = lives_font.render(f'Lives: {settings.current_lives}', True, 'White')
        text_lives_rect = text_lives.get_rect()
        text_lives_rect.topleft = (settings.screen_indent_rect.x, settings.screen_indent_rect.y)
        self.screen.blit(text_lives, text_lives_rect)
        
    def draw_score(self, settings):
        """Displays score"""
        # increase_score(player, dick, settings)
        score_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 50)
        text_score = score_font.render(f'Score: {settings.current_score}', True, 'White')
        text_score_rect = text_score.get_rect()
        text_score_rect.topright = (settings.screen_indent_rect.right, settings.screen_indent_rect.y)
        self.screen.blit(text_score, text_score_rect)     
        
    def draw_high_score(self, settings, stats):
        """Displays high score"""
        high_score_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 70)
        text_high_score = high_score_font.render(f'High Score: {stats.high_score}', True, 'DarkGrey')
        text_high_score_rect = text_high_score.get_rect()
        text_high_score_rect.topright = (settings.screen_indent_rect.right, settings.screen_indent_rect.y + text_high_score_rect.height * 2)
        self.screen.blit(text_high_score, text_high_score_rect)

    def draw_timer(self, settings):
        """Display play time"""
        
        timer_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 40)
        text_timer = timer_font.render(f':{int(settings.get_play_time()/1000)}', True, 'White')
        text_timer_rect = text_timer.get_rect()
        text_timer_rect.midtop = (settings.screen_indent_rect.centerx, settings.screen_indent_rect.y)
        self.screen.blit(text_timer, text_timer_rect)
    # maybe after g.o. make dick run with super speed and or smth like siple animation    
    def draw_game_over(self, settings):
        """Draw game over screen"""
        # increase_score(player, dick, settings)
        if settings.current_lives < 0:    
            game_over_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 10)
            text_game_over = game_over_font.render(f'Game over', True, 'Red')
            text_game_over_rect = text_game_over.get_rect()
            text_game_over_rect.center = (self.screen_rect.centerx, 
                                      self.screen_rect.centery)
            self.screen.fill('Pink')
            self.screen.blit(text_game_over, text_game_over_rect)
        
    def draw_pause(self, settings):
        """Draw pause text when paused and make it blink"""
        if self.show_text:
            pause_font = pygame.font.SysFont('Unispace', 
                                                self.screen_rect.width // 50)
            text_pause = pause_font.render('PAUSED', True, 'White')
            text_pause_rect = text_pause.get_rect()
            text_pause_rect.midtop = (settings.screen_indent_rect.centerx, settings.screen_indent_rect.y)
            self.screen.blit(text_pause, text_pause_rect)
        
    def draw_dick_hp(self, dick):
        """Draw dick hp"""
        dick_hp_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 50)
        text_dick_hp = dick_hp_font.render(f'{dick.health}%', True, 'White')
        text_dick_hp_rect = text_dick_hp.get_rect()
        text_dick_hp_rect.midbottom = dick.rect.midtop
        self.screen.blit(text_dick_hp, text_dick_hp_rect)

    def draw_ammo_charge(self, player):
        """Draw % of charge ammo"""
        ammo_font = pygame.font.SysFont('Unispace', 
                                             self.screen_rect.width // 50)
        text_ammo = ammo_font.render(f'{player.ammo_charge}%', True, 'White')
        text_ammo_rect = text_ammo.get_rect()
        text_ammo_rect.center = player.gun_rect.topright
        self.screen.blit(text_ammo, text_ammo_rect)
           


