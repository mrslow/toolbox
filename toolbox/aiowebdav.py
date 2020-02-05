import asyncio
from aiohttp import ClientSession, TCPConnector


class OperationFailed(Exception):
    def __init__(self, method, path, expected_codes, actual_code):
        self.reason = f'Failed on {method} "{path}"'

        expected = ", ".join([str(code) for code in expected_codes])

        msg = f'{self.reason}. Receiving {actual_code}, expected ({expected})'

        super(OperationFailed, self).__init__(msg)


class WebDavClient:
    def __init__(self,
                 host,
                 port=80,
                 loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.baseurl = f'http://{host}:{port}'
        self.session = ClientSession(connector=TCPConnector())
        self._closed = False

    async def _send(self, method, path, expected_codes, **kwargs):
        url = self._get_url(path)
        resp = await self.session.request(method, url, allow_redirects=False,
                                          **kwargs)
        if resp.status not in expected_codes:
            raise OperationFailed(method, path, expected_codes, resp.status)
        return resp

    def _get_url(self, path):
        return f'{self.baseurl}/{str(path).strip("/ ")}'

    async def delete(self, remote_path):
        await self._send('DELETE', remote_path, (204,))

    async def upload(self, fileobj, remote_path):
        await self._send('PUT', remote_path, (200, 201, 204), data=fileobj)

    async def download(self, remote_path, fileobj):
        resp = await self._send('GET', remote_path, (200, 206))
        fileobj.write(await resp.content.read())

    async def close(self):
        await self.session.close()
        self._closed = True
