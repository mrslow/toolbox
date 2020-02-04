import os
import shutil


class LocalPath(os.PathLike):
    def __init__(self, path) -> None:
        self.path = os.path.normpath(path)

    def __fspath__(self) -> str:
        return str(self.path)

    def __hash__(self) -> int:
        return self.path.__hash__()

    def __str__(self) -> str:
        return self.path.__str__()

    def __eq__(self, other) -> bool:
        return self.path == other

    def __add__(self, path) -> os.PathLike:
        return self.path.__add__(path)

    def join(self, *paths) -> os.PathLike:
        return LocalPath(os.path.join(self.path, *paths))

    def listdir(self) -> list:
        return os.listdir(self.path)

    def move(self, dst) -> True:
        shutil.copy(self.path, dst)
        os.remove(self.path)
        return True

    def ensure_dir(self, *paths) -> os.PathLike:
        path = os.path.join(self.path, *paths)
        os.makedirs(path, exist_ok=True)
        return LocalPath(path)

    def remove(self) -> True:
        os.remove(self.path)
        return True

    def read(self, mode='rb') -> bytes:
        with open(self.path, mode) as file:
            return file.read()

    def write(self, data, mode='wb', ensure=False) -> os.PathLike:
        if ensure:
            head, tail = os.path.split(self.path)
            os.makedirs(head, exist_ok=True)
        with open(self.path, mode) as file:
            file.write(data)
        return self

    def encode(self, fmt) -> bytes:
        return self.path.encode(fmt)
