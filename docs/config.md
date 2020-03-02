# Config

### Пример использования

database.yaml
```yaml
database:
    test_db:
        host: localhost
        user: postgres
        database: postgres
#     test_db_2:
#         host: localhost
#         ...
# 
# redis:
#     host: localhost
#     port: 6397
```

environ.yaml
```yaml
app_host: localhost
app_port: 5555

directories:
    local:
        temp_dir: temp
    arch: archive
```

vars.py
```python
from datetime import datetme

date_time = datetime(2020, 1, 1)
```

main.py
```python
from toolbox import Config

conf = Config('/absolute/proj/path',
              conf_path='relative/config',
              files_path='/absolute/files',
              variables_path='vars.py')
conf.test_var = 42

print(conf)
proj_path = /absolute/proj/path  # LocalPath
conf_path = /absolute/proj/path/relative/conf  # LocalPath
files_path = /absolute/files  # LocalPath
db = {'test_db': {'host': 'localhost', 'user': 'postgres', 'database': 'test_db'}}  # dict
redis = None  # None
temp_dir = /absolute/files/temp  # LocalPath
arch = archive  # LocalPath
app_host = localhost  # str
app_port = 5555  # int
date_time = 2020-01-01 00:00:00  # datetime
test_var = 42  # int

print(conf.test_var, conf['test_var'])
42 42

conf.test_var == conf['test_var']
True

print(conf.db['test_db'])
{'host': 'localhost', 'user': 'postgres', 'database': 'test_db'}
```

### Документация

_class_ toolbox.**Config**(proj_path,
                           conf_path='config',
                           files_path=None,
                           variables_path=None)
* **proj_path** (str, os.PathLike) - абсолютный путь до корневой директории проекта.
* **conf_path** (str, os.PathLike) - абсолютный или относительный путь до директории с yaml-конфигами.
* **files_path** (str, os.PathLike) - абсолютный или относительный путь до локальной директории для хранения файлов.
* **variables_path** (str, os.PathLike) - абсолютный или относительный путь до python-файла с переменными.

#### Особенности работы с конфигом.

* Все проинициализированные переменные не защищены от перезаписи.
* Есть возможность указать переменную после инициализации конфига.
* Чтение/запись переменных осуществляется как через атрибут, так и по ключу (см. пример выше). Регистр учитывается. Если читаемой переменной нет, вернется AttributeError.
* Если аргументы files_path или conf_path содержат отновительные пути, то их путь присоединяется к proj_path.
* Если аргумент variables_path содержит относительный путь, то его путь присоединяется к conf_path.
* Аргумент conf_path является необязательным и если не указан, то yaml-конфиги читаться не будут. При этом если указан относительный variables_path, то будет возбуждено исключение.
* Если какого то yaml-конфига нет, он будет проигнорирован.
* Файл конфигурации подключений к БД должен иметь имя database.yaml, лежать в директории conf_path и иметь структуру как в примере выше.
* Файл с переменными окружения должен иметь имя environ.yaml и лежать в conf_path. Его структура произвольна за исключением блока directories. Пути/директории указанные в корне блока будут считаться абсолютными. Те пути/директори, что дополнительно вложены в блок local, считаются относительными и присоединяются к files_path. Если указан блок local, но не указан files_path, будет возбуждено исключение.
* Все пути (proj_path, conf_path, files_path и все пути из блока directories файла environ.yaml) являются экземплярами класса [LocalPath](localpath.md).
* Из файла с переменным (variables_path), читается всё, кроме импортированных в нём модулей и переменных начинающихся с двух нижних подчеркиваний "__". Импортированные таким образом переменные имеют тип как в исходном файле.
* Путь variables_path не хранится в экземпляре класса Config.
