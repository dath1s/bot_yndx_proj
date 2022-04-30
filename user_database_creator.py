import sqlite3

cur = sqlite3.connect('db/users.db')

cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_telegram_id INT NOT NULL,
    bin STR NOT NULL,
    price INT
);
""")
# cur.execute('DELETE FROM users WHERE id=3')
# cur.execute('UPDATE users SET id = (SELECT count(*) + 1 FROM users t WHERE t.id < users.id)')
res = cur.execute('SELECT * FROM users')

for i in res:
    print(i)

cur.commit()
