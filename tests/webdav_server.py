import os
from cheroot import wsgi
from wsgidav import util
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.dav_provider import DAVProvider
from wsgidav.fs_dav_provider import FolderResource, FileResource


class LocalWebdavServer:
    def __init__(self, root_path, host='localhost', port=28080, verbose=3):
        self.host = host
        self.port = port
        self.verbose = verbose
        self.root_path = root_path

    def get_app(self):
        config = {
            'provider_mapping': {'/': CustomDAVProvider(self.root_path)},
            'simple_dc': {'user_mapping': {'*': True}},
            'verbose': self.verbose,
        }
        return WsgiDAVApp(config)

    def get_server(self):
        app = self.get_app()
        return wsgi.Server(bind_addr=(self.host, self.port), wsgi_app=app)


class CustomDAVProvider(DAVProvider):

    def __init__(self, root_path):
        self.mount_path = ''
        self.readonly = False
        self.root_folder_path = root_path
        super().__init__()

    def _loc_to_file_path(self, path, environ):
        root_path = self.root_folder_path
        path_parts = path.strip("/").split("/")
        file_path = os.path.abspath(os.path.join(root_path, *path_parts))
        if not file_path.startswith(root_path):
            raise RuntimeError(f'Security exception: tried to access file '
                               f'outside root: {file_path}')

        file_path = util.to_unicode_safe(file_path)
        return file_path

    def get_resource_inst(self, path, environ):
        fp = self._loc_to_file_path(path, environ)
        if not os.path.exists(fp):
            if environ['REQUEST_METHOD'] == 'PUT':
                head, _ = os.path.split(fp)
                os.makedirs(head, exist_ok=True)
            return None

        if os.path.isdir(fp):
            return FolderResource(path, environ, fp)
        return FileResource(path, environ, fp)
