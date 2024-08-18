# use SQLite
# datetime is stored as string

import sqlite3

# Connect to / create flashcard database
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()

# Create cards table
cursor.execute('''CREATE TABLE IF NOT EXISTS myCards(
               front TEXT PRIMARY KEY, 
               back TEXT, 
               score INT, 
               last_seen TEXT
               )''')

# Insert a row of data
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
# conn.commit()

# Close the connection
conn.close()

def uploadCard(card):
    # only uploads if not making duplicate
    if not doesCardExist(card):
        print("Uploading...")
        atts = card.get_atts_for_db()
        conn = sqlite3.connect('flashcards.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO myCards VALUES {atts}")
        conn.commit()
        conn.close()
    else:
        print("Duplicate: could not upload card")

def downloadCards():
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
SELECT *
FROM myCards
ORDER BY last_seen;
''') #oldest first
    cards = cursor.fetchall()
    conn.close()
    return cards
# cards is an array of tuples. each card is a row, and each field is an entry in the tuple

# returns truthy or falsey value
def doesCardExist(card):
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    atts = card.get_atts_for_db()
    front = atts[0]
    cursor.execute(f"SELECT * FROM myCards WHERE front=?",(front,))
    x = cursor.fetchall()
    conn.close()
    return x

# Should have same front, and back will not be updated
def updateScoreTime(newCard):
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    atts = newCard.get_atts_for_db()
    front = atts[0]
    score = atts[2]
    last_seen = atts[3]
    cursor.execute('''
UPDATE myCards
SET score= ?, last_seen= ?
WHERE front=?
''', (score, last_seen, front,))
    conn.commit()
    conn.close()