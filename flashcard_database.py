import mysql.connector
import database_login as login

mydb = mysql.connector.connect(
  host="localhost",
  user= login.username,
  password=login.password
)

print(mydb)