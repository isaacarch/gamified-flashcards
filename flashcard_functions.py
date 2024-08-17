import datetime
from flashcard_database import uploadCard

# Scores:
# 0 -- no knowledge 
# 1 -- little knowledge 
# 2 -- okay knowledge 
# 3 -- great knowledge 

# temp array to store -- database later
flashcardsArr = []

# flashcard class
class flashcard:
    def __init__(self, front, back):
        self.__front = front
        self.__back = back
        self.__score = 0
        self.__last_seen = datetime.datetime.now()
    def __str__(self):
        return "Front: "+self.__front+"\nBack: "+self.__back+"\nScore: "+str(self.__score)+"\nLast studied: "+str(self.__last_seen)
    def test(self):
        print("Question: ",self.__front)
        input("Answer: ")
        score = input("On a scale of 0 to 3, with 0 being fully incorrect and 3 being fully correct, how accurate was your answer?\n")
        while score.isnumeric == False or 0 < int(score) or 3 > int(score):
            score = input("Please enter 0, 1, 2, or 3: ")
        self.__last_seen = datetime.datetime.now()
    def get_atts(self):
        return (self.__front, self.__back, self.__score, str(self.__last_seen))

# create a new flashcard from user-entered text
def newFlashcard():
    front = input("Question: ")
    back = input("Answer: ")
    flashcardsArr.append(flashcard(front, back))
    print(flashcardsArr[-1])

def uploadFlashcards():
    for card in flashcardsArr:
        print("Uploading...")
        uploadCard(card)
    print("All done :)")

newFlashcard()
newFlashcard()
newFlashcard()
uploadFlashcards()