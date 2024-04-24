# QRkot_spreadseets — благотворительный фонд поддержки котиков QRKot с отчётом в Google Sheets.

Учебный проект в Практикуме сделал Мишустин Василий, v@vvvas.ru

Клонировать репозиторий и перейти в него в командной строке:

```
git clone  
cd QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv  
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать и заполнить файл .env по примеру .env.example

Создать таблицы в БД

```
alembic upgrade head
```

Запустить

```
uvicorn app.main:app --reload
```
