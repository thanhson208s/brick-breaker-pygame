from ball import *
from bar import *
from piece import *
from sound import *
import constants, config
import pygame, math, json

class GameManager:
    WAIT = -1
    READY = 0
    RUN = 1
    WIN = 100
    LOSE = -100
    PAUSE = 2

    def __init__(self):
        self.state = GameManager.WAIT
        self.ball = Ball(self)
        self.bar = Bar(self)
        self.pieces = None
        self.point = None
        self.pointTimer = None
        self.remainTime = None

    def initGame(self, mapIndex=-1):
        self.state = GameManager.READY
        self.mapIndex = mapIndex
        self.bar.initGame()
        self.ball.initGame()
        self.initPieces()
        self.point = 0
        self.pointTimer = 0
        self.remainTime = config.TOTAL_TIME * 1000

    def initPieces(self):
        path = (config.MAP_FOLDER + str(self.mapIndex) + '.json') if self.mapIndex >= 0 else config.DEFAULT_MAP 
        try:
            json_file = open(path)
        except:
            json_file = open(config.DEFAULT_MAP)
        data = json.load(json_file)
        
        self.pieces = []
        for item in data:
            if item['type'] == Piece.RECTANGLE:
                self.pieces.append(RectanglePiece(item['rect'], item['hp']))
            elif item['type'] == Piece.TRIANGLE:
                self.pieces.append(TrianglePiece(item['vertices'], item['hp']))
            elif item['type'] == Piece.CIRCLE:
                self.pieces.append(CirclePiece(item['center'], item['radius'], item['hp']))

    def startGame(self):
        self.state = GameManager.RUN
        self.ball.startGame()
        SoundManager.instance().playCollideWithBarEffect()

    def pauseGame(self):
        if self.state == GameManager.RUN:
            self.state = GameManager.PAUSE
        elif self.state == GameManager.PAUSE:
            self.state = GameManager.RUN

    def endGame(self):
        self.state = GameManager.WAIT

    def onSpace(self):
        if (self.state == GameManager.READY):
            self.startGame()
        elif self.state in [GameManager.WIN, GameManager.LOSE]:
            self.initGame(self.mapIndex)
        

    def onControlStart(self, key):
        if (self.state == GameManager.WAIT):
            return
        if (self.state == GameManager.RUN and config.ENABLE_AUTO):
            return
        self.bar.onControlStart(key)
    
    def onControlEnd(self, key):
        if (self.state == GameManager.WAIT):
            return
        if (self.state == GameManager.RUN and config.ENABLE_AUTO):
            return
        self.bar.onControlEnd(key)

    def checkCollideWithBorder(self):
        # check collide with top
        isCollided = False
        if self.ball.p.y - self.ball.radius <= 0:
            isCollided = True
            self.ball.p.y = self.ball.radius
            collisionVector = pygame.math.Vector2(0, 1)
            self.ball.v -= (2 * self.ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
        if self.ball.p.x - self.ball.radius <= 0:
            isCollided = True
            self.ball.p.x = self.ball.radius
            collisionVector = pygame.math.Vector2(1, 0)
            self.ball.v -= (2 * self.ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
        if self.ball.p.x + self.ball.radius >= config.WIDTH:
            isCollided = True
            self.ball.p.x = config.WIDTH - self.ball.radius
            collisionVector = pygame.math.Vector2(-1, 0)
            self.ball.v -= (2 * self.ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector

        if self.ball.p.y + self.ball.radius >= config.HEIGHT and (config.ENABLE_CHEAT or self.state == GameManager.WIN):
            isCollided = True
            self.ball.p.y = config.HEIGHT - self.ball.radius
            collisionVector = pygame.math.Vector2(0, -1)
            self.ball.v -= (2 * self.ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector

        return isCollided

    def update(self, dt):
        if self.state in [GameManager.WAIT, GameManager.PAUSE]:
            return

        self.bar.update(dt)
        if self.state == GameManager.READY:
            self.ball.updateInitPosition(self.bar)
        elif self.state == GameManager.RUN:
            self.pointTimer += dt / 1000
            if self.pointTimer >= config.POINT_DECREASE_PERIOD:
                self.pointTimer -= config.POINT_DECREASE_PERIOD
                self.point = max(self.point - config.POINT_DECREASE_VALUE, 0)
            
            self.ball.update(dt)
            # check collied with border
            if not self.checkCollideWithBorder():
                # check collide with bar
                if not self.bar.checkCollide(self.ball):
                    # check collide with pieces
                    for piece in self.pieces:
                        if piece.isCollided(self.ball):
                            SoundManager.instance().playCollideWithPieceEffect()
                            piece.hp -= 1
                            if piece.hp <= 0:
                                self.point += piece.point
                                self.pieces.remove(piece)
                else:
                    SoundManager.instance().playCollideWithBarEffect()
            else:
                SoundManager.instance().playCollideWithBorderEffect()
            #check win - lose
            self.remainTime = max(0, self.remainTime - dt)
            if len(self.pieces) == 0:
                self.state = GameManager.WIN
                SoundManager.instance().playWinEffect()
            else:
                if self.ball.p.y - self.ball.radius > config.HEIGHT or self.remainTime <= 0:
                    self.state = GameManager.LOSE
                    SoundManager.instance().playLoseEffect()
        elif self.state == GameManager.WIN:
            self.ball.update(dt)
            if not self.checkCollideWithBorder():
                self.bar.checkCollide(self.ball)
        elif self.state == GameManager.LOSE:
            self.ball.update(dt)
            if not self.checkCollideWithBorder():
                self.bar.checkCollide(self.ball)

    def isRunning(self):
        return self.state == GameManager.RUN     