from datetime import datetime
from flashcard_database import uploadCard, downloadCards

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
        print("Question: ",self.__front)
        input("Answer: ")
        score = input("On a scale of 0 to 3, with 0 being fully incorrect and 3 being fully correct, how accurate was your answer?\n")
        while score.isnumeric() == False or 0 > int(score) or 3 < int(score):
            score = input("Please enter 0, 1, 2, or 3: ")
        self.change_score(int(score))
        self.__last_seen = datetime.now()
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
        print("Uploading...")
        uploadCard(card)
    print("All done :)")

# download and instantiate cards
def getCards():
    cards = downloadCards()
    for card in cards:
        flashcardsArr.append(flashcard(card[0], card[1], card[2], datetime.strptime(card[3], '%Y-%m-%d %H:%M:%S.%f')))
    return flashcardsArr