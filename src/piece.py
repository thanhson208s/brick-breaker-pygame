import config, constants
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

    def quickCheckCollide(self, ball):
        if (ball.p.x < self.box[0] - ball.radius) \
            or (ball.p.x > self.box[0] + self.box[2] + ball.radius) \
            or (ball.p.y < self.box[1] - ball.radius) \
            or (ball.p.y > self.box[1] + self.box[3] + ball.radius):
            return False
        return True

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
        if not self.quickCheckCollide(ball):
            return False

        isCollided = False
        if ball.p.x >= self.x + self.w:
            if ball.p.y > self.y and ball.p.y < self.y + self.h:
                if ball.p.x <= self.x + self.w + ball.radius:
                    isCollided = True
                    collisionVector = pygame.math.Vector2(1, 0)
                    ball.p.x = self.x + self.w + ball.radius
            else:
                vert = pygame.math.Vector2(self.x + self.w, self.y if ball.p.y <= self.y else (self.y + self.h))
                if (ball.p - vert).magnitude() <= ball.radius:
                    isCollided = True
                    collisionVector = ball.p - vert
                    ball.p = vert + collisionVector.normalize() * ball.radius
        elif ball.p.x <= self.x:
            if ball.p.y > self.y and ball.p.y < self.y + self.h:
                if ball.p.x >= self.x - ball.radius:
                    isCollided = True
                    collisionVector = pygame.math.Vector2(-1, 0)
                    ball.p.x = self.x - ball.radius
            else:
                vert = pygame.math.Vector2(self.x, self.y if ball.p.y <= self.y else (self.y + self.h))
                if (ball.p - vert).magnitude() <= ball.radius:
                    isCollided = True
                    collisionVector = ball.p - vert
                    ball.p = vert + collisionVector.normalize() * ball.radius
        else:
            if ball.p.y < self.y and ball.p.y >= self.y - ball.radius:
                isCollided = True
                collisionVector = pygame.math.Vector2(0, -1)
                ball.p.y = self.y - ball.radius
            elif ball.p.y > self.y + self.h and ball.p.y <= self.y + self.h + ball.radius:
                isCollided = True
                collisionVector = pygame.math.Vector2(0, 1)
                ball.p.y = self.y + self.h + ball.radius

        if isCollided:
            temp = (ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            if temp.dot(collisionVector) < 0:
                ball.v -= 2 * temp
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
        if not self.quickCheckCollide(ball):
            return False
        
        isCollided = False
        for i in range(3):
            p0 = self.vertices[i]
            p1 = self.vertices[(i + 1) % 3]
            p2 = self.vertices[(i + 2) % 3]
            parVector = p0 - p1
            perVector = pygame.math.Vector2(-parVector.y, parVector.x)
            if perVector.dot(ball.p - p2) < 0:
                perVector = perVector * (-1)
            if (p0 - p2).dot(perVector) * (p0 - ball.p).dot(perVector) < 0:
                if (p1 - p0).dot(ball.p - p0) <= 0:
                    dist = (ball.p - p0).magnitude()
                    if dist <= ball.radius:
                        isCollided = True
                        collisionVector = ball.p - p0
                elif (p0 - p1).dot(ball.p - p1) <= 0:
                    dist = (ball.p - p1).magnitude()
                    if dist <= ball.radius:
                        isCollided = True
                        collisionVector = ball.p - p1
                else:
                    dist = (ball.p - p0).magnitude() * \
                        math.sin(math.acos((p1 - p0).dot(ball.p - p0)/((p1 - p0).magnitude() * (ball.p - p0).magnitude())))
                    if dist <= ball.radius:
                        isCollided = True
                        collisionVector = perVector
                break

        if isCollided:
            temp = (ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            if temp.dot(collisionVector) < 0:
                ball.v -= 2 * temp
            return True
        else: 
            return False

    def draw(self, screen):
        label_hp = self.font.render(str(self.hp), False, constants.WHITE)
        pygame.draw.polygon(screen, constants.WHITE, self.vertices, 2)
        screen.blit(label_hp, sum(self.vertices, pygame.math.Vector2(0, 0)) / 3 - pygame.math.Vector2(label_hp.get_size())/2)

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
            ball.p = self.center + collisionVector.normalize() * (self.radius + ball.radius)
            temp = (ball.v.dot(collisionVector) / collisionVector.magnitude_squared()) * collisionVector
            if temp.dot(collisionVector) < 0:
                ball.v -= 2 * temp
            return True
        return False

    def draw(self, screen):
        label_hp = self.font.render(str(self.hp), False, constants.WHITE)
        pygame.draw.circle(screen, constants.WHITE, self.center, self.radius, 2)
        screen.blit(label_hp, (self.center.x - label_hp.get_width()/2, self.center.y - label_hp.get_height()/2))