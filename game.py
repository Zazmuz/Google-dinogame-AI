from help_functions import *

WIDTH = 640
HEIGHT = 480
WHITE = (255, 255, 255)
GREEN = (50, 200, 50, 50)
RED = (200, 0, 0)

PLAYERS = 100

floor_y = HEIGHT - 40

player_radius = 30
player_x = 100
player_y = [0] * PLAYERS
player_y_speed = [0] * PLAYERS
player_alive = [True] * PLAYERS
player_fitness = [0] * PLAYERS

obstacle_x = []
obstacle_radius = []
obstacle_y = []


for i in range(1, 4):
    obstacle_x.append(WIDTH * i + randint(-25, 25))
    if randint(1,5) == 5:
        obstacle_radius.append(70)
    else:
        obstacle_radius.append(40)

for g in obstacle_radius:
    obstacle_y.append(floor_y - g)
try:
    with open('current_weights.pickle', 'rb') as pkl_file:
        weights = pickle.load(pkl_file)
except:
    weights = [[(np.random.rand(4, 5) - 0.5) * 0.1, (np.random.rand(5, 1) - 0.5) * 0.1] for x in range(PLAYERS)]

pg.init()
my_font = pg.font.Font(pg.font.get_default_font(), 30)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

running = True
render = True
fast_render = False
while running:
    if render == True:
        if fast_render == True:
            clock.tick(20000)
        else:
            clock.tick(60)  # 60 fps
    else:
        clock.tick(20000)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            with open("current_weights.pickle", "wb") as pkl_file:
                pickle.dump(weights, pkl_file)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player_alive = [False] * 100
            if event.key == pg.K_0:
                render = False
            if event.key == pg.K_9:
                render = True
            if event.key == pg.K_2:
                fast_render = False
            if event.key == pg.K_1:
                fast_render = True

    # Update
    for o in range(3):
        obstacle_x[o] -= 10
        if obstacle_x[o] < -100:
            obstacle_x[o] = WIDTH * 3 #+ randint(-25, 25)
            obstacle_radius[o] = randint(40, 70)
            obstacle_y[o] = floor_y - obstacle_radius[o]
            if randint(1, 4) == 2:
                obstacle_y[o] = floor_y - 70 - obstacle_radius[o]

    if not any(player_alive):
        # Create a new generation if all players are dead
        weights = new_generation(weights, player_fitness)
        player_y = [0] * PLAYERS
        player_y_speed = [0] * PLAYERS
        player_alive = [True] * PLAYERS
        player_fitness = [0] * PLAYERS
        print("New generation")

    for p in range(PLAYERS):
        player_y_speed[p] += 1
        player_y[p] += player_y_speed[p]

        if player_y[p] > floor_y - player_radius:
            player_y[p] = floor_y - player_radius
#            player_y_speed[p] = 100

        closest_obstacle = 0
        for r in range(len(obstacle_radius)):
            if obstacle_x[r] < obstacle_x[closest_obstacle]:
                closest_obstacle = r
        closest_radius = obstacle_radius[closest_obstacle]


        if think(weights[p], np.array([10, min(obstacle_x), closest_radius, obstacle_y[closest_obstacle]])) and player_y[
            p] == floor_y - player_radius:
            player_y_speed[p] = -20

        if player_alive[p]:
            player_fitness[p] += 1

        if circle_collision(player_x, player_y[p], player_radius, min(obstacle_x), obstacle_y[closest_obstacle],
                            closest_radius):
            player_alive[p] = False

    # Draw
    if render:
        screen.fill((0, 0, 0))
        pg.draw.rect(screen, WHITE, (0, floor_y, WIDTH, 2))

        score_text = my_font.render('Score: ' + str(max(player_fitness)), True, (50, 0, 0))
        screen.blit(score_text, (0, 0))

        for o in range(3):
            draw_circle(screen, obstacle_x[o], obstacle_y[o], obstacle_radius[o], RED)

        for p in range(PLAYERS):
            if player_alive[p]:
                draw_circle(screen, player_x, player_y[p], player_radius, GREEN)

        pg.display.flip()

