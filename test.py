import pygame, random
from flashcard_database import uploadCard, downloadCards, updateScoreTime
from flashcard_algorithm import startDeck, getCard, deckEmpty, useCard
from pygame.locals import *
#print("a")
resolution = (400,300)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (25,227,36)
levels = 1
screen = pygame.display.set_mode(resolution)

# from flashcard_algorithm import startDeck, testCard, deckEmpty

# need to get cards with fixed game size

def testCard():
    card = getCard()
    front = str(card.getFront()).encode()
    back = str(card.getBack()).encode()
    # display card front 
    # user inputs text for what they think is on the back 
    # display card back 
    # user enters score 
    s = front
    print(s)
    end = pygame.time.get_ticks() + 1500
    while pygame.time.get_ticks() < end:
        game.pygameText(s, 50, 100, "Press Q to reveal", 50, 200)
    #print("Question: ",self.__front)
    #input("Answer: ")
    pygame.event.clear()
    
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
    elif event.type == KEYDOWN:
        match chr(event.key):
            case 'q':
                end = pygame.time.get_ticks() + 1500
                while pygame.time.get_ticks() < end:
                    game.pygameText(f"Answer: {back}", 5, 50)
                end = pygame.time.get_ticks() + 1500
                while pygame.time.get_ticks() < end:
                    game.pygameText(f"From 0-3, how accurate was your answer?", 50, 100, "0 being incorrect & 3 being correct,", 5, 250)
                
            case _: pass
            
    score = 0
    pygame.event.clear()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
    elif event.type == KEYDOWN:
        print(event.key)
        match event.key:
            case 48|49| 50| 51:
                score = int(chr(event.key))
                #break
            case _: pass
        #break
    #score = input() # actually do this thru pygame
    useCard(card, score) # sends card back to flashcard_algorithm with new score to shuffle it back in and update values
    return score
    

class entity:
    def __init__(self, maxHealth):
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
    def damage(self, dmg):
        self.currentHealth = max(0, self.currentHealth - dmg)
    def heal(self, hp):
        self.currentHealth = min(self.maxHealth, self.currentHealth + hp)
    def __str__(self):
        return ("Health: "+str(self.currentHealth)+"/"+str(self.maxHealth))
    def isDead(self):
        return self.currentHealth == 0

from datetime import datetime, timedelta

# Scores:
# 0 -- no knowledge 
# 1 -- little knowledge 
# 2 -- okay knowledge 
# 3 -- great knowledge 

# temp array to store -- database later
# when game starts, flashcards will be in an array
flashcardsArr = []

# flashcard class
class flashcard:
    def __init__(self, front, back, score, time):
        self.__front = front
        self.__back = back
        self.__score = score
        self.__last_seen = time
    def __str__(self):
        return "Front: "+self.__front+"\nBack: "+self.__back+"\nScore: "+str(self.__score)+"\nLast studied: "+str(self.__last_seen)
    def test(self):
        end = pygame.time.get_ticks() + 1500
        while pygame.time.get_ticks() < end:
            game.pygameText(f"Question: {self.__front}", 50, 50)
        #print("Question: ",self.__front)
        #input("Answer: ")
        end = pygame.time.get_ticks() + 1500
        while pygame.time.get_ticks() < end:
            game.pygameText("From 0-3, how accurate was your answer?", 50, 50, "with 0 being fully incorrect and 3 being fully correct,", 50, 250)
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                match chr(event.key):
                    case '0','1','2','3':
                        score = int(chr(event.key))
                    case 'r': 
                        end = pygame.time.get_ticks() + 1500
                        while pygame.time.get_ticks() < end:
                            game.pygameText(f"From 0-3, how accurate was your answer?", 50, 50, "with 0 being fully incorrect and 3 being fully correct,", 50, 250)
                    case _: pass
                break
                    
        #while score.isnumeric() == False or 0 > int(score) or 3 < int(score):
        #    score = input("Please enter 0, 1, 2, or 3: ")
        self.change_score(int(score)) 
        self.__last_seen = datetime.now()
        updateScoreTime(self) # changes score and last_seen in database for this card
        return int(score)
    def get_atts_for_db(self):
        return (self.__front, self.__back, self.__score, str(self.__last_seen))
    def get_score_time(self):
        return (self.__score, self.__last_seen)
    def change_score(self, userScore):
        if userScore >= 2:
            self.__score = self.__score + userScore - 1
        else:
            self.__score = max(self.__score + userScore - 2, 0)


