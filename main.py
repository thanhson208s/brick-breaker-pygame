import sys, pygame, math

sys.path.insert(1, 'src/')
import constants, config, utility
from gamedata import *
from ball import *
from bar import *
from piece import *

pygame.init()

# === GLOBAL OBJECTS === #
clock = pygame.time.Clock()
gameManager = GameManager()

screen = pygame.display.set_mode(config.SIZE)
fps_font = pygame.font.SysFont("monospace", 12)
button_font = pygame.font.SysFont("monospace", 20, True)
title_font = pygame.font.SysFont('baby blocks', 48)
background = pygame.transform.scale(pygame.image.load('res/bg.jpg'), config.SIZE) 
# === GLOBAL OBJECTS === #

# === Init all global data === #
running = True
curScene = constants.MENU_SCENE
# === Init all global data === #

def showFps():
    fps = clock.get_fps()
    label_fps = fps_font.render("fps: " + "%.2f"%fps, False, constants.WHITE)
    screen.blit(label_fps, (10, config.HEIGHT - 20))

# === Menu Scene === #
def drawMenuButton(text, p):
    btn_color = constants.GRAY
    #check if mouse in button
    mouse = pygame.mouse.get_pos()
    rect = (p[0] - config.BTN_SIZE_LARGE[0]/2, p[1] - config.BTN_SIZE_LARGE[1]/2, config.BTN_SIZE_LARGE[0], config.BTN_SIZE_LARGE[1])
    if mouse[0] >= rect[0] and mouse[0] <= rect[0] + rect[2] \
        and mouse[1] >= rect[1] and mouse[1] <= rect[1] + rect[3]:
        btn_color = constants.WHITE
    
    pygame.draw.rect(screen, btn_color, rect, 5)
    text = button_font.render(text, False, btn_color)
    screen.blit(text, (p[0] - text.get_width()/2, p[1] - text.get_height()/2))

def processMenuScene():
    global running, curScene

    # 1.hanle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #this loop is the last
        elif event.type == pygame.MOUSEBUTTONUP:
            #check which btn is pressed
            mouse = pygame.mouse.get_pos()
            if mouse[0] >= config.WIDTH/2 - config.BTN_SIZE_LARGE[0]/2 and mouse[0] <= config.WIDTH/2 + config.BTN_SIZE_LARGE[0]/2:
                if mouse[1] >= config.BTN_START_Y - config.BTN_SIZE_LARGE[1]/2 and mouse[1] <= config.BTN_START_Y + config.BTN_SIZE_LARGE[1]/2:
                    print('Button start pressed')
                    curScene = constants.GAME_SCENE
                    gameManager.initGame()
                elif mouse[1] >= config.BTN_RANK_Y - config.BTN_SIZE_LARGE[1]/2 and mouse[1] <= config.BTN_RANK_Y + config.BTN_SIZE_LARGE[1]/2:
                    print('Button rank pressed')
                elif mouse[1] >= config.BTN_QUIT_Y - config.BTN_SIZE_LARGE[1]/2 and mouse[1] <= config.BTN_QUIT_Y + config.BTN_SIZE_LARGE[1]/2:
                    print('Button quit pressed')
                    running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                curScene = constants.GAME_SCENE
                gameManager.initGame(event.key - pygame.K_0)
    # 2. process data
    # nothing to process

    # 3. update GUI
    # draw title
    label_title = title_font.render("BRICK BREAKER", False, constants.WHITE)
    screen.blit(label_title, (config.WIDTH/2 - label_title.get_width()/2, config.TITLE_Y))

    label_author = button_font.render("Created by " + config.AUTHOR + " with pygame.", False, constants.WHITE)
    screen.blit(label_author, (config.WIDTH/2 - label_author.get_width()/2, config.TITLE_Y + 120))

    label_version = button_font.render("Version " + config.VERSION, False, constants.WHITE)
    screen.blit(label_version, (config.WIDTH/2 - label_version.get_width()/2, config.TITLE_Y + 150))

    # draw menu
    drawMenuButton("START", (config.WIDTH/2, config.BTN_START_Y))
    drawMenuButton("RANK", (config.WIDTH/2, config.BTN_RANK_Y))
    drawMenuButton("QUIT", (config.WIDTH/2, config.BTN_QUIT_Y))
    
# === Menu Scene === #

# === Game Scene === #
def drawBar(bar):
    start_pos = (bar.p.x - bar.length/2, bar.p.y)
    end_pos = (bar.p.x + bar.length/2, bar.p.y)
    pygame.draw.line(screen, constants.WHITE, start_pos, end_pos, 5)

def drawBall(ball):
    pygame.draw.circle(screen, constants.BALL_COLOR, ball.p, ball.radius)

def drawPieces(pieces):
    for piece in pieces:
        piece.draw(screen)

def drawPoint(point):
    label_point = fps_font.render("Point: " + str(point), False, constants.WHITE)
    screen.blit(label_point, (config.WIDTH - 10 - label_point.get_width(), config.HEIGHT - 20))

def drawGameOver(point):
    label_game_over = title_font.render('GAME OVER', False, constants.WHITE)
    screen.blit(label_game_over, (config.WIDTH/2 - label_game_over.get_width()/2, config.TITLE_Y))
    
    label_point = button_font.render("Point: " + str(point), False, constants.WHITE)
    screen.blit(label_point, (config.WIDTH/2 - label_point.get_width()/2, config.HEIGHT/2 - label_point.get_height()/2))

    label_note = fps_font.render("Press ESC to exit to menu or SPACE to restart level!", False, constants.WHITE)
    screen.blit(label_note, (config.WIDTH/2 - label_note.get_width()/2, config.HEIGHT*3/4 - label_note.get_height()/2))


def processGameScene():
    global running, curScene

    # 1.hanle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #this loop is the last
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                gameManager.onControlStart(event.key)
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                gameManager.onControlEnd(event.key)
            elif event.key == pygame.K_SPACE:
                gameManager.startGame()
            elif event.key == pygame.K_ESCAPE:
                gameManager.endGame()
                curScene = constants.MENU_SCENE

    # 2. process data
    gameManager.update(clock.get_time())

    # 3. update GUI
    if gameManager.state in [GameManager.READY, GameManager.RUN]:
        drawBar(gameManager.bar)
        drawBall(gameManager.ball)
        drawPieces(gameManager.pieces)
        drawPoint(gameManager.point)
    elif gameManager.state == GameManager.WIN or gameManager.state == GameManager.LOSE:
        drawBar(gameManager.bar)
        drawBall(gameManager.ball)
        drawGameOver(gameManager.point)

# === Game Scene === #

# === main loop === #
print('Game has started!')
while running:
    clock.tick(60)
    screen.fill(constants.BLACK)
    screen.blit(background, (0, 0))

    if (curScene == constants.MENU_SCENE):
        processMenuScene()
    if (curScene == constants.GAME_SCENE):
        processGameScene()
    
    showFps()
    pygame.display.flip()