# use SQLite
# datetime is stored as string

import sqlite3

# Connect to / create flashcard database
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()

# Create cards table
cursor.execute('''CREATE TABLE IF NOT EXISTS myCards
             (front text, back text, score int, last_seen text)''')

# Insert a row of data
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
# conn.commit()

# Close the connection
conn.close()

    
def uploadCard(card):
    atts = card.get_atts()
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO myCards VALUES {atts}")
    conn.commit()
    conn.close()