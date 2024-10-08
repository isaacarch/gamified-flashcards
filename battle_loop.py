from flashcard_algorithm import startDeck, getCard, deckEmpty, useCard

# need to get cards with fixed game size


def testCard():
    card = getCard()
    front = card.getFront()
    back = card.getBack()
    # display card front 
    # user inputs text for what they think is on the back 
    # display card back 
    # user enters score 
    score = input() # actually do this thru pygame
    useCard(card, score) # sends card back to flashcard_algorithm with new score to shuffle it back in and update values
    
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

def battle():
    player = entity(20)
    boss = entity(5)

    startDeck(20)
    while not deckEmpty() and not player.isDead() and not boss.isDead():
        print("Player")
        print(player)
        print("----")
        print("Boss")
        print(boss)
        print("----")
        score = testCard() # 0, 1, 2, or 3 depending on how well player knows card 
        if score > 1:
            score -= 1
            boss.damage(score) # 1 or 2 dmg
        else:
            score += 1
            player.damage(score) # 1 or 2 dmg

    if player.isDead():
        print("You died :(")
    elif boss.isDead():
        print("You win! :)")
    else:
        print("It's a tie?")
