# Logger

### Пример использования

```python
from toolbox import Logger

logger = Logger('var/log/application', loglevel='INFO')

# registering logger named `access`. It includes FileHandler and StreamHandler 
logger.register('access', cout=True)

# registering logger named `operations`. It includes FileHandler only.
logger.register('operations')

# get access to logger
logger.access.info('INFO message')
logger.get('operations').warn('WARNING message')
```

### Документация

_class_ toolbox.**Logger**(logdir, loglevel='DEBUG')
* **logdir** (str) - путь к папке для хранения логов.
* **loglevel** (str) - уровень логирования.

---

**register**(name, cout=False)  
Регистрирует логгер. Автоматически добавляет ему FileHandler с именем name 
* **name** (str) - имя логгера. Файл лога будет иметь тоже названия, что и логгер только с расширением .log
* **cout** (bool) - флаг, отвечающий за необходимость вывода в консоль логируемых сообщений

---

**get**(name)  
Получет логгер с именем name. При невозможности найти логгер с указанным именем возбуждает исключение LoggerNotFound
* **name** (str) - имя логгера.
