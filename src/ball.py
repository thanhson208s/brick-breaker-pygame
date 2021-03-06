import config, constants, utility
import pygame, math

class Ball: 
    def __init__(self, gameManager):
        self.v = None
        self.radius = None
        self.p = None
        self.gameManager = gameManager

    def initGame(self):
        self.radius = config.BALL_RADIUS
        self.p = pygame.math.Vector2(config.WIDTH/2, config.BAR_Y - self.radius)
        self.v = pygame.math.Vector2(0, 0)

    def updateInitPosition(self, bar):
        self.p.x = bar.p.x

    def startGame(self):
        self.v.y = -config.BALL_BASE_SPEED

    def update(self, dt):
        self.p += self.v * dt / 1000
        