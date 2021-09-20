import pygame, random

TOWER_SPEED = 5
SKY_COLOR = (25, 2, 52)

score = 0
highscore = 0

started = False
gameOver = False

towers = []
opPlanes = []

deathMessage = None

plane = pygame.transform.flip(pygame.image.load('plane.png'), True, False)
opPlane = pygame.image.load('planeBlue.png')

pygame.init()

font10 = pygame.font.SysFont('Comic Sans MS', 10, 10)
font15 = pygame.font.SysFont('Comic Sans MS', 15, 15)
font20 = pygame.font.SysFont('Comic Sans MS', 20, 20)
font30 = pygame.font.SysFont('Comic Sans MS', 30, 30)
font50 = pygame.font.SysFont('Comic Sans MS', 50, 50)
font200 = pygame.font.SysFont('Comic Sans MS', 200, 200)

def makeTowers():
    for i in range(10):
        towers.append(tower(1920+i*192))

class OpPlane():
    def __init__(self):
        self.y = random.randint(10,500)
        self.x = 1920
        self.planeSpeed = random.randint(2,5)
        self.v = -.5
        self.alive = True
        self.type = "plane"
        self.rot = 0
    def move(self):
        if self.alive == False:
            if self.rot < 90:
                self.rot += 1.5
            self.y -= self.v
            self.v *= 1.1
        self.x -= self.planeSpeed+TOWER_SPEED
        if self.x < 0:
            return "terminate"

class Bird():
    def __init__(self):
        self.set()
    def set(self):
        self.x = 960
        self.y = 540
        self.v = 0
        self.rot = 0
        self.alive = True
    def move(self):
        global gameOver, highscore, score, deathMessage
        if started == True:
            if self.rot > -90:
                self.rot -= 1.5
            self.y -= self.v
            if self.v < .5 and self.v > 0:
                self.v = -.5
            elif self.v > 0:
                self.v *= .9
            elif self.v < 0:
                self.v *= 1.1
            if self.y > 1080:
                gameOver = True
                if score > highscore:
                    highscore = score
                if self.alive == True:
                    deathMessage = "You died by crashing into the ground"
            elif self.y < 0:
                self.alive = False
                deathMessage = "You flew to close to the sun"
    def jump(self):
        self.rot = 45
        self.v = 10
        if self.y < 0:
            self.y = 0

class tower():
    def __init__(self, x):
        self.y = 0
        self.x = x
        self.windows = []
        self.type = "building"
        self.start()
    def start(self):
        self.y = random.randint(100,500)
        for i in range(self.y//30):
            for j in range(6):
                self.windows.append([j, i, random.randint(0,3)])
    def move(self):
        self.x -= TOWER_SPEED
        if self.x <= -100:
            self.x = 1920
            self.start()