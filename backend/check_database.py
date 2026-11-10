import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM movies")
count = cursor.fetchone()[0]

print("Total movies:", count)

cursor.execute("""
    SELECT id, title, genres, rating, release_date
    FROM movies
    LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()