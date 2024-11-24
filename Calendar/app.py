from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Настройки приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Импорт моделей после инициализации db
#from models import Event

# Создание всех таблиц
with app.app_context():
    db.create_all()

# Маршруты API
# ...

if __name__ == '__main__':
    app.run(debug=True)




#                                 1. Добавление события (POST)

@app.route('/api/v1/calendar/events', methods=['POST'])
def create_event():
    data = request.get_json()

    # Проверка наличия всех полей
    if not data or not all(k in data for k in ('date', 'title', 'text')):
        return jsonify({'error': 'Invalid data'}), 400

    #  Длинна полей
    if len(data['title']) > 30:
        return jsonify({'error': 'Title length exceeds 30 characters'}), 400
    if len(data['text']) > 200:
        return jsonify({'error': 'Text length exceeds 200 characters'}), 400

    # Проверка формата даты
    try:
        event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Date format should be YYYY-MM-DD'}), 400

    # Проверка на существующее событие в эту дату
    if Event.query.filter_by(date=str(event_date)).first():
        return jsonify({'error': 'Event already exists on this date'}), 400

    # Создание события
    new_event = Event(
        date=str(event_date),
        title=data['title'],
        text=data['text']
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201


#                           2. Получение списка событий (GET)
@app.route('/api/v1/calendar/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200


#                            3. Чтение события по ID (GET)
@app.route('/api/v1/calendar/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.to_dict()), 200
    else:
        return jsonify({'error': 'Event not found'}), 404

#                             4. Обновление события (PUT)
@app.route('/api/v1/calendar/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Обновление даты
    if 'date' in data:
        try:
            event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            # Проверка на существующее событие с такой датой
            existing_event = Event.query.filter(Event.date == str(event_date), Event.id != event_id).first()
            if existing_event:
                return jsonify({'error': 'Another event exists on this date'}), 400
            event.date = str(event_date)
        except ValueError:
            return jsonify({'error': 'Date format should be YYYY-MM-DD'}), 400

    # Обновление заголовка
    if 'title' in data:
        if len(data['title']) > 30:
            return jsonify({'error': 'Title length exceeds 30 characters'}), 400
        event.title = data['title']

    # Обновление текста
    if 'text' in data:
        if len(data['text']) > 200:
            return jsonify({'error': 'Text length exceeds 200 characters'}), 400
        event.text = data['text']

    db.session.commit()
    return jsonify(event.to_dict()), 200

#                                     5. Удаление события (DELETE)
@app.route('/api/v1/calendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()
    return '', 204


