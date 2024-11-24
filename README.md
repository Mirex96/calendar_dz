Шаг 7: Тестирование API

Можем использовать Postman или curl для тестирования.

Пример запроса на добавление события:

curl -X POST http://127.0.0.1:5000/api/v1/calendar/events \
-H 'Content-Type: application/json' \
-d '{
    "date": "2023-10-15",
    "title": "Встреча",
    "text": "Встреча с клиентом в офисе."
}'
Пример запроса на получение списка событий:

curl http://127.0.0.1:5000/api/v1/calendar/events
Пример запроса на получение события по ID:

curl http://127.0.0.1:5000/api/v1/calendar/events/1
Пример запроса на обновление события:

curl -X PUT http://127.0.0.1:5000/api/v1/calendar/events/1 \
-H 'Content-Type: application/json' \
-d '{
    "title": "Обновленная встреча",
    "text": "Перенос встречи на 16:00."
}'
Пример запроса на удаление события:

curl -X DELETE http://127.0.0.1:5000/api/v1/calendar/events/1
