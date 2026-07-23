from database.database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM lectures")
rows = cursor.fetchall()

print(f"Total lectures: {len(rows)}\n")

for row in rows:
    print(dict(row))

conn.close()