# fix colision check with rotating block

import pygame
import sys
import math

from settings import Settings
from background import Background
from player import Player
from dick import Dick
from bonus_live import BonusLive

def check_events(player, dick, settings, background, stats):
    """Respond to keypresses and mnouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score(settings)
            sys.exit()       
        #jumping
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player, settings, background, stats) 
        # when paused make it blink
        elif event.type == background.blink_event:
            background.show_text = not background.show_text

        # elif event.type == pygame.KEYDOWN:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         shoot(settings, player)
                           
def check_keydown_events(event, player, settings, background, stats):
    """Respond to keypresses"""
    #space, esc, q, p
    if event.key == pygame.K_SPACE:
        
        player_jump(player, background)
        player.ground_flag = False
        settings.game_started_flag = True
        settings.game_active_flag = True
        
        settings.get_pause_end()
        #sounds.moving(ship)
        # if dck_rect.x == 650 or dck_rect.left == screen_rect.right:
        #   start_time = pygame.time.get_ticks()


    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
        stats.save_high_score(settings)
        sys.exit()

    #pause and unpause
    elif event.key == pygame.K_p and settings.game_active_flag == True:
        settings.game_active_flag = False
        settings.get_pause_start()  
    elif event.key == pygame.K_p and settings.game_active_flag == False and settings.game_started_flag == True:
        settings.game_active_flag = True
        settings.get_pause_end()

def reset_timers(settings):
    """Reset timers"""
    settings.start_time = 0
    settings.pause_start = 0
    settings.pause_end = 0
    settings.pause_time = 0


    def start_game():
        """Reset all things to start new game"""
        
        # # Reset the game settings
        # ai_settings.initialize_dynamic_settings()
        # # Hide the mouse cursor.
        # pygame.mouse.set_visible(False)
        # # Reset the game statistics.
        # stats.reset_stats()
        # stats.game_active = True
        # # Reset the scoreboard images.
        # sb.prep_score()
        # sb.prep_high_score()
        # sb.prep_level()
        # sb.prep_ships()
        # # Empty the list of aliens and bullets.
        # aliens.empty()
        # bullets.empty()
        # # Create a new fleet and center the ship.
        # create_fleet(ai_settings, screen, ship, aliens)
        # ship.center_ship()

def update_player(player, background):
    """Update the player's postionion and atributes"""
    #position
    player.gravity += 1
    player.rect.y += player.gravity
    if player.rect.bottom >= background.ground_rect.top:
        player.rect.bottom = background.ground_rect.top
        player.ground_flag = True
    else:
        player.rotation_angle += 20 #default 10 = 1.5 flips
        player.image_rotated = pygame.transform.rotate(player.image_copy,
                                                           -player.rotation_angle)
        player.rotated_rect = player.image_rotated.get_rect()
        player.rotated_rect.center = player.rect.center
    #weapon ammo/charge
    discharge_charge_weapon(player)

def player_jump(player, background):
    """Make player to jump"""
    if player.rect.bottom == background.ground_rect.top and player.ground_flag == True:
        player.gravity = - player.jump_height

def discharge_charge_weapon(player):
    """Unload and reload weapon"""
    overheating(player)
    overheat_cooldown(player)
    mouse_button_pressed = pygame.mouse.get_pressed()
    if mouse_button_pressed[0] and player.ammo_charge >= 0 and not player.overheating:
        player.ammo_charge -= player.discharge_speed
    elif player.ammo_charge < 100 and player.recharge_delay == 0:
        player.ammo_charge += player.charge_speed
    elif player.ammo_charge > 100:
        player.ammo_charge = 100
    
def overheating(player):
    """Checks if a weapon is overheated"""
    if player.ammo_charge < 0:
        player.overheating = True
        player.recharge_delay = player.recharge_delay_max
        player.ammo_charge = 0 # need to assigne to stop dead loop

def overheat_cooldown(player):
    """Delays reloading weapon when overheated"""
    if player.recharge_delay > 0:
        player.recharge_delay -= 1
    elif player.recharge_delay == 0:
        player.overheating = False 

