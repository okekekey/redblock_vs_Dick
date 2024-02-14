#make duble flip only for premium users

import pygame
import sys
import random

#initialize pygame
pygame.init()

#creating a display surface
screen = pygame.display.set_mode((800, 400))
#creating a reckt of the screen
screen_rect = screen.get_rect()
#screen.fill('Blue')
#creating a name of the screen
pygame.display.set_caption('red block vs dick.exe')
#creating a clock object
clock = pygame.time.Clock()



#ground surface and its rect
ground = pygame.Surface((800, 70))
ground.fill('Green')
ground_rect = ground.get_rect()
ground_rect.bottom = screen_rect.bottom
ground_brown = pygame.Surface((800, 60))
ground_brown.fill((150, 75, 0))
ground_brown_rect = ground_brown.get_rect()
ground_brown_rect.bottom = screen_rect.bottom

#creating new surface
test_surface = pygame.Surface((200, screen_rect.height - ground_rect.height))
test_surface.fill((100, 100, 100))
#test_surface.fill('Gray')

#creating a moving surface dck and placing it on the ground
dck_size = 30
dck = pygame.Surface((dck_size, dck_size))
dck.fill('Pink')
dck_rect = dck.get_rect()
dck_rect.bottom = ground_rect.top
dck_rect.x = 650

#creating bonus lives
spawn_rate = screen_rect.width * 10 #default 10
bonus_live = pygame.Surface((20, 25))
bonus_live.fill('White')
bonus_live_rect = bonus_live.get_rect()
bonus_live_rect.right = random.randint(spawn_rate, int(spawn_rate * 4))
bonus_live_rect.top = random.randint(bonus_live_rect.height, screen_rect.centery)

#creating a playa
player = pygame.Surface((50, 100), pygame.SRCALPHA) #needs to make a proper rotation
player.fill('Red')
player_rect = player.get_rect()
player_rect.bottom = ground_rect.top
player_rect.centerx = 100
player_gravity = 0 
rotation_angle = 0

#creating balls
# balls_width = player_rect.width + 2 * dck_rect.width
# balls = pygame.Surface((balls_width, dck_rect.height))
# balls.fill('Pink')
# balls_rect = balls.get_rect()
# balls_rect.midbottom = player_rect.midbottom

game_active_flag = False

game_time = 0


#to create a text there are 3 steps: 1. creating a font 2.creating image or surface of the text 3. blit this image to the surface
#creating a font (font type, size) requires to import font file to the directory
test_font = pygame.font.Font(None, 60)
#creating a surface of the text. (the text itself, anty analysing (smothes ages of the text) True or False, color)
text_surface = test_font.render('My dick sucks...', True, 'Purple')
#creating rect of the text just to aligned int in the center
text_surface_rect = text_surface.get_rect()
text_surface_rect.center = (screen_rect.centerx, screen_rect.centery - text_surface_rect.height / 2)

#start text
start_font = pygame.font.Font(None, 35)
text_start = start_font.render('To start dodging my dicks press spacebar', True, 'Purple')
text_start_rect = text_start.get_rect()
text_start_rect.center = (screen_rect.centerx, screen_rect.bottom - text_start_rect.height)
#game name text
game_name_font = pygame.font.Font(None, 40)
text_game = game_name_font.render('Red Block vs DICK!', True, 'Pink')
text_game_rect = text_game.get_rect()
text_game_rect.center = (screen_rect.centerx, screen_rect.centery - text_start_rect.height)

#score
counter_dck = 0  
counter_dck_prev = counter_dck - 1
score_font = pygame.font.Font(None, 30)
condition_dck_met = False

#lives
counter_lives = 3
live_font = pygame.font.Font(None, 30)

#clock
start_time = 0
clock_font = pygame.font.Font(None, 40)

#text you suck!
suck_font = pygame.font.Font(None, 220)
text_you_suck = suck_font.render('You suck!', True, 'Black')
text_you_suck_rect = text_you_suck.get_rect()
text_you_suck_rect.center = (screen_rect.centerx, screen_rect.centery - text_start_rect.height)

#charge
charge = 100
charge_font = pygame.font.Font(None, 27)
text_charge = charge_font.render(f'{charge}%', True, 'Black')
text_charge_rect =text_charge.get_rect()
#recharge and discharge
overheat = False
recharge_delay = 0
recharge_delay_max = 120
#overheat
overheat_font = pygame.font.Font(None, 36)
text_overheat = overheat_font.render('OVERHEAT!', True, 'Red')
text_overheat_rect = text_overheat.get_rect()
text_overheat_rect.midbottom= player_rect.midtop

#lvl speed
lvl_speed_start = 5 #5 default
lvl_speed = lvl_speed_start
lvl_step_number = 10 #10 default

start_point = player_rect.midright
end_point = pygame.mouse.get_pos()