# create a new flashcard from user-entered text
def newFlashcard():
    front = input("Question: ")
    back = input("Answer: ")
    flashcardsArr.append(flashcard(front, back, 0, datetime.now()))
    print(flashcardsArr[-1])

def uploadFlashcards():
    for card in flashcardsArr:
        uploadCard(card)
    print("All done :)")

def createFlashcards(num):
    for i in range(0, num):
        newFlashcard()
    uploadFlashcards()

# download and instantiate cards
def getCards():
    cards = downloadCards()
    for card in cards:
        flashcardsArr.append(flashcard(card[0], card[1], card[2], datetime.strptime(card[3], '%Y-%m-%d %H:%M:%S.%f')))
    return flashcardsArr

class Wall:
    def __init__(self, xPos, YPos, Width, Height) -> None:
        self.x = xPos
        self.y = YPos
        self.width = Width
        self.height = Height
        self.type = "wall"

    def draw(self, surface):
        pygame.draw.rect(surface, black, pygame.Rect(self.x, self.y, self.width, self.height))

    def update(self, gameObjects):
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
        pygame.draw.circle(surface, red, (self.x, self.y), self.radius)

    def update(self, gameObjects):
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
    
    def wallcollision(self, gameObj):
        closestX = gameObj.x if (self.x < gameObj.x) else (gameObj.x+gameObj.width if self.x > gameObj.x+gameObj.width else self.x)
        closestY = gameObj.y if self.y < gameObj.y else (gameObj.y+gameObj.height if self.y > gameObj.y+gameObj.height else self.y)
        
        dx = closestX - self.x
        dy = closestY - self.y

        return ( dx * dx + dy * dy ) <= self.radius * self.radius

    def update(self, gameObjects):
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
        global ends, levels, starts
        end = ends[int(2*levels - 2)]
        if (end[0] - self.x)**2 + (end[1] - self.y)**2 <= (end[2] + self.radius)**2: 
            levels += 0.5
            #pygame.quit()
        for gameObj in gameObjects:
            match gameObj.type:
                case "ball":
                    if (gameObj.x - self.x)**2 + (gameObj.y - self.y)**2 <= (gameObj.radius + self.radius)**2:
                        self.x, self.y = starts[int(2*levels - 2)]
                case "wall":
                    if self.wallcollision(gameObj):
                        self.x, self.y = starts[int(2*levels - 2)]
                case _: pass
        #cord = pygame.mouse.get_pos()
        #self.x = cord[0]
        #self.y = cord[1]

# unused as of now
class Text:
    def __init__(self, s = '', xPos =  resolution[0] / 2, yPos = resolution[1] / 2):
        self.x = xPos
        self.y = yPos
        self.string = s

    def draw(self, surface):
        f = pygame.font.Font("Arial", 36)
        
        # print the text
        end = pygame.time.get_ticks() + 1500
        text_surface = f.render(s, True, black)
        while pygame.time.get_ticks() < end:
            self.screen.blit(text_surface, dest=(xPos,yPos))
            pygame.display.flip()

    def update(self, gameObjects):
        pass

