from flashcard_functions import getCards
from datetime import timedelta

flashcards = getCards()

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
    flashcards.sort(key=lambda x: whenToStudy(x))

