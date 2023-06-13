import pygame
import random
import psycopg2
from db import highest_score

pygame.init()

#Global constants
screen_height = 600
screen_width = 1100

screen = pygame.display.set_mode((screen_width, screen_height))

dino = pygame.image.load('Dino/Images/DinoStart.png').convert_alpha()

running = [pygame.image.load('Dino/Images/DinoRun1.png').convert_alpha(),pygame.image.load('Dino/Images/DinoRun2.png').convert_alpha()]

jumping = pygame.image.load('Dino/Images/DinoJump.png').convert_alpha()

bending = [pygame.image.load('Dino/Images/DinoBend1.png').convert_alpha(), pygame.image.load('Dino/Images/DinoBend2.png').convert_alpha()]

large_cactus = [pygame.image.load('Dino/Images/LargeCactus1.png').convert_alpha(), pygame.image.load('Dino/Images/LargeCactus2.png').convert_alpha(), pygame.image.load('Dino/Images/LargeCactus3.png').convert_alpha()]

small_cactus = [pygame.image.load('Dino/Images/SmallCactus1.png').convert_alpha(), pygame.image.load('Dino/Images/SmallCactus2.png').convert_alpha(), pygame.image.load('Dino/Images/SmallCactus3.png').convert_alpha()]

bird = [pygame.image.load('Dino/Images/Bird1.png').convert_alpha(), pygame.image.load('Dino/Images/Bird2.png').convert_alpha()]

cloud = pygame.image.load('Dino/Images/Cloud.png').convert_alpha()

bg = pygame.image.load('Dino/Images/Track.png').convert_alpha()

