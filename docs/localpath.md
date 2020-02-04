# LocalPath

### Класс
> _class_ toolbox.**LocalPath**(path)
* **path** (str, os.PathLike) - путь до директории или файла.

### Методы
> **join**(*args)

Объединяет исходный путь со всеми принятыми аргументами. Возвращает новый LocalPath.

> **ensure_dir**(*args)

Объединяет исходный путь со всеми принятыми аргументами. создавая все несуществующие директории. Возвращает новый LocalPath.

> **write**(data, mode='wb', ensure=False)

Записывает принятое содержимое по пути назначения в файл. Возвращает себя (LocalPath).
* mode (str) - определяет тип записываемых данных. _rb_ - bytestring, _r_ - str.
* ensure (bool) - определяет будут ли созданы отсутствующие директории по пути назначения.

> **read**(mode='rb')

Читает и возвращает содержимое по пути назначения.
* mode (str) - определяет тип возвращаемых данных. _rb_ - bytestring, _r_ - str.

> **move**(path)

Перемещает объект по пути назначения.

> **remove**()

Удаляет объект по пути назначения.

> **encode**(fmt)

Возвращает путь в указанной кодировке.

> **listdir**()

Возвращает список содержимого директории.

### Пример использования
path = **LocalPath**('/root/path')  
path.**join**('new', 'dir', 'filename.txt).**write**('text', _mode_='w', _ensure_=True)