import pygame
import sys
import math
from bullets import Bullets


def check_events(player, dick, settings, background, stats, bonus_live, guns, menu):
    """Respond to keypresses and mnouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score(settings)
            settings.save_settings()
            sys.exit()
        # screen resize
        elif event.type == pygame.VIDEORESIZE:
            if event.w < settings.screen_sizes[6][0]:
                event.w = settings.screen_sizes[6][0]
            if event.h < settings.screen_sizes[6][1]:
                event.h = settings.screen_sizes[6][1]
            settings.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            settings.screen_rect = settings.screen.get_rect()
            #settings.calculate_ss_variables(player)
            resize(settings, background, player, dick, bonus_live, menu)


            # if not settings.game_active_flag:     
            #     player.place(background)
            #     dick.initial_postion(background)                            
                                   
        # jumping
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player, settings, background, stats, guns, menu) 
        # when paused make it blink
        elif event.type == background.blink_event:
            background.show_text = not background.show_text
                           
def check_keydown_events(event, player, settings, background, stats, guns, menu):
    """Respond to keypresses"""
    #space, esc, q, p
    if event.key == pygame.K_SPACE and menu.current_status != menu.all_states[2]:
        
        player_jump(player, background)
        player.ground_flag = False
        settings.game_started_flag = True
        settings.game_active_flag = True
        menu.current_status = menu.all_states[0]
          
        settings.get_pause_end()
        #sounds.moving(ship)
        # if dck_rect.x == 650 or dck_rect.left == screen_rect.right:
        #   start_time = pygame.time.get_ticks()

    elif event.key == pygame.K_q:
        stats.save_high_score(settings)
        settings.save_settings()
        sys.exit()

    # menu
    elif event.key == pygame.K_ESCAPE and menu.current_status == menu.all_states[0]:
        settings.game_active_flag = False
        settings.get_pause_start()
        menu.current_status = menu.all_states[1]
    elif event.key == pygame.K_ESCAPE and menu.current_status == menu.all_states[1] and settings.game_started_flag == True:
        settings.game_active_flag = True
        settings.get_pause_end()
        menu.current_status = menu.all_states[0]
    # go back
    elif event.key == pygame.K_ESCAPE and menu.current_status == menu.all_states[2]:
        menu.current_status = menu.all_states[1]
    # game not started
    elif event.key == pygame.K_ESCAPE and menu.current_status == menu.all_states[1]:
        menu.current_status = menu.all_states[0]

              
    # pause and unpause
    elif event.key == pygame.K_p and settings.game_active_flag == True:
        settings.game_active_flag = False
        settings.get_pause_start()  
    elif event.key == pygame.K_p and settings.game_active_flag == False and settings.game_started_flag == True:
        settings.game_active_flag = True
        settings.get_pause_end()
    
    elif event.key == pygame.K_1 or pygame.K_2 or pygame.K_3: 
        change_weapon(guns, event)


def resize(settings, background, player, dick, bonus_live, menu):
    """Resizes and rearranges elements after changing screen size"""
    background.resize(settings)
    player.resize(settings, background)
    player.rotated_resize(settings, background)
    dick.resize(settings, background)
    bonus_live.bonus_live_resize(settings)
    menu.resize(settings, player)

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

def update_player(player, background, dick, settings, guns):
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
    guns.discharge_charge_weapon()

def player_jump(player, background):
    """Make player to jump"""
    if player.rect.bottom == background.ground_rect.top and player.ground_flag == True:
        player.gravity = - player.jump_height

def update_dick(player, dick, settings, background, guns):
    """Update the Dick position on the screen"""
    dick.rect.x -= settings.lvl_speed
    dick_collision(player, dick, settings, background)
    increase_score(player, dick, settings)
    dick_transfer(dick, settings, background)
    if dick.rect.left < settings.screen_rect.right and not settings.start_timer_flag:
        start_timer(settings)
        settings.start_timer_flag = True
    increase_speed_level(settings)
    dicrease_hp_dick(dick, player, settings, background, guns)
    dick_check_hp(dick, settings, background)
    dick_change_image(dick, settings, background)
    game_over(settings)
    
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
    if settings.current_lives > 0 and (player.rect.colliderect(dick.rect) or player.rotated_rect.colliderect(dick.rect)):
        settings.current_lives -= 1
        settings.game_active_flag = False
        dick.reset(settings, background)
        reset_timers(settings)

#need to measure performance somehow
def game_over(settings):
    """Check lives and stops the game if it reaches 0"""
    if settings.current_lives < 1:
        settings.game_over_flag = True
        if settings.lvl_speed < 100:
            settings.lvl_speed = 100
        elif settings.lvl_speed < 500:
            settings.lvl_speed += 3
        else:
            settings.lvl_speed = 300

# rethink logics here 
def dicrease_hp_dick(dick, player, settings, background, guns):
    """Checks if mouse pointer colides with dick rect and decreases dick hp"""
    mouse_button_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_button_pressed[0] and dick.rect.collidepoint(mouse_pos) and settings.game_started_flag and dick.health > 0 and not guns.overheating_flag:
        dick.health -= guns.current_weapon_stats['dmg']
        background.draw_dick_hp(dick)
        
def dick_check_hp(dick, settings, background):
    """Check dicks HP and sets flags for scoring and chng imgs"""       
    if -100 < dick.health <= 0:
        dick.small_dick_flag = True
        settings.dick_kill_flag = True
        dick.health = -1000
        
def dick_change_image(dick, settings, background):
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
    if dick.rect.right < player.rect.left and not settings.dick_pass_flag and not settings.game_over_flag:
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

def update_bonus_live(player, bonus_live, settings, guns):
    """Update BL position on the screen"""
    bonus_live.rect.x -= settings.lvl_speed
    if bonus_live.rect.right < settings.screen_rect.left:
        bonus_live.place_postion()
    bonus_live_collision(player, bonus_live, settings, guns)
            
def bonus_live_collision(player, bonus_live, settings, guns):
    """Responde to player-BL and mouse pointer collision"""
    mouse_button_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if player.rect.colliderect(bonus_live.rect) or player.rotated_rect.colliderect(bonus_live.rect) or (mouse_button_pressed[0] and bonus_live.rect.collidepoint(mouse_pos) and not guns.overheating_flag):
        settings.current_lives += 1
        bonus_live.place_postion()

def change_weapon(guns, event):
    """Change weapon when pressing 123"""
    #need to do a check if weapon unlocked
    if event.key == 49 and guns.weapon_slot_1: # 1 ak47
        guns.current_weapon = guns.weapons[1]
        guns.laod_weapon_stats()
        guns.ammo_capacity = -1
    elif event.key == 50 and guns.weapon_slot_2: # 2 laser
        guns.current_weapon = guns.weapons[2]
        guns.laod_weapon_stats()
        guns.ammo_capacity = 0
    elif event.key == 51 and guns.weapon_slot_3: # 3 knife
        guns.current_weapon = guns.weapons[3]
        guns.laod_weapon_stats()
        guns.ammo_capacity = 0

def shoot(bullets, guns, player):
        """"""
        speed_factor = 30
        
        if pygame.mouse.get_pressed()[0]:
            bullets.mouse_x, bullets.mouse_y = pygame.mouse.get_pos()
            # angle, bullet direction
            bullets.dx = bullets.mouse_x - guns.rect.centerx
            bullets.dy = bullets.mouse_y - guns.rect.centery
            bullets.angle = math.atan2(bullets.dy, bullets.dx)
            # initial position
            bullets.bullet_x = guns.rect.centerx
            bullets.bullet_y = guns.rect.centery
            # velocity
            bullets.bullet_vel_x = speed_factor * math.cos(bullets.angle)
            bullets.bullet_vel_y = speed_factor * math.sin(bullets.angle)   

            new_bullet = Bullets(guns, player)
            new_bullet.bullet_vel_x = bullets.bullet_vel_x
            new_bullet.bullet_vel_y = bullets.bullet_vel_y
            bullets.add(new_bullet)