class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_bend = 340
    jump_count = 10 #8.5
    jump_velo = jump_count

    def __init__(self):
        self.bend_img = bending
        self.run_img = running
        self.jump_img = jumping

        self.dino_bend = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_count = self.jump_velo
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, keys):
        if self.dino_bend:
            self.bend()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
        
        if keys[pygame.K_UP] and not self.dino_bend:
            self.dino_bend = False
            self.dino_run = False
            self.dino_jump = True
        elif keys[pygame.K_DOWN] and not self.dino_jump:
            self.dino_bend = True
            self.dino_run = False
            self.dino_jump = False
        elif not (keys[pygame.K_DOWN] or self.dino_jump):
            self.dino_bend = False
            self.dino_run = True
            self.dino_jump = False

    def bend(self):
        self.image = self.bend_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_bend
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    # def jump(self):
    #     self.image = self.jump_img
    #     if self.dino_jump:
    #         self.dino_rect.y -= self.jump_count * 4
    #         self.jump_count -= 0.8
    #         if self.jump_count < -self.jump_velo:
    #             self.dino_jump = False
    #             self.jump_count = self.jump_velo

    def jump(self):
        self.image = self.jump_img
        if not self.dino_jump:
            if self.keys[pygame.K_UP]:
                self.dino_jump = True
                # self.jump_count = self.jump_velo
        else:
            # The condition self.jump_count >= -self.jump_velo checks if the jump is still ongoing. self.jump_count starts with the initial jump velocity (self.jump_velo) and gradually decreases until it reaches the negative of the initial velocity.
            if self.jump_count > -self.jump_velo:
                # If self.jump_count is positive, the dinosaur moves up; if it is negative, the dinosaur moves down.
                if self.jump_count > 0:
                    # The line self.dino_rect.y -= (self.jump_count ** 2) / 2 updates the vertical position of the dinosaur. It subtracts (self.jump_count ** 2) / 2 from the current y position when the dinosaur is moving up
                    self.dino_rect.y -= (self.jump_count ** 2) / 2
                else:
                    # and adds it when the dinosaur is moving down. The (self.jump_count ** 2) / 2 expression ensures a smooth and realistic arc-like motion during the jump.
                    self.dino_rect.y += (self.jump_count ** 2) / 2
                # the self.jump_count as a countdown timer for the dinosaur's jump. It starts with a positive value that represents how long the jump should last. As the game loop runs, we subtract 1 from the countdown timer each time.
                self.jump_count -= 1
                # When the countdown timer reaches zero or goes below zero, it means the jump is finished, and the dinosaur starts to fall back down.
                # by decreasing the countdown timer by 1 each time, we simulate the passing of time during the jump and control the duration and smoothness of the dinosaur's movement.
            else:
                # Once self.jump_count reaches a value less than -self.jump_velo, it means the jump is complete, and the dinosaur has landed. In this case, the self.dino_jump flag is set to False to indicate that the dinosaur is no longer jumping. Additionally, the self.jump_count is reset to the initial jump velocity (self.jump_velo) to prepare for the next jump.
                self.dino_jump = False
                self.jump_count = self.jump_velo

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
class Cloud:
    def __init__(self):
        # The self.x position is randomly generated within a range that starts from screen_width and adds a random value 
        self.x = screen_width + random.randint(500, 700)
        # This ensures that the cloud starts off-screen to the right side. The self.y position is set to a random value between 50 and 100, determining the vertical position of the cloud.
        self.y = random.randint(50, 100)
        self.image = cloud
        self.width = self.image.get_width() # these attributes are essential for proper positioning, visibility, and rendering of the cloud object in the game.
     
    def update(self):
        self.x -= game_speed # This moves the cloud towards the left side of the screen. The game_speed is a variable controlling the speed of the game.
        if self.x < -self.width: # width value is crucial when checking if the cloud has moved completely off the left side of the screen (if self.x < -self.width). Without it, the condition would not accurately detect when the cloud is fully off-screen, leading to incorrect repositioning of the cloud.
            self.x = screen_width + random.randint(2000, 2500)
            # This ensures that the cloud will reappear off-screen to the right side after a random distance. 
            self.y = random.randint(50, 100)
     
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect() 
        # The rect attribute represents the rectangle that surrounds the small cactus image. It is initialized using the chosen image based on the type attribute. This rectangle helps with collision detection and positioning of the small cactus on the game screen.
        self.rect.x = screen_width #The rect_x attribute is set to the screen width, which determines the initial x-position of the cactus off the right edge of the screen.

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCacti(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        # calls the __init__ method of the parent class (Obstacle) and passes the image parameter and the type attribute as arguments. This initializes the small cactus object using the base Obstacle class.
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCacti(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Ptero(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0 # The self.index attribute is set to 0. It keeps track of the current image of the Pterodactyl animation.

    def draw(self, screen):
        # the Pterodactyl animation consists of 10 frames or images. The self.index variable is incremented in the draw method, and it ranges from 0 to 9, representing the 10 frames of the animation.
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        # By dividing self.index by 5 (self.index // 5), we get the following results for each range of self.index values:
        # self.index values 0 to 4: The result of self.index // 5 is 0, indicating that the first image (self.image[0]) should be displayed.
        # self.index values 5 to 9: The result of self.index // 5 is 1, indicating that the second image (self.image[1]) should be displayed.
        self.index += 1
        # After displaying the current image, the self.index is incremented by 1. This moves the animation to the next frame, ensuring that the Pterodactyl appears to be in motion.


def main():
    global game_speed, x_pos_bg, y_pos_bg, score, obstacles, level
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 15
    obstacles = []
    x_pos_bg = 0
    y_pos_bg = 380
    score = 0
    level = 1
    font = pygame.font.Font('Dino/Roboto/Roboto-Black.ttf', 20)
    death_count = 0

    def scores():
        global score, game_speed, level, highest_score
        score += 1
        if score % 100 == 0:
            game_speed += 1
            if score % 500 == 0:
                level += 1
        
        levels = font.render("Level: " + str(level), True, (0, 0, 0))
        levels_rect = levels.get_rect()
        levels_rect.center =  (100, 40)
        screen.blit(levels, levels_rect)
        high_score = font.render("High Score: " + str(highest_score), True, (0, 0, 0))
        high_score_rect = high_score.get_rect()
        high_score_rect.center = (550, 40)
        screen.blit(high_score, high_score_rect)
        text = font.render("Points: " + str(score), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        screen.blit(text, text_rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = bg.get_width()
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def save_data(score, level):
        try:
            conn = psycopg2.connect(
                host="rogue.db.elephantsql.com",
                port=5432,
                database="wocsykfv",
                user="wocsykfv",
                password="rwPJlc2S6ceN1uDanxX3cS9f2w9NCDJQ"
            )
            cur = conn.cursor()
            query = f"""
                INSERT INTO game_results (game_title, points, level)
                VALUES ('Jumping Dino', {int(score)}, {int(level)})"""
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(f'Error: {e}')
        finally:
            cur.close()
            conn.close()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255, 255, 255))
        keys = pygame.key.get_pressed()

        player.draw(screen)
        player.update(keys)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCacti(small_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCacti(large_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Ptero(bird))
        
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                save_data(score, level)
                menu(death_count)

        background()

        cloud.draw(screen)
        cloud.update()

        scores()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global score, level, highest_score
    run = True
    lose = None
    while run:
        screen.fill('White')
        font = pygame.font.Font('Dino/Roboto/Roboto-Black.ttf', 30)
        if death_count == 0:
            text = font.render("Press any Key to Start", True, ('Black'))
        elif death_count > 0:
            lose = font.render("GAME OVER", True, ('Black'))
            text = font.render("Press any Key to Restart", True, ('Black'))
            points = font.render("Points: " + str(score), True, ('Black'))
            points_rect = points.get_rect()
            points_rect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(points, points_rect)
            levels = font.render("Level: " + str(level), True, ('Black'))
            levels_rect = levels.get_rect()
            levels_rect.center =  (screen_width // 2, screen_height // 2 + 100)
            screen.blit(levels, levels_rect)
            if score > highest_score:
                highest_score = score
        if lose is not None:
            lose_rect = lose.get_rect()
            lose_rect.center = (screen_width  // 2, screen_height // 2 - 200)
            screen.blit(lose, lose_rect)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, text_rect)
        screen.blit(dino, (screen_width // 2 - 40, screen_height // 2 - 140))
        pygame.display.update()
        # option to quit the game safely, restart or exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main() # runs main() as soon as any key is pressed


menu(death_count=0)
