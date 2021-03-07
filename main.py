import sys, pygame, math, subprocess, time

sys.path.insert(1, 'src/')
import constants, config
from gamedata import *
from ball import *
from bar import *
from piece import *
from sound import *

pygame.init()

# === GLOBAL OBJECTS === #
clock = pygame.time.Clock()
gameManager = GameManager()
soundManager = SoundManager.instance()

screen = pygame.display.set_mode(config.SIZE)
fps_font = pygame.font.SysFont("monospace", 12)
button_font = pygame.font.SysFont("monospace", 20, True)
title_font = pygame.font.SysFont('baby blocks', 48)
background = pygame.transform.scale(pygame.image.load('res/bg.jpg'), config.SIZE)
# === GLOBAL OBJECTS === #

# === Init all global data === #
running = True
curScene = constants.MENU_SCENE
timer = 0
# === Init all global data === #

def showFps():
    fps = clock.get_fps()
    label_fps = fps_font.render("fps: " + "%.2f"%fps, False, constants.WHITE)
    screen.blit(label_fps, (10, config.HEIGHT - 20))

def switchScene(scene):
    global curScene, timer
    curScene = scene
    soundManager.playSceneTransitionEffect()

    if curScene == constants.GAME_SCENE:
        timer = 0

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
                    switchScene(constants.GAME_SCENE)
                    gameManager.initGame()
                elif mouse[1] >= config.BTN_CONTROL_Y - config.BTN_SIZE_LARGE[1]/2 and mouse[1] <= config.BTN_CONTROL_Y + config.BTN_SIZE_LARGE[1]/2:
                    switchScene(constants.CONTROL_SCENE)
                elif mouse[1] >= config.BTN_QUIT_Y - config.BTN_SIZE_LARGE[1]/2 and mouse[1] <= config.BTN_QUIT_Y + config.BTN_SIZE_LARGE[1]/2:
                    running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                switchScene(constants.GAME_SCENE)
                gameManager.initGame()
            elif event.key == pygame.K_TAB:
                switchScene(constants.CONTROL_SCENE)
            elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                switchScene(constants.GAME_SCENE)
                gameManager.initGame(event.key - pygame.K_0)
            elif event.key == pygame.K_a:
                config.ENABLE_AUTO = not config.ENABLE_AUTO
                mess = "Toggle auto: " + str(config.ENABLE_AUTO)
                subprocess.call("osascript -e '{}'".format("display dialog \"" + mess + "\" with title \"Message\" buttons {\"OK\"}"), shell=True)
            elif event.key == pygame.K_m:
                config.ENABLE_MUSIC = not config.ENABLE_MUSIC
                soundManager.onToggleMusic()
            elif event.key == pygame.K_c:
                config.ENABLE_CHEAT = not config.ENABLE_CHEAT
                mess = "Toggle cheat: " + str(config.ENABLE_CHEAT)
                subprocess.call("osascript -e '{}'".format("display dialog \"" + mess + "\" with title \"Message\" buttons {\"OK\"}"), shell=True)
            elif event.key == pygame.K_s:
                config.ENABLE_SFX = not config.ENABLE_SFX
                mess = "Toggle sfx: " + str(config.ENABLE_SFX)
                subprocess.call("osascript -e '{}'".format("display dialog \"" + mess + "\" with title \"Message\" buttons {\"OK\"}"), shell=True)
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
    drawMenuButton("CONTROL", (config.WIDTH/2, config.BTN_CONTROL_Y))
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

def drawTime(remainTime):
    s = math.ceil(remainTime / 1000)
    m = math.floor(s / 60)
    s = s - m * 60
    label_time = fps_font.render((("" if m >= 10 else "0") + str(m)) + ":" + (("" if s >= 10 else "0") + str(s)), False, constants.WHITE)
    screen.blit(label_time, (config.WIDTH/2 - label_time.get_width()/2, config.HEIGHT - 20))

def drawLife(remainLifes):
    for i in range(remainLifes):
        pygame.draw.circle(screen, constants.BALL_COLOR, (12 + 20 * i, config.HEIGHT - 12), 8)

