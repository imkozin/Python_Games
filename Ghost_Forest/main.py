import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359)) #flags=pygame.NOFRAME
pygame.display.set_caption("Ghost Forest")
icon = pygame.image.load('Week4/Day5/images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

# Player
bg = pygame.image.load('Week4/Day5/images/bg.png').convert()
player = pygame.image.load('Week4/Day5/images//left/1.png').convert_alpha()
walk_left = [
    pygame.image.load('Week4/Day5/images/left/1.png'),
    pygame.image.load('Week4/Day5/images/left/2.png'),
    pygame.image.load('Week4/Day5/images/left/3.png'),
    pygame.image.load('Week4/Day5/images/left/4.png')
]

walk_right = [
    pygame.image.load('Week4/Day5/images/right/5.png'),
    pygame.image.load('Week4/Day5/images/right/6.png'),
    pygame.image.load('Week4/Day5/images/right/7.png'),
    pygame.image.load('Week4/Day5/images/right/8.png')
]


player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 250

is_jumping = False
jump_count = 8

# Monster
ghost = pygame.image.load('Week4/Day5/images/ghost.png').convert_alpha()
# ghost_x = 620
ghost_list_in_game = []
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

#Background
bg_sound = pygame.mixer.Sound('Week4/Day5/melody.mp3')
bg_sound.play()

label = pygame.font.Font('Week4/Day5/Roboto/Roboto-Black.ttf', 50)
lose_label = label.render('GAME OVER!', False, (200, 200, 50))
restart_label = label.render('   Play again', False, (200, 50, 50))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

bullets_left = 5
bullet = pygame.image.load('Week4/Day5/images/bullet.png')
bullets = []

gameplay = True

running = True
while running:


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -20:
                    ghost_list_in_game.pop(i)
        
                if player_rect.colliderect(el):
                    gameplay = False
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jumping:
            if keys[pygame.K_UP]:
                is_jumping = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0
        

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el) :
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

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
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 235)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(15)