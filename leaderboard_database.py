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

def fetchUserScore(mycursor, user, db):
    mycursor.execute(f"SELECT score FROM {db} WHERE username =%s", (user,))
    return mycursor.fetchall()
    # returns empty list or [(score)]

def addScore(mycursor, score, db):
    username = input("Enter your username: ")
    if fetchUserScore(mycursor, username, db): # executes if not empty i.e.: user already exists in db
        command = f"UPDATE {db} SET score =%s WHERE username =%s"
        values = (score, username)
    else:
        command = f"INSERT INTO {db} (username, score) VALUES (%s, %s)"
        values = (username, score)
    mycursor.execute(command, values)

db = guestLogin()
cursor = db.cursor()
addScore(cursor, 10, "global_board")
db.commit()