def drawGameOver(point, state, isOutOfTime, isOutOfLife):
    label_game_over = title_font.render('GAME OVER', False, constants.WHITE)
    screen.blit(label_game_over, (config.WIDTH/2 - label_game_over.get_width()/2, config.TITLE_Y))
    
    label_point = button_font.render("Point: " + str(point), False, constants.WHITE)
    screen.blit(label_point, (config.WIDTH/2 - label_point.get_width()/2, config.HEIGHT/2 - label_point.get_height()/2))

    desc = ""
    if state == GameManager.WIN:
        desc = "You win!"
    else:
        desc = "You lose!"
        if isOutOfTime:
            desc += " Out of time."
        if isOutOfLife:
            desc += " Out of life."
    label_desc = button_font.render(desc, False, constants.WHITE)
    screen.blit(label_desc, (config.WIDTH/2 - label_desc.get_width()/2, config.HEIGHT * 1/4 - label_desc.get_height()/2))

    label_note = fps_font.render("Press ESC to exit to menu or SPACE to restart level!", False, constants.WHITE)
    screen.blit(label_note, (config.WIDTH/2 - label_note.get_width()/2, config.HEIGHT*3/4 - label_note.get_height()/2))

def processGameScene():
    global running, curScene, timer

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
                gameManager.onSpace()
            elif event.key == pygame.K_ESCAPE:
                gameManager.endGame()
                switchScene(constants.MENU_SCENE)
            elif event.key == pygame.K_TAB:
                gameManager.pauseGame()

    # 2. process data
    timer += clock.get_time()
    while timer >= config.FRAME_TIME:
        gameManager.update(config.FRAME_TIME)
        timer -= config.FRAME_TIME

    # 3. update GUI
    if gameManager.state in [GameManager.READY, GameManager.RUN, GameManager.PAUSE, GameManager.REVIVE]:
        drawBar(gameManager.bar)
        drawBall(gameManager.ball)
        drawPieces(gameManager.pieces)
        drawPoint(gameManager.point)
        drawTime(gameManager.remainTime)
        drawLife(gameManager.remainLifes)
    elif gameManager.state == GameManager.WIN or gameManager.state == GameManager.LOSE:
        drawBar(gameManager.bar)
        drawBall(gameManager.ball)
        drawGameOver(gameManager.point, gameManager.state, gameManager.isOutOfTime(), gameManager.isOutOfLife())
# === Game Scene === #

# === Control Scene === #
def processControlScene():
    global running, curScene

    # 1.hanle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #this loop is the last
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_ESCAPE, pygame.K_TAB]:
                switchScene(constants.MENU_SCENE)
    # 2. process data
    # nothing to process

    # 3. update GUI
    # draw instruction
    label_title = title_font.render("CONTROLS", False, constants.WHITE)
    screen.blit(label_title, (config.WIDTH/2 - label_title.get_width()/2, config.TITLE_Y))

    label = button_font.render("SPACE  start game  ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 150))
    label = button_font.render("   ->  move left   ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 180))
    label = button_font.render("   <-  move right  ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 210))
    label = button_font.render("  ESC  exit game   ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 240))
    label = button_font.render("    M  toggle music", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 270))
    label = button_font.render("    A  toggle auto ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 300))
    label = button_font.render("    C  toggle cheat", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 330))
    label = button_font.render("    S  toggle sfx  ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 360))
    label = button_font.render("  TAB  pause game  ", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 390))
    label = button_font.render("  0-9  choose level", False, constants.WHITE)
    screen.blit(label, (config.WIDTH/2 - label.get_width()/2, config.TITLE_Y + 420))
# === Control Scene === #

# === main loop === #
print('Game has started!')
soundManager.playTheme()
while running:
    clock.tick(120)
    screen.fill(constants.BLACK)
    screen.blit(background, (0, 0))

    if (curScene == constants.MENU_SCENE):
        processMenuScene()
    elif (curScene == constants.GAME_SCENE):
        processGameScene()
    elif (curScene == constants.CONTROL_SCENE):
        processControlScene()

    # showFps()
    pygame.display.flip()

print('Game has stopped!')