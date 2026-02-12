from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from database import register_user,login_user,connect_to_db, add_task, update_task, get_tasks, get_task,get_users, delete_task
from flask_cors import CORS
connect_to_db()
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'super-secter-key'
jwt = JWTManager(app)

# route for adding user, it creates password hash and store it into user
@app.route('/register', methods=['POST'])
def register_user_flask():
    if not request.is_json:
        return jsonify({'error': 'JSON input is required with email and password'}),400
    data = request.json
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    result = register_user(email, password)
    if result:
        return jsonify({'message': 'user created into db'}), 201
    return jsonify({'error': 'there is error adding user, try again later'}),500

#route for login of user, it creates access token and pass it back if login success
@app.route('/login', methods=['POST'])
def login_user_flask():
    if not request.is_json:
        return jsonify({'error': 'Json required with email and password'}),400
    data = request.json
    result = login_user(data.get('email'), data.get('password'))
    if result is None:
        return jsonify({'error': 'user not found'}),404
    if result:
        access_token = create_access_token(identity=data.get('email'))
        return jsonify({'message': 'login success', "token": access_token }),200
    return jsonify({'error': 'error occured while logging in user'}),500

#jwt protected route, it adds task for user... fetch email from jwt identity
@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task_user():
    if not request.is_json:
        return jsonify({'error': 'JSON is required as input'}),400
    data = request.json
    email = get_jwt_identity()
    result = add_task(email, data.get('title'))
    if result is None:
        return jsonify({'error': f'Error in fining user with {email}'}), 404
    if result == 1:
        return jsonify({'message': f'Task added for {email}'}),201
    return jsonify({'error': 'Error occured while adding task for user'}),500

#route to update task, gets email fro jwt
@app.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task_user(id):
    email = get_jwt_identity()
    result = update_task(email,id)
    if result == 1:
        return jsonify({'message': f'Task udated for {email}'}),200
    return jsonify({'error': 'Error occured while udating task for user'}),500

# to fetch tasks for logged in user
@app.route('/tasks')
@jwt_required()
def get_all_tasks():
    return jsonify(get_tasks(get_jwt_identity())),200

#fetch one task from jwt user
@app.route('/tasks/<int:id>')
@jwt_required()
def get_task_user(id):
    result = get_task(get_jwt_identity(), id)
    if result is None:
        return jsonify({'error': 'No task present with this ID'}),404
    return jsonify(result)

#to fetch all users
@app.route('/users')
def get_all_users():
    result = get_users()
    if result is None:
        return jsonify({'error': 'No users found'}),404
    return jsonify(result),200

#to delete task
@app.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task_user(id):
    result = delete_task(get_jwt_identity(), id)
    if result == 1:
        return jsonify({'message': 'task deleted'}),200
    return jsonify({'error': 'error in deleting task'}),500

#get info of logged in user
@app.route('/me')
@jwt_required()
def get_me():
    return jsonify({'you are': get_jwt_identity()})


if __name__ == '__main__':
    app.run(debug=True)
    