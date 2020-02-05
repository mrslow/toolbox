import pytest
import time

from aiohttp import ClientConnectionError, ClientSession
from toolbox import WebDavClient
from multiprocessing import Process

from .webdav_server import LocalWebdavServer


@pytest.fixture
async def ws(tmpdir):
    server = LocalWebdavServer(str(tmpdir), verbose=0).get_server()
    server_process = Process(target=server.start)
    server_process.start()
    await ensure_server_initialized(server_process)
    yield
    server_process.terminate()


async def ensure_server_initialized(server_process):
    timeout = time.time() + 5
    while True:
        if timeout < time.time():
            server_process.terminate()
            pytest.exit('WebDAV server did not respond')
        try:
            async with ClientSession() as session:
                async with session.head('http://localhost:28080') as response:
                    if response.status != 500:
                        break
        except ClientConnectionError:
            pass
        except Exception as exc:
            server_process.terminate()

        time.sleep(0.1)


@pytest.fixture
async def wc(event_loop):
    client = WebDavClient('localhost', 28080, event_loop)
    yield client
    await client.close()
