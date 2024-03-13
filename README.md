Этап 1, Разворачивание проекта:

Запустите контейнер Django:

```docker-compose up```


После запуска откройте новый терминал и войдите в терминал докера командой: 

```docker-compose exec web bash```

Примените все миграции Django для создания необходимых таблиц базы данных:

```python manage.py migrate```


Запустите управляющую команду createsuperuser:

```python manage.py createsuperuser```


Следуйте инструкциям по вводу имени пользователя, адреса электронной почты и пароля для создания суперпользователя.

Теперь вы можете зайти на http://localhost:8000/admin
и добавить клиентов, продукты и покупки.

Этап 2, тестирование:

Получение списка всех продуктов:
http://127.0.0.1:8000/api/market/product

Получение продукта по id (пример с id = 1):
http://127.0.0.1:8000/api/market/product/get_product?pk=1

Создание покупки:

Перед тестированием создания покупки создайте клиента в панели админа.

Вывод списка всех продуктов (метод GET):

http://127.0.0.1:8000/api/market/purchase

Создание покупки (метод POST):

http://127.0.0.1:8000/api/market/purchase/

Пример того, как должно выглядеть body (формат json):
```{"client": 2, "product": 2}```

Получение Purchase по id:

http://127.0.0.1:8000/api/market/purchase/get_purchase?pk=1

Получение всех покупок клиента:

http://127.0.0.1:8000/api/market/purchase/client_purchase_with_product?client=1



ElasticSearch:

ETL процесс запускается с помощью cron каждый час, если вы не хотите ждать этого момента, то запустите в терминале докера:

```python manage.py transferproduct```

Получение продукта через elasticSearch по имени, описанию, цене:

http://127.0.0.1:8000/api/market/product/search/get_product

(если вы тестируете через Postman, то настройте параметры запроса, такие, как name, description, price)


