from datetime import timedelta, datetime
import random

# download and instantiate cards
def getCards():
    cards = downloadCards()
    for card in cards:
        flashcardsArr.append(flashcard(card[0], card[1], card[2], datetime.strptime(card[3], '%Y-%m-%d %H:%M:%S.%f')))
    return flashcardsArr

# global vars
activeCards = getCards()
inactiveCards = []

# rounds time to nearest 5 mins
def roundTime(time):
    timeString = str(time)[0:16]
    offsetMins = 0
    timeMinOne = int(timeString[-1])
    if timeMinOne < 3:
        offsetMins = 0
    elif timeMinOne < 8:
        offsetMins = 5
    else:
        offsetMins = 10
    timeString = str(time)[0:15] + "0:00.000000"
    return datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes = offsetMins)

# score is positive integer
# 0: 5 minutes
# 1: 10 minutes
# 2: 20 minutes
# 3: 30 minutes
#...

# calculate what time to review card
def whenToStudy(card):
    (score, last_seen) = card.get_score_time()
    return last_seen + timedelta(minutes = score*10)

def studyingSoon(card):
    timeUntilStudied = whenToStudy(card) - datetime.now()
    minutesUntilStudied = timeUntilStudied.total_seconds() / 60
    return minutesUntilStudied < 20

# sort cards by time to study
def sortCards():
    global activeCards
    global inactiveCards
    inactiveCards = [card for card in activeCards if not studyingSoon(card)]
    activeCards = [card for card in activeCards if studyingSoon(card)]
    activeCards.sort(key=lambda x: (roundTime(whenToStudy(x)), random.random()), reverse=True)
    return activeCards, inactiveCards

def testCard():
    card = activeCards.pop()
    score = card.test()
    activeCards.append(card)
    sortCards()
    return score

def deckEmpty():
    return len(activeCards) == 0

def getSortedCards():
    sortCards()
    return activeCards

def startDeck(maxSize):
    global activeCards
    global inactiveCards
    if not deckEmpty():
        overflow = max(0, len(activeCards) - maxSize)
        actualSize = len(activeCards) - overflow
        sortCards()
        inactiveCards.extend(activeCards[0:overflow])
        activeCards = activeCards[overflow:]
    else:
        print("No cards in deck!")