while True:
    
    """draw all our elements """ 
    """update everything"""

    
    #get and check all the events happening in pygame
    for event in pygame.event.get():
        #checking if any key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
            #start the game after pressing any button
                game_active_flag = True

                #there is a high chance to drop the timer during the play!!!
                #starting the clock count only when game active (skip pause screen)
                if dck_rect.x == 650 or dck_rect.left == screen_rect.right:
                    start_time = pygame.time.get_ticks()

            #jump physics  
            if event.key == pygame.K_SPACE and player_rect.bottom == ground_rect.top and counter_dck < 140:
                #jump height
                player_gravity = -15
            #checking 3rd condition (dck position) just to prevent jump when starting new game, on 140+ lvl start with a jump may lead to a unavoidable collision)  
            elif event.key == pygame.K_SPACE and player_rect.bottom == ground_rect.top and dck_rect.left != screen_rect.right:
                player_gravity = -15

                
        if event.type == pygame.QUIT:
            #oposite to pygame.init(), and it will be throwing a mistake if there is code after
            #to avoid this error need to import sys module and call exit method
            pygame.quit()
            sys.exit()

    if game_active_flag:
        #fill the scriin just to remove the trail of dck
        #im not clearing the screen and prev frames still visible
        screen.fill('Blue')

        #blockimmagetransfer. draws a source Surface onto main? Surface.
        #surface to draw, coordinats or rect
        screen.blit(test_surface, (0,0))  
        #drawing another surface on top of previous one
        screen.blit(ground, ground_rect)              
        screen.blit(ground_brown, ground_brown_rect)

        #drawign text in the screen center after the player jump over dck
        #counting dcks jumped over
        if dck_rect.right < player_rect.left:
            screen.blit(text_surface, text_surface_rect)
            if not condition_dck_met:
                counter_dck += 1
                condition_dck_met = True
        
        #drawing lives
        text_live = live_font.render(f'Lives: {counter_lives}', True, 'Red')
        text_live_rect = text_live.get_rect()
        text_live_rect.center = (screen_rect.right - text_live_rect.right/2 - 10, text_live_rect.bottom)
        screen.blit(text_live, text_live_rect)
    
        #drawing score
        score = score_font.render(f'Score: {counter_dck}', True, 'Darkgrey')
        score_rect = score.get_rect()
        score_rect.center = (score_rect.right/2 + 10, score_rect.bottom)
        screen.blit(score, score_rect)

        #drawing clock
        game_time = pygame.time.get_ticks() - start_time
        clock_surf = clock_font.render(f': {int(game_time/1000)}', True, 'White')
        clock_rect = clock_surf.get_rect()
        clock_rect.midtop = (screen_rect.centerx, clock_rect.centery)
        screen.blit(clock_surf,clock_rect)

        #drawing bonus lives and make it spin or woble
        bonus_live_rotated = pygame.transform.rotate(bonus_live, rotation_angle)
        bonus_live_rotated_rect = bonus_live_rotated.get_rect()
        bonus_live_rotated_rect.center = bonus_live_rect.center
        screen.blit(bonus_live_rotated, bonus_live_rotated_rect)
        #screen.blit(bonus_live, bonus_live_rect)
        #speed of bonus lives
        bonus_live_rect.x -= 10
        #returning bl to the screen
        if bonus_live_rect.right < 0:
            bonus_live_rect.right = random.randint(spawn_rate, int(spawn_rate * 1.5))
            bonus_live_rect.top = random.randint(bonus_live_rect.height, screen_rect.centery)

        #check if mouse pointer colides with a bonus live
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0] and charge > 1:
            #drawing a line on
            start_point = player_rect.midright
            end_point = pygame.mouse.get_pos()
            laser_beem = pygame.draw.line(screen, 'Gold', start_point, end_point, 3)
            if bonus_live_rect.collidepoint(mouse_pos) and not overheat:
                bonus_live_rect.right = random.randint(spawn_rate, int(spawn_rate * 1.5))
                bonus_live_rect.top = random.randint(bonus_live_rect.height, screen_rect.centery)
                counter_lives += 1
        
        #drawing player 
        player.fill('Red')       
        if player_rect.bottom == ground_rect.top:    
            screen.blit(player, player_rect)
        #rotate player during the jump (frontflip)
        else:
            rotation_angle += 24 #default 12 full flip
            player_rotated = pygame.transform.rotate(player, -rotation_angle)
            player_rotated_rect = player_rotated.get_rect()
            player_rotated_rect.center = player_rect.center
            screen.blit(player_rotated, player_rotated_rect)

        #check if player colides with a bonus lives        
        if bonus_live_rect.colliderect(player_rect):
            bonus_live_rect.right = random.randint(spawn_rate, int(spawn_rate * 1.5))
            bonus_live_rect.top = random.randint(bonus_live_rect.height, screen_rect.centery)
            counter_lives += 1

        #drawing charge %
        text_charge = charge_font.render(f'{charge}%', True, 'Black')
        text_charge_rect = text_charge.get_rect()
        text_charge_rect.center = player_rect.center
        screen.blit(text_charge, text_charge_rect)
        

        #some very complicated logic
        #to avoid dead loop when charge reaches 0 which then causes overheat and making furhter impossible to recharge. 
        #need to arrange all this blocks in such a sequence 
        
        #overheat event dropper
        overheat_event = 0
        #overheat checker
        if charge == 0:
            overheat = True
            overheat_event = pygame.USEREVENT + 1

        #discharge and charge
        if mouse_button[0] and charge > 0 and not overheat:
            charge -= 1
        elif charge < 100 and recharge_delay == 0: 
            charge +=1

        #delay in charging when overheated
        if overheat_event:
            recharge_delay = recharge_delay_max
        elif recharge_delay > 0:
            recharge_delay -= 1
            text_overheat_rect = text_overheat.get_rect()
            text_overheat_rect.midbottom = player_rect.midtop
            screen.blit(text_overheat, text_overheat_rect)
            if recharge_delay == 0:
                overheat = False

        
        #drawing a moving surface dick
        dck = pygame.Surface((dck_size, dck_size))
        dck.fill('Pink')
        screen.blit(dck, dck_rect)
        #speed of dck
        dck_rect.x -= lvl_speed

