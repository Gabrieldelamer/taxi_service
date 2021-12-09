import sqlite3

connection = sqlite3.connect('taxi_db')
cursor = connection.cursor()

connection.commit()
connection.close()