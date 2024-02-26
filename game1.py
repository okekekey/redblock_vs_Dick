#make duble flip only for premium users
# add sound design
# add main menu (settings (screen size, music), weapons, player (skins, number of backflips), exit)
# pack my game PyInstaller (for Python applications) or Inno Setup (for creating win installers)

import pygame
import sys
import random

from settings import Settings
from player import Player
from dick import Dick
from background import Background
from bonus_live import BonusLive
from gamestats import GameStats
import game_functions as gf


#initialize pygame
pygame.init()

# Settings
settings = Settings()





# Creating instances


background = Background(settings)
player = Player(settings)
dick = Dick(settings, background)
time = 0 
bonus_live = BonusLive(settings)
stats = GameStats()


clock = pygame.time.Clock()

background.draw_ground()
dick.initial_postion(background)
player.place(background)

running = True
while running:
    #making while loop run not faster 60 fps appr 1 while loop each 60 ms
    clock.tick(60) # default 60 fps

    gf.check_events(player, dick, settings, background, stats)

    

    if settings.game_active_flag:
        
        background.draw_game_screen(time, settings, stats)
        gf.shoot_laser(settings, player)
        #player.update(background)
        player.draw(background)
        
        gf.update_player(player, background)
        gf.update_dick(player, dick, settings, background)
        gf.update_bonus_live(player, bonus_live, settings)
        
        dick.draw(settings)
        background.draw_ammo_charge(player) 
        bonus_live.draw()

        


    else:
        background.draw_pause_screen(time, settings, stats) 

        player.draw(background)
        dick.draw(settings)

        
    
        #settings.screen.blit(settings.surface_indent, settings.screen_indent_rect)
        


    print(settings.current_score, stats.high_score)
            
    time += 1

        


    #update display
    pygame.display.update()



 