from flask import jsonify, request
from app.services import get_tasks_pagination_service, delete_task_service,get_users_service, register_user_service, login_user_service, add_task_service, update_task_service, get_tasks_service, get_task_service
from flask_jwt_extended import get_jwt_identity, jwt_required

def register_routes(app):
    # route for adding user, it creates password hash and store it into user
    @app.route('/register', methods=['POST'])
    def register_route():
     if not request.is_json:
        return jsonify({'error': 'JSON input is required with email and password'}),400
     data = request.json
     result = register_user_service(data.get('email'), data.get('password'))
     if result['status']:
        return jsonify({'message': result['message']}), result['code']
     return  jsonify({'error': result['message']}), result['code']
    
    #route for login of user, it creates access token and pass it back if login success
    @app.route('/login', methods=['POST'])
    def login_user_flask():
     if not request.is_json:
        return jsonify({'error': 'Json required with email and password'}),400
     data = request.json
     result = login_user_service(data.get('email'), data.get('password'))
     if result['status'] is None:
        return jsonify({'error': result['message']}),result['code']
     if result['status']:
        return jsonify({'message': result['message'], "token": result['token'] }), result['code']
     return jsonify({'error': result['message']}),result['code']    
    

    #jwt protected route, it adds task for user... fetch email from jwt identity
    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def add_task_user():
     if not request.is_json:
        return jsonify({'error': 'JSON is required as input'}),400
     data = request.json
     result = add_task_service(get_jwt_identity(), data.get('title'))
     if result['status'] is None:
        return jsonify({'error': result['message']}), result['code']
     if result['status']:
        return jsonify({'message': result['message']}), result['code']
     return jsonify({'error': result['message']}),result['code']
    
    #route to update task, gets email fro jwt  
    @app.route('/tasks/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_task_user(id):
     result = update_task_service(get_jwt_identity(),id)
     if result['status']:
        return jsonify({'message': result['message']}), result['code']
     return jsonify({'error': result['message']}),result['code']
    
    # to fetch tasks for logged in user
    @app.route('/tasks/all')
    @jwt_required()
    def get_all_tasks():
     result = get_tasks_service(get_jwt_identity())
     return jsonify({'tasks': result['tasks']}), result['code'] 
     
    @app.route('/tasks')
    @jwt_required()
    def get_all_tasks_p():
      page = request.args.get('page', 1, type=int)
      limit = request.args.get('limit', 5, type=int)
      result = get_tasks_pagination_service(get_jwt_identity(), page, limit)
      return jsonify({'tasks': result['tasks']}), 200
    
    #fetch one task from jwt user
    @app.route('/tasks/<int:id>')
    @jwt_required()
    def get_task_user(id):
     result = get_task_service(get_jwt_identity(), id)
     if result['status'] is None:
         return jsonify({'error': result['message']}), result['code']
     return jsonify(result['task']), result['code']
    
    #to fetch all users
    @app.route('/users')
    def get_all_users():
     result = get_users_service()
     if result['status'] is None:
        return jsonify({'error': result['message']}), result['code']
     return jsonify({'users': result['users']}), result['code']
    
    #to delete task
    @app.route('/tasks/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_task_user(id):
     result = delete_task_service(get_jwt_identity(), id)
     if result['status']:
        return jsonify({'message': result['message']}), result['code']
     return jsonify({'error': result['message']}), result['code']
    
    #get info of logged in user
    @app.route('/me')
    @jwt_required()
    def get_me():
     return jsonify({'you are': get_jwt_identity()})