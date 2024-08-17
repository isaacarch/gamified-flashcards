import pygame
from pygame.locals import *
print("a")
resolution = (400,300)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (25,227,36)
levels = 1
screen = pygame.display.set_mode(resolution)


class Wall:
    def __init__(self, xPos, YPos, Width, Height) -> None:
        self.x = xPos
        self.y = YPos
        self.width = Width
        self.height = Height
    def draw(self, surface):
        pygame.draw.rect(surface, red, pygame.Rect(self.x, self.y, self.width, self.height))
    def update(self):
        pass

class Ball: # can be used  for projectiles later 
    def __init__(self, xPos =  resolution[0] / 2, yPos = resolution[1] / 2, xVel = 1, yVel = 1, rad = 15):
        self.x = xPos
        self.y = yPos
        self.dx = xVel
        self.dy = yVel
        self.radius = rad
        self.type = "ball"

    def draw(self, surface):
        pygame.draw.circle(surface, black, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 0 or self.x >= resolution[0]):
            self.dx *= -1
        if (self.y <= 0 or self.y >= resolution[1]):
            self.dy *= -1

class Player: # a circle controlled by the player
    def __init__(self, rad = 15, xx = 0, yy = 0):
        self.x = xx
        self.y = yy
        self.radius = rad
        self.type = "player"

    def draw(self, surface):
        pygame.draw.circle(surface, green, (self.x, self.y), self.radius)

    def update(self):
        vel = 1.5
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.x -= vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.x += vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.y -= vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.y += vel
        if self.x <= 0: self.x = 0
        if self.x >= resolution[0]: self.x = resolution[0]
        if self.y <= 0: self.y = 0
        if self.y >= resolution[1]: self.y = resolution[1]
        if (400 - self.x)**2 + (300 - self.y)**2 <= (25 + self.radius)**2: 
            global levels
            levels += 0.5
            #pygame.quit()
        #cord = pygame.mouse.get_pos()
        #self.x = cord[0]
        #self.y = cord[1]

class game(): # main game loop
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.gameObjects = []
        self.gameObjects.append(Player(20, 100, 150))
        self.gameObjects.append(Ball())
        self.gameObjects.append(Ball(100))
    
    def newlevel(self, levels, objects):
        #screen.fill(white)
        self.gameObjects = []
        for gameObj in objects[int(levels*2 - 3)]:
            self.gameObjects.append(gameObj)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    def run(self):
        while True:
            self.handleEvents()
            currentlevel = 1
            for gameObj in self.gameObjects:
                gameObj.update()

            self.screen.fill(white)

            for gameObj in self.gameObjects:
                gameObj.draw(self.screen)

            global levels, objects
            if levels > currentlevel:
                currentlevel += 0.5
                self.newlevel(levels, objects)

            self.clock.tick(60)
            pygame.display.flip()


objects = [[Player(20, 100, 150),Wall(100, 75, 50, 200)],[Player(20, 100, 150),Ball(200)],[Player(20, 100, 150)],[]]
game().run()