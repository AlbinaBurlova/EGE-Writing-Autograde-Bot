## Тестирование

Покрытие тестами составляет 97% (21 тест) - тестирование включает все хэндлеры телеграм-бота, исключением является файл инициализации bot.py и menu.py. Menu.py не покрывался тестами, поскольку он заключается в создании панели меню и реализуется в файле bot.py. 

### Coverage report

![image](https://github.com/AlbinaBurlova/EGE-Writing-Autograde-Bot/assets/117646051/739937aa-0982-433a-acd6-8298630551b7)

### Aiogram tests

В качестве инструмента тестирования была использована библиотека [aiogram_tests](https://github.com/OCCCAS/aiogram_tests), точнее её [улучшенная версия](https://github.com/Like6po/aiogram_tests/tree/master). Все авторские права остаются за создателями библиотеки. Для собственного удобства была добавлена функция, возвращающая последний запрос сессии бота:
```
    def get_last_request(self):
        return self._handler.bot.session.get_request()
```
