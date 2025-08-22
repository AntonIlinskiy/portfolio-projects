import sqlite3

con = sqlite3.connect("healthbot.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

print("Структура таблицы users:")
for col in cur.execute("PRAGMA table_info(users);"):
    print(dict(col))

print("\nПоследние записи:")
for row in cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 5;"):
    print(dict(row))

con.close()
