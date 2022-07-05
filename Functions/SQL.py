import aiomysql
import asyncio
import json

from collections import namedtuple

with open("Data/cfg.json", encoding="utf8") as data:
    config = json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))


global pool


async def StartMySQL():
    global pool
    pool = await aiomysql.create_pool(autocommit=True, host=config.sql_host, user=config.sql_user, password=config.sql_pass, db=config.sql_db)


async def execute(query):
    conn = await pool.acquire()
    cur = await conn.cursor()

    try:
        await cur.execute(f"{query}")
    except:
        pass
    finally:
        await pool.release(conn)

    return True


async def select(query, one=False, nested=False, dict=False):
    conn = await pool.acquire()

    if not dict:
        cur = await conn.cursor()
    else:
        cur = await conn.cursor(aiomysql.DictCursor)

    try:
        await cur.execute(query)

        if one:
            row = await cur.fetchone()
            if row:
                return row[0]

        row = await cur.fetchall()

        if nested:
            return row

        return row[0]
    except:
        return None
    finally:

        await pool.release(conn)

loop = asyncio.get_event_loop()
loop.run_until_complete(StartMySQL())
