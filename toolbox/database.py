from typing import Any, List
import asyncpg


class DBPool:
    def __init__(self, config, size=10) -> None:
        self._pool = None
        self._codec_list = []
        self.closed = False
        self.config = config
        self.size = size

    def set_codec(self, typename, *,
                  schema='pg_catalog',
                  format='text',
                  encoder,
                  decoder) -> None:
        self._codec_list.append({
            'typename': typename,
            'schema': schema,
            'encoder': encoder,
            'decoder': decoder,
            'format': format,
        })

    async def _codecs(self, con):
        for codec in self._codec_list:
            await con.set_type_codec(**codec)

    async def create(self) -> None:
        self._pool = await asyncpg.create_pool(**self.config,
                                               init=self._codecs,
                                               min_size=self.size,
                                               max_size=self.size)

    async def close(self) -> None:
        if not self.closed:
            await self._pool.close()
            self.closed = True

    async def _exec(self, method, query, args, t_out) -> Any:
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                return await getattr(conn, method)(query, *args, timeout=t_out)

    async def fetch(self, query, *args, timeout=None) -> List[asyncpg.Record]:
        return await self._exec('fetch', query, args, timeout)

    async def fetchval(self, query, *args, timeout=None) -> Any:
        return await self._exec('fetchval', query, args, timeout)

    async def fetchrow(self, query, *args, timeout=None) -> asyncpg.Record:
        return await self._exec('fetchrow', query, args, timeout)

    async def execute(self, query, *args, timeout=None) -> str:
        return await self._exec('execute', query, args, timeout)

    async def executemany(self, query, args, timeout=None) -> None:
        return await self._exec('executemany', query, (args,), timeout)
