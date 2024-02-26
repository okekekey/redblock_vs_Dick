#add scalable screen size

import pygame.display

class Settings():
    """A class to store all setting to the red block vs dick game"""

    def __init__(self) -> None:
        """Initialize the game's static settings"""
                
        # getting user screen width and height
        self.desktop_size = pygame.display.get_desktop_sizes()
        for tuple in self.desktop_size:
               self.screen_width = tuple[0]
               self.screen_height = tuple[1]

        # Creating screen surface
        self.screen = pygame.display.set_mode((2400, 1200)) 
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('red block vs Dick.exe')

        # Screen indentaion for interface
        self.left_indent = self.screen_rect.width // 100
        self.top_indent = self.screen_rect.height // 50
        self.width_indent = self.screen_rect.width - self.left_indent * 2
        self.length_indent = self.screen_rect.height - self.top_indent * 2
        self.screen_indent_rect = pygame.Rect(self.left_indent, self.top_indent, self.width_indent, self.length_indent)

        #self.surface_indent = pygame.Surface((self.width_indent, self.length_indent))
    
        
        # game start flags
        self.game_started_flag = False
        self.game_active_flag = False

        # speed
        self.start_speed = self.screen_width // 256 #10 default
        self.lvl_speed = self.start_speed
        self.lvl_speed_step = 1 #10 default

        # Lives
        self.lives = 1 # default 3
        self.current_lives = self.lives
        self.live_font = pygame.font.SysFont('Unispace', 30)

        # Timer
        self.start_time = 0
        self.pause_start = 0
        self.pause_end = 0
        self.pause_time = 0
        self.timer_flag = False
        self.start_timer_flag = False
        self.timer_font = pygame.font.SysFont('Unispace', 40)
        self.play_time = 0

        # Score
        self.current_score = 0
        self.prev_score = self.current_score - 1
        self.high_score = 0
        self.dick_pass_flag = False # for jumping over
        self.dick_kill_flag = False # for killing dick

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        pass


    def increase_speed(self):
        """Increase speed settings"""
        pass


    def get_pause_start(self):
        """Get ticks when game paused"""
        if self.game_started_flag:
            self.pause_start = pygame.time.get_ticks()
            self.timer_flag = True

    def get_pause_end(self):
        """Get ticks when game started and calculate paused time"""
        if self.game_started_flag == True and self.timer_flag: 
            self.pause_end = pygame.time.get_ticks()
            self.pause_time += self.pause_end - self.pause_start
            self.timer_flag = False

    def get_play_time(self):
        """Calculate play time"""
        self.play_time = pygame.time.get_ticks() - self.start_time - self.pause_time
        return self.play_time







        
        
