from flask import Flask, request, jsonify
from models import db, User, Task
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    elif request.method == 'PUT':
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'user_id': task.user_id} for task in tasks])
    elif request.method == 'POST':
        data = request.get_json()
        new_task = Task(title=data['title'], description=data['description'], user_id=data['user_id'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'user_id': new_task.user_id}), 201

@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'user_id': task.user_id})
    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        task.user_id = data['user_id']
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'user_id': task.user_id})
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
