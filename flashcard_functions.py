import datetime

# Scores:
# 0 -- no knowledge 
# 1 -- little knowledge 
# 2 -- okay knowledge 
# 3 -- great knowledge 

# temp array to store -- database later
flashcards = []

# flashcard class
class flashcard:
    def __init__(self, front, back):
        self.front = front
        self.back = back
        self.score = 0
        self.last_studied = datetime.datetime.now()
    def __str__(self):
        return "Front: "+self.front+"\nBack: "+self.back+"\nScore: "+str(self.score)+"\nLast studied: "+str(self.last_studied)
    def test(self):
        print("Question: ",self.front)
        input("Answer: ")
        score = input("On a scale of 0 to 3, with 0 being fully incorrect and 3 being fully correct, how accurate was your answer?\n")
        while score.isnumeric == False or 0 < int(score) or 3 > int(score):
            score = input("Please enter 0, 1, 2, or 3: ")
        self.last_studied = datetime.datetime.now()

# create a new flashcard from user-entered text
def newFlashcard():
    front = input("Question: ")
    back = input("Answer: ")
    flashcards.append(flashcard(front, back))
    print(flashcards[-1])