from flashcard_functions import getCards
from datetime import timedelta, datetime
import random

flashcards = getCards()

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

# sort cards by time to study
def sortCards():
    flashcards.sort(key=lambda x: (roundTime(whenToStudy(x)), random.random()))

def nextCard():
    return flashcards.pop(0)