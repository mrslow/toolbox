# DBPool

### Пример использования

```python
from toolbox import DBPool

config = {
    'host': 'localhost',
    'user': 'postgres',
    'database': 'postgres'
}

# create a database connection pool
pool = DBPool(config, size=2)
await pool.create()

# execute a statement to create a new table
await pool.execute('CREATE TABLE users(id int, name text)')

# insert a record into the created table
await pool.execute('INSERT INTO users(id, name) VALUES($1, $2)', 1, 'Bob')

# select a row from the table
row = await pool.fetchrow('SELECT * FROM users WHERE name = $1', 'Bob')
# *row* now contains asyncpg.Record(id=1, name='Bob')

# close the connection
await conn.close()
```

### Документация

_class_ toolbox.**DBPool**(config, size=10)
* **config** (dict) - конфигурация для подключения к базе данных.
* **size** (int) - количество подключений в пуле.

---

**set_codec**(typename, *, schema='pg_catalog', format='text', encoder, decoder)  
Установка пары энкодер/декодер для специфической обработки указанного типа данных. ([Оригинальное описание](https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.Connection.set_type_codec))
* **typename** (str) - имя типа в базе для которого будет применяться обработка.
* **schema** (str) - имя схемы в которой определен тип.
* **format** (str) - тип данных передаваемый в декодер и возвращаемый энкодером.
* **encoder** (callable) - метод принимающий один аргумент и возвращающий "закодированное" значение.
* **decoder** (callable) - метод принимающий один аргумент и возвращающий "декодированное" значение.

---

_coroutine_ **create**()  
Создает пул подключений к базе.

---

_coroutine_ **close**()  
Закрывает все подключения к базе.

---

_coroutine_ **fetch**(query, *args, timeout=None)  
Выполняет запрос. В результате возвращает список (list) строк (asyncpg.Record).

_coroutine_ **fetchrow**(query, *args, timeout=None)  
Выполняет запрос. В результате возвращает одну строку (asyncpg.Record).

_coroutine_ **fetchval**(query, *args, timeout=None)  
Выполняет запрос. В результате возвращает значение, тип которого определен в [таблице конвертации](https://magicstack.github.io/asyncpg/current/usage.html#type-conversion).

_coroutine_ **execute**(query, *args, timeout=None)  
Выполняет команду(-ы). В результате возвращает строку (str) со статусом выполнения.

* **query** (str) - строка запроса.
* **args** (any) - аргументы подставляемые в строку запроса.
* **timeout** (int, float) - максимальное время, отведенное для выполнения запроса. Если за указанное время результат не получен, выполнение запроса будет прервано и возбуждено исключение "concurrent.futures.TimeoutError".

---

_coroutine_ **executemany**(query, args, timeout=None)  
Выполняет команду для каждого набора аргументов. Возвращает None.
* **query** (str) - строка запроса.
* **args** (list of tuples) - список кортежей с аргументами подставляемыми в строку запроса.
* **timeout** (int, float) - максимальное время, отведенное для выполнения запроса. Если за указанное время результат не получен, выполнение запроса будет прервано и возбуждено исключение "concurrent.futures.TimeoutError".
