from ball import *
from bar import *
from piece import *
import constants, config, utility
import pygame, math, json

class GameManager:
    WAIT = -1
    READY = 0
    RUN = 1
    WIN = 100
    LOSE = -100

    def __init__(self):
        self.state = GameManager.WAIT
        self.ball = Ball()
        self.bar = Bar()
        self.pieces = None
        self.point = None

    def initGame(self):
        self.state = GameManager.READY
        self.bar.initGame()
        self.ball.initGame()
        self.initPieces()
        self.point = 0

    def initPieces(self):
        json_file = open('/Users/lap14008/Programming/Game Programming/pygame/res/map.json')
        data = json.load(json_file)
        
        self.pieces = []
        for item in data:
            if item['type'] == Piece.RECTANGLE:
                self.pieces.append(RectanglePiece(item['rect'], item['hp']))
            elif item['type'] == Piece.TRIANGLE:
                pass
            elif item['type'] == Piece.CIRCLE:
                pass

    def startGame(self):
        if (self.state != GameManager.READY):
            return
        self.state = GameManager.RUN
        self.ball.startGame()

    def endGame(self):
        pass

    def onControlStart(self, key):
        if (self.state == GameManager.WAIT):
            return
        self.bar.onControlStart(key)
    
    def onControlEnd(self, key):
        if (self.state == GameManager.WAIT):
            return
        self.bar.onControlEnd(key)

    def checkCollideWithBorder(self):
        # check collide with top
        isCollided = False
        if self.ball.p.y - self.ball.radius <= 0:
            isCollided = True
            collisionVector = pygame.math.Vector2(0, 1)
        if self.ball.p.x - self.ball.radius <= 0:
            isCollided = True
            collisionVector = pygame.math.Vector2(1, 0)
        if self.ball.p.x + self.ball.radius >= config.WIDTH:
            isCollided = True
            collisionVector = pygame.math.Vector2(-1, 0)
            
        if self.ball.p.y + self.ball.radius >= config.HEIGHT and config.ENABLE_CHEAT:
            isCollided = True
            collisionVector = pygame.math.Vector2(0, -1)

        if isCollided:
            self.ball.v -= (2 * self.ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            return True
        else: 
            return False

    def update(self, dt):
        if (self.state == GameManager.WAIT):
            return

        self.bar.update(dt)
        if self.state == GameManager.READY:
            self.ball.updateInitPosition(self.bar)
        elif self.state == GameManager.RUN:
            self.ball.update(dt)
            # check collied with border
            if not self.checkCollideWithBorder():
                # check collide with bar
                if not self.bar.checkCollide(self.ball):
                    # check collide with pieces
                    for piece in self.pieces:
                        if piece.isCollided(self.ball):
                            piece.hp -= 1
                            if piece.hp <= 0:
                                self.point += piece.point
                                self.pieces.remove(piece)
                            break