import asyncpg

# from psycopg2 import pool
# import configs


class Database:
    def __init__(self):
        self.user = "postgres"
        self.password = "Aysel.42"
        self.host = "localhost"
        self.port = "5432"
        self.database = "fastapi"
        self._cursor = None

        self._connection_pool = None
        self.con = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )

            except Exception as e:
                print(e)

    async def fetch_rows(self, query: str):
        if not self._connection_pool:
            await self.connect()
        else:
            self.con = await self._connection_pool.acquire()
            try:
                result = await self.con.fetch(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(self.con)
