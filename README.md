# Обрезка ссылок с помощью Битли

Обрезка ссылок при помощи Битли.

### Как установить

Зарегистрируйте ключ на сайте [Bitly](https://app.bitly.com/BlcngOTTfaY/bitlinks/3roypfS), ключ класть в файл .env , пример ключа: 159552b56ac5c79528d7b6abf93797230011c82f .

Пример файла .env
```
BITLY_TOKEN=159552b56ac5c79528d7b6abf93797230011c82f
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример работы скрипта в случае штатной ситуации:
Откройте командную строку.
Если хотите сократить ссылку, то запустите программу и введите свою ссылку. (Ссылка является аргументом при запуске скрипта)
```
python main.py http://dvmn.org/modules/web-api/lesson/bitly/#3
bit.ly/3fa6jy6
```
Если хотите получить количество кликов по скоращенной ссылке, то запустите программу и введите сокращенную ссылку.
```
python main.py bit.ly/3fa6jy6
1
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