class game(): # main game loop
    def __init__(self):
        
        self.clock = pygame.time.Clock()
        self.gameObjects = []
        # maze 1
        self.gameObjects.append(Player(20, 30, 30))
        self.gameObjects.append(Wall(60, 0, 30, 180))
        #self.gameObjects.append(Wall(60, 170, 100, 30))
        #self.gameObjects.append(Wall(230, 220, 100, 30))
        #self.gameObjects.append(Wall(140, 50, 30, 150))
        #self.gameObjects.append(Wall(310, 130, 100, 30))
        #self.gameObjects.append(Wall(230, 200, 30, 150))
        #self.gameObjects.append(Wall(60, 170, 30, 80))
        #self.gameObjects.append(Wall(140, 260, 30, 150))
        #self.gameObjects.append(Wall(230, 50, 30, 180))
        #self.gameObjects.append(Wall(230, 50, 100, 30))
        #self.gameObjects.append(Ball())
        #self.gameObjects.append(Ball(250))
    
    def newlevel(self, levels, objects):
        #screen.fill(white)
        self.gameObjects = []
        if levels == 1:
            self.gameObjects.append(Player(20, 30, 30))
            self.gameObjects.append(Wall(60, 0, 30, 180))
            self.gameObjects.append(Wall(60, 170, 100, 30))
            self.gameObjects.append(Wall(230, 220, 100, 30))
            self.gameObjects.append(Wall(140, 50, 30, 150))
            self.gameObjects.append(Wall(310, 130, 100, 30))
            self.gameObjects.append(Wall(230, 200, 30, 150))
            self.gameObjects.append(Wall(60, 170, 30, 80))
            self.gameObjects.append(Wall(140, 260, 30, 150))
            self.gameObjects.append(Wall(230, 50, 30, 180))
            self.gameObjects.append(Wall(230, 50, 100, 30))
        else:
            for gameObj in objects[int(levels*2 - 3)]:
                self.gameObjects.append(gameObj)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    def run(self):
        while True:
            global screen
            self.handleEvents()
            currentlevel = 1
            for gameObj in self.gameObjects:
                gameObj.update(self.gameObjects)

            screen.fill(white)

            for gameObj in self.gameObjects:
                gameObj.draw(screen)

            global levels, objects
            if levels > currentlevel:
                currentlevel += 0.5
                self.newlevel(levels, objects)
            if (levels % 1 == 0.5):
                end = pygame.time.get_ticks() + 1500
                match self.battle():
                    case -1: 
                        while pygame.time.get_ticks() < end:
                            self.pygameText("You died :(", 100,150)
                        levels -= 0.5
                    case 0: 
                        while pygame.time.get_ticks() < end:
                            self.pygameText("It's a tie?", 100,150, " Make more flashcards!", 100, 250)
                        levels -= 0.5
                    case 1: 
                        while pygame.time.get_ticks() < end:
                            self.pygameText("You win! :)", 100,150)
                        levels += 0.5
                    case _: pass
                self.newlevel(levels, objects)

            self.clock.tick(60)
            pygame.display.flip()
    
    def pygameText(s = '', xPos = 100, yPos = 100, t = '', xPos2 = 100, yPos2 = 100):
        #print(type(str(s)))
        global screen
        f = pygame.font.Font(None, 25)
        screen.fill(white)
        # print the text
        #end = pygame.time.get_ticks() + 1500
        text_surface = f.render(str(s), True, black)
        text2 = f.render(str(t), True, black)
        #while pygame.time.get_ticks() < end:
        #print((xPos, yPos))
        screen.blit(text_surface, (xPos,yPos))
        screen.blit(text2, (xPos2,yPos2))
        pygame.display.flip()
        #screen.fill(white)

    def battle(self):
        player = entity(20)
        boss = entity(5)

        startDeck(20)
        while not deckEmpty() and not player.isDead() and not boss.isDead():
            #print("Player")
            #print(player) # show player health
            game.pygameText(f"Player {player}",100,100, f"Boss {boss}", 100, 200)
            #print("----")
            #print("Boss") # show boss health
            #print(boss)
            #self.pygameText(f"Boss {boss}", 100, 100)
            #print("----")
            score = testCard() # 0, 1, 2, or 3 depending on how well player knows card 
            # how the hell do i get this to show onto the screen 
            if score > 1:
                score -= 1
                boss.damage(score) # 1 or 2 dmg
            else:
                score += 1
                player.damage(score) # 1 or 2 dmg

        if player.isDead():
            print("You died :(")
            return -1
        elif boss.isDead():
            print("You win! :)")
            return 1
        else:
            print("It's a tie?")
            return 0
    

objects = [[Player(20, 30, 30)], #level 1.5 aka battle 1
           [Player(20, 30, 30),Wall(60, 0, 30, 200),Wall(145, 60, 30, 300),Wall(230, 0, 30, 200),Wall(320, 60, 30, 300)], #level 2 puzzle
           [Player(20, 100, 150),Ball(200)], #battle 2
           [Player(20, 30, 30),Wall(60, 0, 30, 200),Wall(145, 60, 30, 300),Wall(230, 0, 30, 200),Wall(320, 60, 30, 300), Ball(200), Ball(100)], # puzzle 3
           [Player(20, 30, 30)], #battle 3
           [] #end screen?
]
ends = [(400,300,25),(400,300,25),(400,300,25),(400,300,25),(400,300,25),(400,300,25)] # (x,y,distance)
starts = [(30,30),(30,30),(30,30),(30,30),(30,30),(100,150)]
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(resolution)
game().run()