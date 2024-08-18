# use MySQL

import mysql.connector
import database_login as login

# admin credentials
def adminLogin():
  mydb = mysql.connector.connect(
    host="localhost",
    user= login.username,
    password=login.password,
    database = "leaderboards"
  )
  return mydb

# can only SELECT, UPDATE, and INSERT
def guestLogin():
  mydb = mysql.connector.connect(
    host="localhost",
    user= "guest",
    password= "\"e$G}bkXs500",
    database = "leaderboards"
  )
  return mydb

def createDB(mycursor):
   mycursor.execute("CREATE DATABASE leaderboards")

def globalBoard(mycursor):
    command = '''
CREATE TABLE IF NOT EXISTS global_board
(
username VARCHAR(20),
score INT,
PRIMARY KEY (username)
);
'''
    mycursor.execute(command)

def fetchUserScore(mycursor, user):
    mycursor.execute("SELECT score FROM global_board WHERE username =%s", (user,))
    return mycursor.fetchall()
    # returns empty list or [(score)]

def addScore(username, score):
    db = guestLogin()
    cursor = db.cursor()
    if fetchUserScore(cursor, username): # executes if not empty i.e.: user already exists in db
        command = "UPDATE global_board SET score =%s WHERE username =%s"
        values = (score, username)
    else:
        command = "INSERT INTO global_board (username, score) VALUES (%s, %s)"
        values = (username, score)
    cursor.execute(command, values)
    db.commit()

addScore("Bob", 40)