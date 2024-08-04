# Django проект, имитирующий интернет-магазин
## Установка:
1. Установить frontend пакет по инструкции: diploma-frontend/README.md
2. Установить зависимости с помощью команды: poetry install
3. Установить миграции для базы данных с помощью команды: python ./myshop/manage.py migrate
4. [Опционально] Загрузить fixture с тестовыми данными с помощью команды: python ./myshop/manage.py loaddata shopapp/fixtures/shopapp.json
5. Запустить проект с помощью команды: python ./myshop/manage.py runserver