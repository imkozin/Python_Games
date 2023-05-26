import pygame
import random
import copy

pygame.init()

i_max = 11
j_max = 21

# screen size
screen_x = 300
scrren_y = 600

screen = pygame.display.set_mode((screen_x, scrren_y))
clock = pygame.time.Clock()
pygame.display.set_caption('Tetris')

# height and width each slot
dx = screen_x/(i_max - 1)
dy = scrren_y/(j_max - 1)

# frequency of renewal
fps = 60
grid = []

# set parameters
for i in range(0, i_max):
    grid.append([])
    for j in range(0, j_max):
        grid[i].append([1])


for i in range(0, i_max):
    for j in range(0, j_max):
        grid[i][j].append(pygame.Rect(i*dx, j*dx, dx, dy))
        grid[i][j].append(pygame.Color('Gray'))

details = [
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    [[1, 0], [1, 1], [0, 0], [-1, 0]],
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

det = [[], [], [], [], [], [], []]
for i in range(0, len(details)):
    for j in range(0, 4):
        det[i].append(pygame.Rect(details[i][j][0]*dx + dx*(i_max//2), details[i][j][1]*dy, dx, dy))

detail = pygame.Rect(0, 0, dx, dy)
det_choice = copy.deepcopy(random.choice(det))

count = 0
game = True
rotate = False
while game:
    delta_x = 0
    delta_y = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_x = -1
            elif event.key == pygame.K_RIGHT:
                delta_x = 1
            elif event.key == pygame.K_UP:
                rotate = True

    key = pygame.key.get_pressed()

    if key[pygame.K_DOWN]:
        count = 31 * fps

    screen.fill(pygame.Color('Black'))
    
    for i in range(0, i_max):
        for j in range(0, j_max):
            pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1], grid[i][j][0])
    
    #borders
    for i in range(4):
        if ((det_choice[i].x + delta_x*dx < 0) or (det_choice[i].x + delta_x*dx >= screen_x)):
            delta_x = 0
        if ((det_choice[i].y + dy >= scrren_y) or (grid[int(det_choice[i].x//dx)][int(det_choice[i].y//dy) + 1][0] == 0)):
            delta_y = 0
            for i in range(4):
                x = int(det_choice[i].x // dx)
                y = int(det_choice[i].y // dy)
                grid[x][y][0] = 0 # paint square
                grid[x][y][2] = pygame.Color('White')
            detail.x = 0
            detail.y = 0
            det_choice = copy.deepcopy(random.choice(det))
    # x movement
    for i in range(4):
        det_choice[i].x += delta_x*dx
    
    count += fps
    # y movement
    if count > 30*fps:
        for i in range(4):
            det_choice[i].y += delta_y*dy
        count = 0

    for i in range(4):
        detail.x = det_choice[i].x
        detail.y = det_choice[i].y
        pygame.draw.rect(screen, pygame.Color('White'), detail)

    c = det_choice[2] #Center of element
    if rotate == True:
        for i in range(4):
            x = det_choice[i].y - c.y
            y = det_choice[i].x - c.x

            det_choice[i].x = c.x - x
            det_choice[i].y = c.y + y
        rotate = False

    for j in range(j_max - 1, -1, -1):
        count_cells = 0
        for i in range(0, i_max):
            if grid[i][j][0] == 0:
                count_cells += 1
            elif grid[i][j][0] == 1:
                break
        if count_cells == (i_max - 1):
            for l in range(0, i_max):
                grid[l][0][0] = 1
            for k in range(j, -1, -1):
                for l in range(0, i_max):
                    grid[l][k][0] = grid[l][k-1][0]

    pygame.display.flip()
    clock.tick(fps)
    