# use MySQL

import mysql.connector
import database_login as login

# admin credentials
def adminLogin():
  mydb = mysql.connector.connect(
    host="localhost",
    user= login.username,
    password=login.password
  )
  return mydb.cursor()

# can only SELECT, UPDATE, and INSERT
def guestLogin():
  mydb = mysql.connector.connect(
    host="localhost",
    user= "guest",
    password= "\"e$G}bkXs500"
  )
  return mydb

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
    mycursor.execute(f"SELECT score FROM {db} WHERE username ={user}")
    return mycursor.fetchall()
    # returns empty list or [(score)]

def addScore(mycursor, score, db):
    username = input("Enter your username: ")
    if fetchUserScore(username, db): # executes if not empty i.e.: user already exists in db
        command = f"UPDATE {db} SET score ={score} WHERE username ={username}"
    else:
        command = f"INSERT INTO {db} (username, score) VALUES ({username}, {score})"
    mycursor.execute(command)

db = adminLogin()
cursor = db.cursor()
globalBoard(cursor)
db.commit()