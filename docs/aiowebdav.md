# WebDavClient

### Пример использования

```python
from io import BytesIO
from toolbox import WebDavClient

# open session
wc = WebDavClient('localhost')

# upload
await wc.upload(BytesIO(b'Dummy'), '/dummy/text.txt')

# download
fileobj = BytesIO()
await wc.download('/dummy/test.txt', fileobj)
assert fileobj.getvalue() == b'Dummy'

# remove
await wc.delete('/dummy/test.txt')

# close session
await wc.close()
```

### Документация

_class_ toolbox.**WebDavClient**(host, port=80, loop=None)
* **host** (str) - хост вебдав сервера.
* **port** (int) - порт вебдав сервера.
* **loop** (asyncio.AbstractEventLoop) - event loop

---

**upload**(fileobj, remote_path)  
Сохраняет содержимое fileobj по укзанному в remote_path пути. 
* **fileobj** (BytesIO) - содержимое для записи
* **remote_path** (str) - путь, где будет записан файл

---

**download**(remote_path, fileobj)  
Получает содержимое файла по указанному в remote_path пути и помещает его в fileobj.
* **remote_path** (str) - путь к файлу, который надо получить
* **fileobj** (BytesIO) - полученное содержимое

---

**delete**(remote_path)  
Передает вебдав серверу команду на удаление файла или директории.
* **remote_path** (str) - путь к файлу, который будет удален

---

**close**()  
Закрывает соединение с вебдав сервером.
