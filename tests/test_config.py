import pytest
from toolbox.localpath import LocalPath
from toolbox.config import Config, ConfigError
from tests.conftest import db_yaml_path, env_yaml_path, variables_path
from .data.variables import date_time, time_delta

test_paths = ['test', '/dev/null', LocalPath('test'), LocalPath('/dev/null')]
ids_test_paths = ['str-rel', 'str-abs', 'localpath-rel', 'localpath-abs']


def test_init(tmpdir):
    conf = Config(tmpdir, conf_path=None)

    assert isinstance(conf.proj_path, LocalPath)
    assert conf.proj_path == tmpdir


def test_init_relative():
    with pytest.raises(ConfigError):
        conf = Config('relative/path')


@pytest.mark.parametrize('path', test_paths, ids=ids_test_paths)
def test_init_conf(tmpdir, path, request):
    conf = Config(tmpdir, conf_path=path)
    path = tmpdir.join(path) if 'rel' in request.node.name else path

    assert isinstance(conf.conf_path, LocalPath)
    assert str(conf.conf_path) == str(path)


@pytest.mark.parametrize('path', test_paths, ids=ids_test_paths)
def test_init_files(tmpdir, path, request):
    conf = Config(tmpdir, files_path=path)
    path = tmpdir.join(path) if 'rel' in request.node.name else path

    assert isinstance(conf.files_path, LocalPath)
    assert str(conf.files_path) == str(path)


def test_access_by_key(tmpdir):
    conf = Config(tmpdir, conf_path=None)

    assert conf['proj_path'] == tmpdir


def test_not_exist_var(tmpdir):
    conf = Config(tmpdir, conf_path=None)

    with pytest.raises(AttributeError):
        assert conf.PROJ_PATH
        assert conf['PROJ_PATH']
        assert conf.not_exist
        assert conf['not_exist']


def test_set_var(tmpdir):
    conf = Config(tmpdir, conf_path=None)
    conf.test_value_1 = 42
    conf['test_value_2'] = '42'

    assert conf.test_value_1 == 42
    assert conf['test_value_2'] == '42'


def test_str_method(tmpdir):
    conf = Config(tmpdir, conf_path=None)

    assert str(conf) == f'proj_path = {tmpdir}\n'


def test_read_database(tmpdir):
    dst_db_yaml_path = tmpdir.join('config', 'database.yaml')
    dst_db_yaml_path.write(open(db_yaml_path, 'rb').read(), ensure=True)
    conf = Config(tmpdir)

    assert conf.db == {
        'test_db': {
            'host': 'localhost',
            'user': 'postgres',
            'password': '',
            'database': 'test_db'
        }
    }
    assert conf.redis == {'host': 'localhost', 'port': 6397}


def test_read_environ(tmpdir):
    dst_env_yaml_path = tmpdir.join('config', 'environ.yaml')
    dst_env_yaml_path.write(open(env_yaml_path, 'rb').read(), ensure=True)
    conf = Config(tmpdir, files_path='files')

    assert conf.app_host == 'localhost'
    assert conf.app_port == 5555
    assert conf.archive == 'archive'
    assert conf.temp == tmpdir.join('files', 'temp')


def test_read_environ_without_files_dir(tmpdir):
    dst_env_yaml_path = tmpdir.join('config', 'environ.yaml')
    dst_env_yaml_path.write(open(env_yaml_path, 'rb').read(), ensure=True)

    with pytest.raises(ConfigError):
        conf = Config(tmpdir)


def test_variables(tmpdir):
    dst_variables_path = tmpdir.join('config', 'variables.py')
    dst_variables_path.write(open(variables_path, 'rb').read(), ensure=True)
    conf = Config(tmpdir, variables_path='variables.py')

    assert conf.date_time == date_time
    assert conf.time_delta == time_delta


def test_variables_no_conf_path(tmpdir):
    dst_variables_path = tmpdir.join('config', 'variables.py')
    dst_variables_path.write(open(variables_path, 'rb').read(), ensure=True)
    with pytest.raises(ConfigError):
        conf = Config(tmpdir, conf_path=None,
                      variables_path='variables.py')


@pytest.mark.parametrize('path', ['var.py', 'var/'], ids=['not-exist', 'dir'])
def test_variables_bad_names(tmpdir, path):
    with pytest.raises(ConfigError):
        conf = Config(tmpdir, variables_path=path)
