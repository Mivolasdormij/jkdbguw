import sqlite3

conn = sqlite3.connect('recipes.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS posts;''')
c.execute('''DROP TABLE IF EXISTS comments;''')
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, comments BLOB)''')
c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, text TEXT)''')

conn.commit()
conn.close()

