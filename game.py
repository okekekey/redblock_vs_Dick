# make duble flip only for premium users
# add sound design
# add main menu (settings (screen size, music), weapons, player (skins, number of backflips), exit)
# try to implement upgrade system increasing pover of a weapon
# add animations. dick run. dick death. player death
# pack my game PyInstaller (for Python applications) or Inno Setup (for creating win installers)
# encript data storing to high score prevent from changing it

import pygame
import sys
import random

from settings import Settings
from player import Player
from dick import Dick
from guns import Guns
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
guns = Guns(settings, player)
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

    gf.check_events(player, dick, settings, background, stats, bonus_live, guns)
    #settings.calculate_ss_variables(player)
    

    
    # main game
    if settings.game_active_flag and not settings.game_over_flag:
        
        background.draw_game_screen(time, settings, stats)
        #player.update(background)
        player.draw(background, guns)
        dick.draw(settings)
        guns.draw(settings, player)
        background.draw_ammo_charge(guns) 
        bonus_live.draw()
        
        gf.update_player(player, background, dick, settings, guns)
        gf.update_dick(player, dick, settings, background, guns)
        gf.update_bonus_live(player, bonus_live, settings, guns)
        gf.shoot_laser(settings, guns)

    # game over screen
    elif settings.game_over_flag:
        background.draw_game_screen(time, settings, stats)
        player.draw(background, guns)
        dick.draw(settings)
        guns.draw(settings, player)
        bonus_live.draw()
        
        gf.update_dick(player, dick, settings, background, guns)
        gf.update_bonus_live(player, bonus_live, settings, guns)
        
    # pause screen
    else:
        background.draw_pause_screen(time, settings, stats)
        
        if not settings.game_started_flag: # only needs to draw elements on the go without changing screen size again to move them to prev pos
            gf.resize(settings, background, player, dick, bonus_live)


        player.draw(background, guns)
        dick.draw(settings)
        guns.draw(settings, player)

        
    
        #settings.screen.blit(settings.surface_indent, settings.screen_indent_rect)
        

    #print(settings.game_started_flag, settings.game_active_flag)
    print(settings.screen, player.jump_height, settings.lvl_speed)

            
    time += 1

        


    #update display
    pygame.display.update()



 