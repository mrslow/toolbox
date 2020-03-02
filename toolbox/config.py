import os
import yaml
from types import ModuleType
from importlib.util import spec_from_file_location, module_from_spec
from toolbox import LocalPath


class Config(dict):
    def __init__(self,
                 proj_path,
                 conf_path='config',
                 files_path=None,
                 variables_path=None):
        self._set_paths(proj_path, conf_path, files_path)
        try:
            if conf_path is not None:
                self._read_database_conf()
                self._read_environment_conf()

            if variables_path is not None:
                self._read_variables(variables_path)
        except Exception as ex:
            raise ConfigError(ex)

    def __getattr__(self, name):
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __str__(self):
        return ''.join(f'{k} = {v}\n' for k, v in vars(self).items())

    def _set_paths(self, proj_path, conf_path, files_path):
        if os.path.isabs(proj_path):
            self.proj_path = LocalPath(proj_path)
        else:
            raise ConfigError('project path must be absolute')

        if conf_path is not None:
            self.conf_path = self._get_path(conf_path, self.proj_path)

        if files_path is not None:
            self.files_path = self._get_path(files_path, self.proj_path)

    def _get_path(self, path, root_path):
        if os.path.isabs(path):
            return LocalPath(path)
        else:
            return root_path.ensure_dir(path)

    def _load_yaml(self, yaml_path):
        return yaml.safe_load(yaml_path.read())

    def _read_database_conf(self):
        db_yaml_path = self.conf_path.join('database.yaml')
        if not db_yaml_path.exist():
            return

        db_yaml = self._load_yaml(db_yaml_path)

        self.db = db_yaml.get('database')
        self.redis = db_yaml.get('redis')

    def _read_environment_conf(self):
        env_yaml_path = self.conf_path.join('environ.yaml')
        if not env_yaml_path.exist():
            return

        env_yaml = self._load_yaml(env_yaml_path)

        directories = env_yaml.pop('directories', {})
        local_directories = directories.pop('local', {})
        self._define_dirs(directories, local_directories)

        for key in env_yaml:
            self.__setattr__(key, env_yaml[key])

    def _define_dirs(self, dirs, local_dirs):
        for key in dirs:
            self.__setattr__(key, LocalPath(dirs[key]))

        if local_dirs and not hasattr(self, 'files_path'):
            raise ConfigError('no directory for local files specified during '
                              'initialization, but directories specified '
                              'in configuration')

        for key in local_dirs:
            local_path = self.files_path.ensure_dir(local_dirs[key])
            self.__setattr__(key, self.files_path.ensure_dir(local_dirs[key]))

    def _read_variables(self, vars_path):
        module_path, module_name = self._get_module_data(vars_path)
        spec = spec_from_file_location(module_name, module_path)
        variables = module_from_spec(spec)
        spec.loader.exec_module(variables)

        for attr_name in vars(variables):
            value = getattr(variables, attr_name)

            if attr_name[:2] == '__':
                continue
            elif isinstance(value, (type, ModuleType)):
                continue

            self.__setattr__(attr_name, value)

    def _get_module_data(self, path):
        if not os.path.isabs(path):
            if not hasattr(self, 'conf_path'):
                raise ConfigError('no config directory for file with '
                                  'variables')
            path = os.path.join(self.conf_path, path)

        if not os.path.exists(path) or not os.path.isfile(path):
            raise ConfigError('variables file not exist')

        _, filename = os.path.split(path)
        return path, filename


class ConfigError(Exception):
    '''Exception class for Config'''
