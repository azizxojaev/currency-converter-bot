import sqlite3 as sql


con = sql.connect('database.db')
cur = con.cursor()


def create_tables():
    global con, cur
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
            from_cur TEXT,
            to_cur TEXT,
            id INTEGER
    )""")


async def create_user(id):
    if cur.execute(f"SELECT * FROM user WHERE id = {id}").fetchone() == None:
        cur.execute(f"INSERT INTO user (id, from_cur, to_cur) VALUES (?, ?, ?)", (id, 'usd', 'rub'))
        con.commit()

    
async def get_user(id):
    return cur.execute(f"SELECT * FROM user WHERE id = {id}").fetchone()


async def update_user(id, from_cur, to_cur):
    cur.execute(f'UPDATE user SET from_cur = ?, to_cur = ? WHERE id = {id}', (from_cur, to_cur))
    con.commit()