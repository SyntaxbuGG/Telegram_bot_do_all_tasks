import asyncpg


class ConnectPostgres:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def check_user(self, userid):
        async with self.pool.acquire() as con:
            results = await con.fetchrow('SELECT id_ FROM users_telegram where user_id = $1', userid)
            return results

    async def check_user_weather(self, userid):
        async with self.pool.acquire() as con:
            results = await con.fetchrow('SELECT users_id FROM user_get_inform where user_id = $1',userid)
            return results

    async def add_user(self, *args):
        async with self.pool.acquire() as con:
            await con.execute('INSERT INTO users_telegram(user_id, firstname, user_name,first_enter)'
                              'VALUES ($1,$2,$3,now()::timestamp(0))', args[0], args[1], args[2])

    async def get_country(self, userid, country):
        async with self.pool.acquire() as con:
            await con.execute('INSERT INTO user_get_inform(users_id,get_country) VALUES ($1,$2)', userid, country)

    async def check_country(self, userid):
        async with self.pool.acquire() as con:
            results = await con.fetchval('SELECT id FROM user_get_inform where users_id = $1', userid)
            return results

    async def execute_query(self, query, *args):
        async with self.pool.acquire() as con:
            await con.execute(query, *args)

    async def fetchrow_query(self, query, *args):
        async with self.pool.acquire() as con:
            result = await con.fetchval(query, *args)
            return result
