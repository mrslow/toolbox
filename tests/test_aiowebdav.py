import pytest
from io import BytesIO
from toolbox import WebDavClient
from toolbox.aiowebdav import OperationFailed

pytestmark = [pytest.mark.asyncio]


@pytest.mark.usefixtures('ws')
class TestWebDavClient:

    async def test_init_no_port(self):
        wc = WebDavClient('localhost')
        assert wc.baseurl == 'http://localhost:80'

    async def test_ex(self, wc):
        with pytest.raises(OperationFailed):
            await wc._send('PROPFIND', '/nonexist', (207,))
        await wc._send('GET', '/', (200, ))

    @pytest.mark.parametrize('folder',
                             ['', 'nonexist'],
                             ids=['exist', 'non-exist'])
    async def test_upload(self, wc, folder, tmpdir):
        remote_path = f'{folder}/test_upload.txt'
        local_path = tmpdir.join(remote_path)
        await wc.upload(b'Uploadable content', remote_path)

        assert local_path.check()
        assert local_path.read() == 'Uploadable content'

    @pytest.mark.parametrize('folder',
                             ['', 'sub'],
                             ids=['direct', 'subfolder'])
    async def test_delete(self, wc, tmpdir, folder):
        remote_path = f'{folder}/test_remove.txt'
        local_path = tmpdir.join(remote_path)
        local_path.write('Deletable content', ensure=True)

        assert local_path.check()
        await wc.delete(remote_path)
        assert not local_path.check()

    @pytest.mark.parametrize('folder',
                             ['', 'sub'],
                             ids=['direct', 'subfolder'])
    async def test_download(self, wc, tmpdir, folder):
        remote_path = f'{folder}/test_download.txt'
        local_path = tmpdir.join(remote_path)
        local_path.write('Downloadable content', ensure=True)

        assert local_path.check()
        fileobj = BytesIO()
        await wc.download(remote_path, fileobj)
        assert local_path.read() == fileobj.getvalue().decode()