#different type of weapon LASER GUN
        #checking if laser_beem colides with dck_rect
        # if mouse_button[0] and not overheat:
        #     if dck_rect.clipline(start_point, end_point):
        #         dck_size = 20
        #         #store the x coordinat of dck
        #         x = dck_rect.x
        #         dck_rect = dck.get_rect()
        #         dck_rect.x = x
        #         dck_rect.bottom = ground_rect.top

#possibly add a dck health 
#different type of weapon RIFLE just need to replace line with bullet     
        #checking if mouse colides with dck_rect (after adding get_pressed it started to work slow)
        if event.type == pygame.MOUSEMOTION:
            mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0] and dck_rect.collidepoint(event.pos) and not overheat:
            dck_size = 20
            #store the x coordinat of dck
            x = dck_rect.x
            dck_rect = dck.get_rect()
            dck_rect.x = x
            dck_rect.bottom = ground_rect.top

        #returning dck back to the screen
        if dck_rect.x < 0 - dck_rect.width:
            dck_size = 30
            dck = pygame.Surface((dck_size, dck_size))                        
            dck_rect = dck.get_rect()
            dck_rect.bottom = ground_rect.top
            dck_rect.left = screen_rect.right
            condition_dck_met = False

        #lvl up
        #using the prev score to increase speed only when jumped over dck (catching this precice moment)
        if counter_dck > 1 and counter_dck != counter_dck_prev:
            #closing the window of this moment
            counter_dck_prev = counter_dck
            #increasing speed for only 1 iteration (cause the window is closed)
            if counter_dck % lvl_step_number == 0:
                lvl_speed += 1

        #gravity of the player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > ground_rect.top:
            player_rect.bottom = ground_rect.top
        

        #check if player colides with dck
        if player_rect.colliderect(dck_rect) and counter_lives > 0:
            #redrawing surfaces to hide rotating dick
            screen.blit(test_surface, (0, 0))
            screen.blit(score, score_rect)
            #drawing dick rip
            player.fill('Pink')
            dck = pygame.Surface((dck_size, dck_size))
            dck_rect = dck.get_rect()
            dck_rect.bottom = ground_rect.top
            dck_rect.left = player_rect.right
            dck.fill('Pink')
            screen.blit(dck, dck_rect)
            player_rect.bottom = ground_rect.top
            screen.blit(player, player_rect)
            pygame.draw.line(screen, 'Red', player_rect.midtop, (player_rect.centerx, player_rect.y + dck_size/2), 3)

            #reset postion of dck and size
            dck_size = 30
            dck = pygame.Surface((dck_size, dck_size))
            dck_rect = dck.get_rect()
            dck_rect.bottom = ground_rect.top
            dck_rect.left = screen_rect.right
            #logic
            counter_lives -= 1
            screen.fill('Blue', text_live_rect)
            text_live = live_font.render(f'Lives: {counter_lives}', True, 'Red')
            screen.blit(text_live, text_live_rect)
            game_active_flag = False
            start_time = pygame.time.get_ticks()
        
        #end screen
        if counter_lives == 0:
            screen.fill('Pink')
            screen.blit(text_you_suck, text_you_suck_rect)
            screen.blit(score, score_rect)
            screen.blit(clock_surf, clock_rect)
            text_live = live_font.render(f'Lives: {counter_lives}', True, 'Red')
            screen.blit(text_live, text_live_rect)
            counter_dck = 0
            counter_lives = 3
            lvl_speed = lvl_speed_start
    
    #start screen    
    else:
        #draw start text
        screen.blit(text_start, text_start_rect)
        if game_time == 0:
                       
            #draw game name
            screen.blit(text_game, text_game_rect)
            #drawing dck on the start screen
            dck = pygame.Surface((dck_size, dck_size))
            dck.fill('Pink')
            dck_rect.bottom = ground_rect.top
            screen.blit(dck, dck_rect)
            screen.blit(player, player_rect)
        



    #update display
    pygame.display.update()
    #making while loop run not faster 60 fps appr 1 while loop each 60 ms
    clock.tick(60) # default 60

 