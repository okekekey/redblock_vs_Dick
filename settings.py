#add scalable screen size

import pygame.display

class Settings():
    """A class to store all setting to the red block vs dick game"""

    def __init__(self) -> None:
        """Initialize the game's static settings"""
                
        # getting user screen width and height
        self.desktop_size = pygame.display.get_desktop_sizes()
        for tuple in self.desktop_size:
               self.monitor_width = tuple[0]
               self.monitor_height = tuple[1]

        self.screen_sizes = [(2560, 1440), (1920, 1080), (1600, 900), (1366, 768), (1280, 720), (1024, 576), (350, 200)]

        # Creating screen surface
        self.screen = pygame.display.set_mode(self.screen_sizes[5], pygame.RESIZABLE) 
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('red block vs Dick.exe')
        
        # game start flags
        self.game_started_flag = False # true when firts pressed space
        self.game_active_flag = False # truen when game is running
        self.game_over_flag = False

        # speed
        self.start_speed = 10 #self.monitor_width // 256 #10 default
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

    def calculate_ss_variables(self, player):
        """Calculate player size, jump heigh, dick size and speed of the game based on the game window size"""
        # player width
        if self.screen_rect.width > self.screen_sizes[1][0]: #1920
            player.w_divider = 40
        elif self.screen_rect.width > self.screen_sizes[2][0]: #1600
            player.w_divider = 35
        elif self.screen_rect.width > self.screen_sizes[3][0]: #1366
            player.w_divider = 30
        elif self.screen_rect.width > self.screen_sizes[4][0]: #1280
            player.w_divider = 25
        elif self.screen_rect.width > self.screen_sizes[5][0]: #1024
            player.w_divider = 22
        elif self.screen_rect.width < self.screen_sizes[5][0]: #1024
            player.w_divider = 20
        # player height
        if self.screen_rect.height > self.screen_sizes[1][1]: #1080
            player.h_divider = 10
        elif self.screen_rect.height > self.screen_sizes[2][1]: #900
            player.h_divider = 9
        elif self.screen_rect.height > self.screen_sizes[3][1]: #768
            player.h_divider = 8
        elif self.screen_rect.height > self.screen_sizes[4][1]: #720
            player.h_divider = 8
        elif self.screen_rect.height > self.screen_sizes[5][1]: #576
            player.h_divider = 7
        elif self.screen_rect.height > self.screen_sizes[6][1]: #576
            player.h_divider = 6
        # jump height
        if self.screen_rect.height > self.screen_sizes[1][1]: #1080
            player.jump_height = 26
        elif self.screen_rect.height > self.screen_sizes[2][1]: #900
            player.jump_height = 23
        elif self.screen_rect.height > self.screen_sizes[3][1]: #768
            player.jump_height = 21
        elif self.screen_rect.height > self.screen_sizes[4][1]: #720
            player.jump_height = 21
        elif self.screen_rect.height > self.screen_sizes[5][1]: #576
            player.jump_height = 19
        elif self.screen_rect.height > 450: #450
            player.jump_height = 18
        elif self.screen_rect.height > 350: #350
            player.jump_height = 17
        # game speed
        if self.screen_rect.width > self.screen_sizes[1][0]: #1920
            self.lvl_speed = self.screen_rect.width // 200
        elif self.screen_rect.width > self.screen_sizes[2][0]: #1600
            self.lvl_speed = self.screen_rect.width // 170
        elif self.screen_rect.width > self.screen_sizes[3][0]: #1366
            self.lvl_speed = self.screen_rect.width // 140
        elif self.screen_rect.width > self.screen_sizes[4][0]: #1280
            self.lvl_speed = self.screen_rect.width // 120
        elif self.screen_rect.width > self.screen_sizes[5][0]: #1024
            self.lvl_speed = self.screen_rect.width // 100
        elif self.screen_rect.width > 600: 
            self.lvl_speed = self.screen_rect.width // 80
        elif self.screen_rect.width > self.screen_sizes[6][0]: #350
            self.lvl_speed = self.screen_rect.width // 70


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







        
        
