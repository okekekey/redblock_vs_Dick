#https://ddorn.gitlab.io/post/2021-04-01-creating-a-retro-sunset-with-pygame/
#add mountains to the sides like hd pics maybe
#increase speed of background with lvl increase

import pygame
import pygame.gfxdraw
import random

from math import cos, sin, pi

from settings import Settings

class Background():
    """A class to draw background and UI elements"""
    
    def __init__(self, settings) -> None:
        """Initialize all elements of background"""
        
        self.screen = settings.screen 
        self.screen_rect = self.screen.get_rect() 

        # screen size
        self.screen_width = settings.screen_rect.width
        self.screen_height = settings.screen_rect.height

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
        self.indent()

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
        self.draw_ground()
        # Texts
        self.draw_game_name()
        self.draw_game_over(settings)
        self.draw_lives(settings)
        self.draw_score(settings)
        self.draw_high_score(settings, stats)
        self.draw_pause(settings)
          
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

    def resize(self, settings):
        """Resize background according to the screen size"""
        self.screen = settings.screen 
        self.screen_rect = self.screen.get_rect() 

        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

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
        
        self.indent()
                           
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
    
    def indent(self):
        """Creates screen indentation to attach UI to it"""
        self.left_indent = self.screen_rect.width // 100
        self.top_indent = self.screen_rect.height // 50
        self.width_indent = self.screen_rect.width - self.left_indent * 2
        self.length_indent = self.screen_rect.height - self.top_indent * 2
        self.screen_indent_rect = pygame.Rect(self.left_indent, self.top_indent, self.width_indent, self.length_indent)
        #self.surface_indent = pygame.Surface((self.width_indent, self.length_indent))  

    def draw_text(self, text, size, color):
        """function to help text creation quicker"""
        self.font = pygame.font.SysFont('Unispace', size)
        self.text = self.font.render(text, True, color)
        self.text_rect = self.text.get_rect()
    
    def draw_game_name(self):
        """Draw game name on the first screen"""
        self.draw_text('Red Block vs Richard!', self.screen_rect.width // 10, 'Pink')
        self.text_rect.center = (self.screen_rect.centerx, 
                                      self.screen_rect.centery)
        self.screen.blit(self.text, self.text_rect)

    def draw_lives(self, settings):
        """Displays lives left"""
        self.draw_text(f'Lives: {settings.current_lives}', self.screen_rect.width // 50, 'White')
        self.text_rect.topleft = (self.screen_indent_rect.x, self.screen_indent_rect.y)
        self.screen.blit(self.text, self.text_rect)
        
    def draw_score(self, settings):
        """Displays score"""
        self.draw_text(f'Score: {settings.current_score}', self.screen_rect.width // 50, 'White')
        self.text_rect.topright = (self.screen_indent_rect.right, self.screen_indent_rect.y)
        self.screen.blit(self.text, self.text_rect)   
        
    def draw_high_score(self, settings, stats):
        """Displays high score"""
        self.draw_text(f'High Score: {stats.high_score}', self.screen_rect.width // 70, 'DarkGrey')
        self.text_rect.topright = (self.screen_indent_rect.right, self.screen_indent_rect.y + self.text_rect.height * 2)
        self.screen.blit(self.text, self.text_rect)

    def draw_timer(self, settings):
        """Display play time"""
        self.draw_text(f':{int(settings.get_play_time()/1000)}', self.screen_rect.width // 40, 'White')
        self.text_rect.midtop = (self.screen_indent_rect.centerx, self.screen_indent_rect.y)
        self.screen.blit(self.text, self.text_rect)
# my dick sucks music
    def draw_game_over(self, settings):
        """Draw game over screen"""
        if settings.current_lives < 1:   
            self.draw_text(f'GAME OVER', self.screen_rect.width // 10, 'Red') 
            self.text_rect.center = (self.screen_rect.centerx, 
                                      self.screen_rect.centery)
            self.screen.fill('Pink')
            self.screen.blit(self.text, self.text_rect)
        
    def draw_pause(self, settings):
        """Draw pause text when paused and make it blink"""
        if self.show_text:
            self.draw_text('PAUSED', self.screen_rect.width // 50, 'White')
            self.text_rect.midtop = (self.screen_indent_rect.centerx, self.screen_indent_rect.y)
            self.screen.blit(self.text, self.text_rect)
        
    def draw_dick_hp(self, dick):
        """Draw dick hp"""
        self.draw_text(f'{dick.health}%', self.screen_rect.width // 50, 'White')
        self.text_rect.midbottom = dick.rect.midtop
        self.screen.blit(self.text, self.text_rect)

    def draw_ammo_charge(self, guns):
        """Draw % of charge ammo"""
        self.draw_text(f'{guns.ammo_charge}%', self.screen_rect.width // 50, 'White')
        self.text_rect.center = guns.rect.topright
        self.screen.blit(self.text, self.text_rect)
           


