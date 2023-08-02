import sqlite3 

connection = sqlite3.connect('bot.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    username VARCHAR(200),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    created VARCHAR(100)
);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS sights (
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(200),
    longitude VARCHAR(100),
    latitude VARCHAR(100)
);
""")