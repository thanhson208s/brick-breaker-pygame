import config, constants
import pygame, math

class Ball: 
    def __init__(self, gameManager):
        self.v = None
        self.radius = None
        self.p = None
        self.gameManager = gameManager
        self.accelerationTimer = None

    def initGame(self):
        self.radius = config.BALL_RADIUS
        self.p = pygame.math.Vector2(config.WIDTH/2, config.BAR_Y - self.radius)
        self.v = pygame.math.Vector2(0, -config.BALL_BASE_SPEED)
        self.accelerationTimer = 0

    def reviveGame(self):
        self.radius = config.BALL_RADIUS
        self.p = pygame.math.Vector2(config.WIDTH/2, config.BAR_Y - self.radius)
        self.v = pygame.math.Vector2(0, -self.v.magnitude())

    def updateInitPosition(self, bar):
        self.p.x = bar.p.x

    def update(self, dt):
        self.accelerationTimer += dt / 1000
        if self.accelerationTimer >= config.BALL_ACCELERATION_PERIOD:
            self.accelerationTimer -= config.BALL_ACCELERATION_PERIOD
            speed = min(self.v.magnitude() + config.BALL_ACCELERATION_VALUE, config.BALL_MAX_SPEED)
            self.v = self.v.normalize() * speed
        self.p += self.v * dt / 1000