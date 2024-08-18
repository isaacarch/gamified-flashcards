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

# the tablename functions as a password bc this is what you enter to upload your score to the table 
def createPrivateTable(tableName):
   db = adminLogin()
   cursor = db.cursor()
   command = f'''
CREATE TABLE IF NOT EXISTS {tableName}
(
username VARCHAR(20),
score INT,
PRIMARY KEY (username)
)
'''
   cursor.execute(command)
   db.commit()
   cursor.close()
   db.close()

def fetchUserScore(mycursor, user, board):
    mycursor.execute(f"SELECT score FROM {board} WHERE username =%s", (user,))
    return mycursor.fetchall()
    # returns empty list or [(score)]


def addScore(username, score, board):
    db = guestLogin()
    cursor = db.cursor()
    if fetchUserScore(cursor, username, board): # executes if not empty i.e.: user already exists in db
        command = f"UPDATE {board} SET score =%s WHERE username =%s"
        values = (score, username)
    else:
        command = f"INSERT INTO {board} (username, score) VALUES (%s, %s)"
        values = (username, score)
    cursor.execute(command, values)
    db.commit()
    cursor.close()
    db.close()

def addScoreToGlobal():
   username = input("Enter your username: ")
   score = input("Enter your score: ")
   addScore(username, score, "global_board")

# If private board doesn't exist, it will be created
def addScoreToPrivate():
   board = input("Enter the name of your leaderboard: ")
   createPrivateTable(board)
   username = input("Enter your username: ")
   score = input("Enter your score: ")
   addScore(username, score, board)