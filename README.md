 Telegram-бота по поиску стоматологических клиник.
 ***
Используемые технологии:
- Python
- aiogram
- SQLite
- Яндекс API JavaScript и HTTP Геокодер
- Яндекс API Поиска по организациям 
***
Описание интерфейса пользователя:

Запуск Telegram-бота:

<img width="585" height="548" alt="image" src="https://github.com/user-attachments/assets/88490202-cc53-4757-a24a-9f63787af123" />

Раздел Местоположение:

<img width="691" height="356" alt="image" src="https://github.com/user-attachments/assets/fa5009a1-fbf9-4b3e-aed0-f2fb3af119d8" />

Раздел Поиск клиник:

<img width="723" height="277" alt="image" src="https://github.com/user-attachments/assets/4edbb160-f2fc-4af2-bf10-678772131755" />

Информация о выбранной клинике:

<img width="725" height="483" alt="image" src="https://github.com/user-attachments/assets/1c10d1ea-a720-485c-a680-d92a5a90de0b" />

Раздел Помощь:

<img width="719" height="350" alt="image" src="https://github.com/user-attachments/assets/cfb16c1d-b839-430d-9a52-91b87a42ce86" />

***
Файловая структура проекта:

| Название файла  | Содержание файла |
|----------------|-------------------|
| main.py | Точка входа, код запуска бота и инициализации всех остальных модулей|
| config.py | Файл со всеми конфигурационными параметрами |
| db.py | Функции подключения и работы с базой данных |
| text.py |  Все тексты, используемые ботом |
| kb.py |  Все клавиатуры, используемые ботом |
| handlers.py | Основной файл, состоящий из функций-обработчиков с декораторами (фильтрами) | 
