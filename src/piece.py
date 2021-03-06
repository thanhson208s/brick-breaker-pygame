import config, constants, utility
import pygame, math

class Piece:
    RECTANGLE = 0
    TRIANGLE = 1
    CIRCLE = 2

    def __init__(self, hp=1):
        self.hp = hp
        self.point = (2 ** (hp - 1)) * config.POINT_PER_HP
        self.font = pygame.font.SysFont('monospace', 14)

    def isCollided(self, ball):
        #if collied, change ball velocity and return True
        #else return False
        pass

class RectanglePiece(Piece):
    def __init__(self, rect, hp=1):
        super().__init__(hp)
        self.type = Piece.RECTANGLE
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.box = rect

    def isCollided(self, ball):
        isCollided = False
        if ball.p.x >= self.x + self.w:
            if ball.p.y > self.y and ball.p.y < self.y + self.h:
                if ball.p.x <= self.x + self.w + ball.radius:
                    isCollided = True
                    collisionVector = pygame.math.Vector2(1, 0)
            else:
                vert = pygame.math.Vector2(self.x + self.w, self.y if ball.p.y <= self.y else (self.y + self.h))
                if (ball.p - vert).magnitude() <= ball.radius:
                    isCollided = True
                    collisionVector = ball.p - vert
        elif ball.p.x <= self.x:
            if ball.p.y > self.y and ball.p.y < self.y + self.h:
                if ball.p.x >= self.x - ball.radius:
                    isCollided = True
                    collisionVector = pygame.math.Vector2(-1, 0)
            else:
                vert = pygame.math.Vector2(self.x, self.y if ball.p.y <= self.y else (self.y + self.h))
                if (ball.p - vert).magnitude() <= ball.radius:
                    isCollided = True
                    collisionVector = ball.p - vert
        else:
            if ball.p.y < self.y and ball.p.y >= self.y - ball.radius:
                isCollided = True
                collisionVector = pygame.math.Vector2(0, -1)
            elif ball.p.y > self.y + self.h and ball.p.y <= self.y + self.h + ball.radius:
                isCollided = True
                collisionVector = pygame.math.Vector2(0, 1)

        if isCollided:
            ball.v -= (2 * ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            return True
        else: 
            return False

    def draw(self, screen):
        label_hp = self.font.render(str(self.hp), False, constants.WHITE)
        pygame.draw.rect(screen, constants.WHITE, self.box, 2)
        screen.blit(label_hp, (self.x + self.w/2 - label_hp.get_width()/2, self.y + self.h/2 - label_hp.get_height()/2))

class TrianglePiece(Piece):
    def __init__(self, vertices, hp=1):
        super().__init__(hp)
        self.type = Piece.TRIANGLE
        self.vertices = [pygame.math.Vector2(v) for v in vertices]
        
        minX = min([v[0] for v in vertices])
        minY = min([v[1] for v in vertices])
        self.box = (minX, minY, max([v[0] for v in vertices]) - minX, max([v[1] for v in vertices]) - minY)

    def isCollided(self, ball):
        return False

    def draw(self, screen):
        label_hp = self.font.render(str(self.hp), False, constants.WHITE)
        pygame.draw.polygon(screen, constants.WHITE, self.vertices, 2)
        screen.blit(label_hp, sum(self.vertices, pygame.math.Vector2(0, 0)) / 3)

class CirclePiece(Piece):
    def __init__(self, center, radius, hp):
        super().__init__(hp)
        self.type = Piece.CIRCLE
        self.center = pygame.math.Vector2(center)
        self.radius = radius
        self.box = (self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2)

    def isCollided(self, ball):
        if (self.center - ball.p).magnitude() <= self.radius + ball.radius:
            collisionVector = ball.p - self.center
            ball.v -= (2 * ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            return True
        return False

    def draw(self, screen):
        label_hp = self.font.render(str(self.hp), False, constants.WHITE)
        pygame.draw.circle(screen, constants.WHITE, self.center, self.radius, 2)
        screen.blit(label_hp, (self.center.x - label_hp.get_width()/2, self.center.y - label_hp.get_height()/2))