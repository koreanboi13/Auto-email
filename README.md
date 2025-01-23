# Автоматизация отправки email

## Описание

Данный проект предназначен для автоматизации процесса отправки музыкальных битов артистам с использованием электронной почты и Telegram-бота. Он состоит из трех скриптов:

1. **send.py** - Отправляет биты артистам по электронной почте с использованием данных из Excel-файла.
2. **bot.py** - Telegram-бот для управления битами и взаимодействия с пользователем.
3. **clear.py** - Очистка папки с битами.

## Как работает проект

### 1. **send.py**
- Отправляет файлы из указанной папки (максимальный размер файла - 25 МБ) артистам, чьи email-адреса указаны в файле `artists.xlsx`.
- Работает в двух режимах:
  - Отправка битов только артистам со статусом "ждет".
  - Отправка битов только артистам, которым уже отправляли.
- Логины и пароли для почты хранятся в файле `sender.txt`.
- Тексты писем для отправки задаются в файлах `text_single.txt` и `text_multiple.txt`.

### 2. **bot.py**
- Telegram-бот для управления отправкой битов и очисткой папки с битами.
- Возможности:
  - Добавление битов через Telegram.
  - Отправка битов артистам, которым уже отправляли.
  - Отправка битов новым артистам.
  - Очистка папки с битами.

### 3. **clear.py**
- Удаляет все файлы из папки, указанной в файле `path.txt`.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/project-name.git
2. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте и настройте следующие файлы:
   - **`sender.txt`** - Укажите email и пароль отправителя:
     ```
     your_email@gmail.com
     your_password
     ```
   - **`path.txt`** - Укажите путь к папке с битами:
     ```
     /path/to/beats
     ```
   - **`text_single.txt`** и **`text_multiple.txt`** - Укажите заголовок и текст письма.
   - **`token.txt`** - Укажите токен вашего Telegram-бота.

4. Создайте папку для хранения битов:
   ```bash
   mkdir beats
   ```

5. Убедитесь, что в папке находится файл `artists.xlsx` с данными артистов.

## Использование

### Запуск Telegram-бота
1. Запустите бот:
   ```bash
   python bot.py
   ```
2. В Telegram отправьте команду `/start`, чтобы начать работу.

### Отправка писем через `send.py`
- Для отправки только новым артистам:
  ```bash
  python send.py 1
  ```
- Для отправки только артистам, которым уже отправляли:
  ```bash
  python send.py 2
  ```

### Очистка папки с битами
1. Запустите `clear.py`:
   ```bash
   python clear.py
   ```

## Примечания
- Убедитесь, что SMTP-доступ разрешен для указанной почты.
- Telegram-бот автоматически создаст папку `beats`, если она отсутствует.
- Excel-файл `artists.xlsx` должен содержать:
  - Email-адреса артистов в колонке `F`.
  - Статус в колонке `H` (например, "ждет" или "отправил биты").
