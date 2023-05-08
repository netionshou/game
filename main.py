import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1044, 587))
pygame.display.set_caption("kakashki")
icon = pygame.image.load('addimages/IMG_3900.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('addimages/bg1.png').convert_alpha()

walk_left = [
    pygame.image.load('addimages/p_left/s1.png').convert_alpha()
,
    pygame.image.load('addimages/p_left/s2.png').convert_alpha()
,
    pygame.image.load('addimages/p_left/s3.png').convert_alpha()
,
    pygame.image.load('addimages/p_left/s4.png').convert_alpha()

]
walk_right = [
    pygame.image.load('addimages/p_right/u1.png').convert_alpha()
,
    pygame.image.load('addimages/p_right/u2.png').convert_alpha()
,
    pygame.image.load('addimages/p_right/u3.png').convert_alpha()
,
    pygame.image.load('addimages/p_right/u4.png').convert_alpha()

]



ghost = pygame.image.load('addimages/pngegg2.png').convert_alpha()

ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 410

is_jump = False
jump_count = 9

bg_sound = pygame.mixer.Sound('sounds/POL-azure-waters-short.wav')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('fonts/ofont.ru_Pixeloid Sans.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193,196,199))
restart_label = label.render('Играть заново', False, (115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(350, 350))


bullets_left = 5
bullet = pygame.image.load('addimages/pula.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:
    pygame.display.update()
    screen.blit(bg, (bg_x, 0)) #pзадник
    screen.blit(bg, (bg_x + 1044, 0))

    if gameplay:

    #ДЛЯ БОЯ КВАДРАТ НА ПЕРСОНАЖЕ
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))


        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 50

                if el.x < -50:
                    ghost_list_in_game.pop()

                if player_rect.colliderect( el ):
                    gameplay = False



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
    # ходьба
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT]and player_x < 577:
            player_x += player_speed
    #прыжок
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count**2)/2 #прыжок пплавный
                else:
                    player_y += (jump_count**2)/2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1044:
            bg_x = 0
        else:
            bg_x -=2




        if bullets:
            for el in bullets:
                screen.blit(bullet,(el.x, el.y))
                el.x += 4

                if el.x > 1044:
                    bullets.pop(i)


                if ghost_list_in_game:
                    for(index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):  #столкновение моба с врагом
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((87, 88 , 89))
        screen.blit(lose_label,(350,250))
        screen.blit(restart_label, restart_label_rect )

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:

            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer :
            ghost_list_in_game.append(ghost.get_rect(topleft=(1044,410)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_c and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft =( player_x + 30, player_y +10)))
            bullets_left -= 1
    clock.tick(15)