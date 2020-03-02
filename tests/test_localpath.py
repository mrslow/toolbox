from os import PathLike
from toolbox import LocalPath


def test_init(tmpdir):
    local_path = LocalPath(tmpdir)
    local_path_str = LocalPath(str(tmpdir))

    assert isinstance(local_path, PathLike)
    assert isinstance(local_path_str, PathLike)


def test_magic_methods(tmpdir):
    local_path = LocalPath(tmpdir)

    assert local_path == tmpdir
    assert str(local_path) == str(tmpdir)
    assert local_path.__hash__() == tmpdir.__hash__()
    assert local_path.__fspath__() == tmpdir.__fspath__()
    assert local_path + 'test.zip' == tmpdir + 'test.zip'


def test_join(tmpdir):
    local_path = LocalPath(tmpdir)

    new_local_path = local_path.join('dir', 'test.zip')
    new_tmpdir_path = tmpdir.join('dir', 'test.zip')

    assert isinstance(new_local_path, LocalPath)
    assert new_local_path == new_tmpdir_path
    assert new_local_path != local_path


def test_listdir(tmpdir):
    tmpdir.join('test.zip').write('dummy')
    tmpdir.join('test2.zip').write('dummy')

    local_path = LocalPath(tmpdir)
    listdir = local_path.listdir()

    assert isinstance(listdir, list)
    assert len(listdir) == 2
    assert set(listdir) == set(('test.zip', 'test2.zip'))


def test_move(tmpdir):
    dst = tmpdir.ensure_dir('dir').join('test.zip')
    src = tmpdir.join('test.zip')
    src.write('dummy')

    local_path = LocalPath(src)

    assert local_path.move(str(dst))
    assert dst.check()
    assert not src.check()
    assert dst.read() == 'dummy'


def test_ensure_dir(tmpdir):
    local_path = LocalPath(tmpdir)

    new_local_path = local_path.ensure_dir('dir')
    new_tmpdir_path = tmpdir.join('dir')

    assert isinstance(new_local_path, LocalPath)
    assert new_tmpdir_path.check()


def test_remove(tmpdir):
    src = tmpdir.join('test.zip')
    src.write('dummy')

    local_path = LocalPath(src)

    assert local_path.remove()
    assert not src.check()


def test_read(tmpdir):
    src = tmpdir.join('test.zip')
    src.write('dummy')

    local_path = LocalPath(src)

    assert local_path.read() == b'dummy'
    assert local_path.read(mode='r') == 'dummy'


def test_write(tmpdir):
    src = tmpdir.join('dir', 'test.zip')

    local_path = LocalPath(src)
    local_path.write(b'dummy', ensure=True)

    assert src.check()
    assert src.read() == 'dummy'


def test_encode(tmpdir):
    local_path = LocalPath(str(tmpdir))

    encoded_local_path = local_path.encode('utf-8')

    assert isinstance(encoded_local_path, bytes)
    assert encoded_local_path.decode() == tmpdir


def test_exist(tmpdir):
    not_exist_file = tmpdir.join('test_0.zip')
    exist_file = tmpdir.join('test_1.zip')
    exist_file.write('dummy')
    not_exist_dir = tmpdir.join('test_0/')
    exist_dir = tmpdir.ensure_dir('test_1/')

    local_path_not_exist_file = LocalPath(str(not_exist_file))
    local_path_exist_file = LocalPath(str(exist_file))
    local_path_not_exist_dir = LocalPath(str(not_exist_dir))
    local_path_exist_dir = LocalPath(str(exist_dir))

    assert local_path_not_exist_file.exist() is False
    assert local_path_exist_file.exist() is True
    assert local_path_not_exist_dir.exist() is False
    assert local_path_exist_dir.exist() is True
