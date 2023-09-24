import pygame

pygame.init()

#Screeb size
screen_width =784
screen_height =480
screen = pygame.display.set_mode((screen_width, screen_height))

#Title
pygame.display.set_caption("PangPang")

#FPS
clock = pygame.time.Clock()
#-------------------------------------------------------------------#

# initializing

# 1. game intialization (background, game image, coordination, moving speed, font, collision...)
# background
background = pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/background.png")

# stage (background image includes stage)

ground_height = 50 # character placed on the stage

#character
character = pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/real_character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = (screen_height - character_height- ground_height)

character_to_x=0
character_speed=5

#font 
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"

#weapon
weapon = pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/weapon_test_2.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

#ball
ball_images = [
    pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/real_ball.png"),
    pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/real_ball2.png"),
    pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/real_ball3.png"),
    pygame.image.load("/Users/user/Desktop/VS_code/pygame/pygame_project/images/real_ball4.png")]

#ball speed according to the size
ball_speed_y = [-18, -15, -12, -9]

#ball processing
balls = []

balls.append({
    "pos_x" : 50, 
    "pos_y" : 50,
    "img_idx" : 0, 
    "to_x" : 3,
    "to_y" : -7,
    "init_spd_y" : ball_speed_y[0]
})

weapon_to_remove= -1
ball_to_remove = -1
#Game loop
running = True 
while running:
    dt = clock.tick(60) #FPS setting
    #10 fps == 10 pieces of image at 1 sec
    #50 fps == 50 pieces of image at 1 sec

#2. processing event
    for event in pygame.event.get(): #getting event input
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed  
            elif event.key == pygame.K_SPACE: #weapond using
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x =0
    #3. moving character events                
    character_x_pos += character_to_x

    if character_x_pos <0:
        character_x_pos =0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    # weapon position adjustment
    weapons = [[w[0], w[1]-weapon_speed] for w in weapons]
    #weapons removal if reach to the ceiling
    weapons = [[w[0], w[1]] for w in weapons if w[1]>0]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
    
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # when ball reach to the wall, direction is changed opposite side
        if ball_pos_x < 0 or ball_pos_x >screen_width - ball_width:
            ball_val["to_x"] *=-1

        # y position of ball (bouncing effect)
        if ball_pos_y >= screen_height - ground_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        # to make the ball fall to the ground
        else:
            ball_val["to_y"] += 0.45 


        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    #4. collision processing
    
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
    
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
    # ball and character colide
        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pox_x = weapon_val[0]
            weapon_pox_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # if ball is not the smallest, divide it to the next ball size
                if ball_img_idx < 3:
                    #current ball size
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    #divdied ball size
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    #left ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width/2) -(small_ball_width/2),
                        "pos_y" : ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx" : ball_img_idx +1,
                        "to_x" : -3,
                        "to_y" : -7,
                        "init_spd_y" : ball_speed_y[ball_img_idx +1]})
                    #right ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width/2) -(small_ball_width/2),
                        "pos_y" : ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx" : ball_img_idx +1,
                        "to_x" : 3,
                        "to_y" : -7,
                        "init_spd_y" : ball_speed_y[ball_img_idx +1]})
                break
        else:
            continue
        break

    #removing collided ball or weapon    
    if ball_to_remove >-1:
        del balls[ball_to_remove]
        ball_to_remove=-1

    if weapon_to_remove >-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1

    if len(balls) ==0:
        game_result = "Mission Complete"
        running=False
        
    #5. representing all things on the screen
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(character, (character_x_pos, character_y_pos))
    
    #time calculation
    elapsed_time = (pygame.time.get_ticks() - start_ticks)/1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (0,0,0))
    screen.blit(timer, (10,10))

    if total_time - elapsed_time <=0:
        game_result = "Time Over"
        running = False
    if running == False:
        msg = game_font.render(game_result,True,(0,0,0))
        msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(msg, msg_rect)
    pygame.display.update()

pygame.time.delay(2500)

pygame.quit()