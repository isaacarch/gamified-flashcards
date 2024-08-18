# use SQlite

import sqlite3

# Connect to / create flashcard database
conn = sqlite3.connect('leaderboards_lite.db')
cursor = conn.cursor()

# Create cards table
cursor.execute('''CREATE TABLE IF NOT EXISTS globalBoard(
               username TEXT PRIMARY KEY, 
               points INT
               )''')

# Insert a row of data
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
# conn.commit()

# Close the connection
conn.close()

def userExists(username):
    conn = sqlite3.connect('leaderboards_lite.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM globalBoard WHERE username=?",(username,))
    x = cursor.fetchall()
    conn.close()
    return x

def addName(username, score):
    conn = sqlite3.connect('leaderboards_lite.db')
    cursor = conn.cursor()
    if userExists(username):
        cursor.execute("UPDATE globalBoard SET points=? WHERE username=?",(score, username,))
    else:
        cursor.execute("INSERT INTO globalBoard VALUES (?,?)",(username, score,))
    conn.commit()
    conn.close()