def shoot_laser(settings, player):
    """Draw laser beam """
    mouse_pos = pygame.mouse.get_pos()
    mouse_button_pressed = pygame.mouse.get_pressed()
    if mouse_button_pressed[0] and not player.overheating:
        pygame.draw.line(settings.screen, 'Red', player.rect.center,
                          mouse_pos, 3)

def update_dick(player, dick, settings, background):
    """Update the Dick position on the screen"""
    dick.rect.x -= settings.lvl_speed
    dick_collision(player, dick, settings, background)
    increase_score(player, dick, settings)
    dick_transfer(dick, settings, background)
    if dick.rect.left < settings.screen_rect.right and not settings.start_timer_flag:
        start_timer(settings)
        settings.start_timer_flag = True
    increase_speed_level(settings)
    dicrease_hp_dick(dick, player, settings, background)
    dick_check_hp(dick, settings, background)
    dick_change_imager(dick, settings, background)
    
def dick_transfer(dick, settings, background):
    """Transfer dick left to right after reaching left ednge of the screen"""
    if dick.rect.right < settings.screen_rect.left:
        dick.drop_flag()
        dick.reset_hp()
        dick.choose_image()
        dick.load_image(settings)
        dick.rect.left = settings.screen_rect.right
        dick.rect.bottom = background.ground_rect.top
        settings.dick_pass_flag = False  
            
def dick_collision(player, dick, settings, background):
    """Responde to player-dick collision"""
    #if it register collisions not correctly it is because of the 2nd condition
    if player.rect.colliderect(dick.rect): #or player.rotated_rect.colliderect(dick.rect):
        settings.current_lives -= 1
        settings.game_active_flag = False
        dick.reset(settings, background)
        reset_timers(settings)

def dicrease_hp_dick(dick, player, settings, background):
    """Checks if mouse pointer colides with dick rect and decreases dick hp"""
    mouse_button_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_button_pressed[0] and dick.rect.collidepoint(mouse_pos) and settings.game_started_flag and dick.health > 0 and not player.overheating:
        dick.health -= 5
        background.draw_dick_hp(dick)
        
def dick_check_hp(dick, settings, background):
    """Check dicks HP and sets flags for scoring and chng imgs"""       
    if -100 < dick.health <= 0:
        dick.small_dick_flag = True
        settings.dick_kill_flag = True
        dick.health = -1000
        
def dick_change_imager(dick, settings, background):
    """Replace image of dick on the go"""      
    if dick.small_dick_flag:
        #store the x coordinat before transforming to restore the position
        x = dick.rect.x
        dick.choose_image()
        dick.load_image(settings)
        dick.rect.bottom = background.ground_rect.top
        dick.rect.x = x

def start_timer(settings):
    '''Starts timer'''
    settings.start_time = pygame.time.get_ticks()

def increase_score(player, dick, settings):
    '''+1 score for jumping over dick and killing it'''
    if dick.rect.right < player.rect.left and not settings.dick_pass_flag:
        settings.current_score += 1
        settings.dick_pass_flag = True
    elif dick.small_dick_flag and settings.dick_kill_flag:
        settings.current_score += 1
        settings.dick_kill_flag = False

def increase_speed_level(settings):
    """Increase dick speed each 10 lvls, lvl up speed"""
    if settings.current_score > 1 and settings.current_score != settings.prev_score:
        settings.prev_score = settings.current_score
        if settings.current_score % settings.lvl_speed_step == 0:
            settings.lvl_speed += 1

def update_bonus_live(player, bonus_live, settings):
    """Update BL position on the screen"""
    bonus_live.rect.x -= settings.lvl_speed
    if bonus_live.rect.right < settings.screen_rect.left:
        bonus_live.place_postion()
    bonus_live_collision(player, bonus_live, settings)
            
def bonus_live_collision(player, bonus_live, settings):
    """Responde to player-BL and mouse pointer collision"""
    mouse_button_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if player.rect.colliderect(bonus_live.rect) or player.rotated_rect.colliderect(bonus_live.rect) or (mouse_button_pressed[0] and bonus_live.rect.collidepoint(mouse_pos) and not player.overheating):
        settings.current_lives += 1
        bonus_live.place_postion()
    