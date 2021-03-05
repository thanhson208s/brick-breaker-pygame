import config, constants, utility
import pygame, math

class Bar:
    def __init__(self):
        self.p = None
        self.v = None
        self.length = None
        self.speed = None
        self.controlBuffer = None

    def initGame(self):
        self.p = pygame.math.Vector2(config.WIDTH/2, config.BAR_Y)
        self.v = pygame.math.Vector2(0, 0)
        self.length = config.BAR_BASE_LENGTH
        self.speed = config.BAR_BASE_SPEED
        self.controlBuffer = []

    def onControlStart(self, key):
        self.controlBuffer.append(key)

    def onControlEnd(self, key):
        self.controlBuffer.remove(key)

    def checkCollide(self, ball):
        offset = (ball.p.y - self.p.y) / abs(ball.p.y - self.p.y) if ball.p.y != self.p.y else 0

        # find closet point
        p_left = pygame.math.Vector2(self.p.x - self.length/2, self.p.y)
        p_right = pygame.math.Vector2(self.p.x + self.length/2, self.p.y)
        if ball.p.x >= p_left.x and ball.p.x <= p_right.x:
            if abs(ball.p.y - self.p.y) <= ball.radius:
                rate = (self.p.x - ball.p.x) / (self.length / 2)
                angle = (math.pi/2 + math.pi/3 * rate) * offset
                ball.v = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * ball.v.magnitude()
                return True
            else:
                return False

        # check left point
        if (ball.p - p_left).magnitude() <= ball.radius:
            vec = ball.p - p_left
            angle = math.atan2(vec.y, vec.x)
            rate = (abs(angle) - math.pi/2) / (math.pi/2)
            angle = (math.pi * 5/6 + math.pi * 1/6 * rate) * offset
            ball.v = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * ball.v.magnitude()
            return True

        # check right point
        if (ball.p - p_right).magnitude() <= ball.radius:
            vec = ball.p - p_right
            angle = math.atan2(vec.y, vec.x)
            rate = (math.pi/2 - abs(angle)) / (math.pi/2)
            angle = (math.pi * 1/6 - math.pi * 1/6 * rate) * offset
            ball.v = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * ball.v.magnitude()
            return True

        return False


    def update(self, dt):
        if len(self.controlBuffer) > 0:
            if self.controlBuffer[0] == pygame.K_LEFT:
                self.v.x = -self.speed
            else:
                self.v.x = self.speed
        else:
            self.v.x = 0
            return
        
        self.p += self.v * (dt / 1000)
        if self.p.x - (self.length/2 + config.BALL_RADIUS/2) < 0:
            self.p.x = self.length/2 + config.BALL_RADIUS/2
        if self.p.x + (self.length/2 + config.BALL_RADIUS/2) > config.WIDTH:
            self.p.x = config.WIDTH - (self.length/2 + config.BALL_RADIUS/2)