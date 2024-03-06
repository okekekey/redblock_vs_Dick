import pygame
import sys



class Menu():
    """A class to draw menue"""

    def __init__(self, settings, player) -> None:
        """"""

        self.screen = settings.screen 
        self.screen_rect = self.screen.get_rect() 

        # images
        self.resume_image = pygame.image.load('images/menu/resume.png').convert_alpha()    
        self.options_image = pygame.image.load('images/menu/options.png').convert_alpha()
        self.quit_image = pygame.image.load('images/menu/quit.png').convert_alpha()
        self.video_image = pygame.image.load('images/menu/video.png').convert_alpha()
        self.audio_image = pygame.image.load('images/menu/audio.png').convert_alpha()
        self.keys_image = pygame.image.load('images/menu/keys.png').convert_alpha()
        self.back_image = pygame.image.load('images/menu/back.png').convert_alpha()

        self.resume_image_copy = self.resume_image.copy()
        self.options_image_copy = self.options_image.copy()
        self.quit_image_copy = self.quit_image.copy()
        self.video_image_copy = self.video_image.copy()
        self.audio_image_copy = self.audio_image.copy()
        self.keys_image_copy = self.keys_image.copy()
        self.back_image_copy = self.back_image.copy()

        self.resize(settings, player)


        self.all_states = ['play', 'menu', 'options', 'video', 'audio', 'keys']
        self.current_status = self.all_states[0]

        self.pressed = False


    def update(self, settings, stats):
        """"""
        pos = pygame.mouse.get_pos()

        # resume
        if self.resume_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and self.current_status == 'menu':
            if self.resume_rect.collidepoint(pos) and self.pressed == False:    
                self.current_status = self.all_states[0]
                settings.game_active_flag = True
                settings.get_pause_end()
        # options
        elif self.options_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and self.current_status == 'menu':
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                self.current_status = self.all_states[2]
            
        # quit
        elif self.quit_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and self.current_status == 'menu':
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                stats.save_high_score(settings)
                settings.save_settings()
                sys.exit()
               
        # video
        elif self.video_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                pass
        
        # audio
        elif self.audio_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]and self.current_status == 'options':
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                pass

        # keys
        elif self.keys_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]and self.current_status == 'options':
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                pass

        # back
        elif self.back_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and self.current_status == 'options':
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                self.current_status = self.all_states[1]
                
        
        
        


        
        
        # to register a click only inside the rect
        if pygame.mouse.get_pressed()[0]:
            self.pressed = True
        else:
            self.pressed = False

        


    def draw(self):
        """"""
        if self.current_status == self.all_states[1]:
            self.screen.blit(self.resume_image, self.resume_rect)
            self.screen.blit(self.options_image, self.options_rect)
            self.screen.blit(self.quit_image, self.quit_rect)

        if self.current_status == self.all_states[2]:
            self.screen.blit(self.video_image, self.video_rect)
            self.screen.blit(self.audio_image, self.audio_rect)
            self.screen.blit(self.keys_image, self.keys_rect)
            self.screen.blit(self.back_image, self.back_rect)

        # if self.current_status == self.all_states[3]:
        #     self.screen.blit(self.video_image, self.video_rect)
        #     self.screen.blit(self.audio_image, self.audio_rect)
        #     self.screen.blit(self.keys_image, self.keys_rect)
        #     self.screen.blit(self.back_image, self.back_rect)

     

    def resize(self, settings, player):
        """Resize menu buttons according to the screen size"""
        self.screen = settings.screen 
        self.screen_rect = self.screen.get_rect() 

        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.resume_image = pygame.transform.scale(self.resume_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.options_image = pygame.transform.scale(self.options_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.quit_image = pygame.transform.scale(self.quit_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.video_image = pygame.transform.scale(self.video_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.audio_image = pygame.transform.scale(self.audio_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.keys_image = pygame.transform.scale(self.keys_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        self.back_image = pygame.transform.scale(self.back_image_copy, (settings.screen_rect.width // (player.h_divider * 2), settings.screen_rect.height // (player.h_divider * 1.5)))
        
        self.indent(player)

        # rects
        self.resume_rect = self.resume_image.get_rect(midtop = (self.position_1))
        self.options_rect = self.options_image.get_rect(midtop = (self.position_2))
        self.quit_rect = self.quit_image.get_rect(midtop = (self.position_3))
        self.video_rect = self.video_image.get_rect(midtop = (self.position_1))
        self.audio_rect = self.audio_image.get_rect(midtop = (self.position_2))
        self.keys_rect = self.keys_image.get_rect(midtop = (self.position_3))
        self.back_rect = self.back_image.get_rect(midtop = (self.position_4))

    def indent(self, player):
        """Creates screen indentation to attach buttons to it"""
        self.top_indent = self.screen_rect.height // player.h_divider 
        self.indent_step = self.screen_rect.height // player.h_divider 

        self.position_1 = (self.screen_rect.centerx, self.top_indent + (self.indent_step * 0))
        self.position_2 = (self.screen_rect.centerx, self.top_indent + (self.indent_step * 1))
        self.position_3 = (self.screen_rect.centerx, self.top_indent + (self.indent_step * 2))
        self.position_4 = (self.screen_rect.centerx, self.top_indent + (self.indent_step * 3))
        self.position_5 = (self.screen_rect.centerx, self.top_indent + (self.indent_step * 4))



