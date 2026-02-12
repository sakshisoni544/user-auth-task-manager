from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
from app.models import get_tasks_pagination, register_user,login_user, add_task, update_task, get_tasks, get_task,get_users, delete_task

def register_user_service(email,password):
    hash_password = generate_password_hash(password)
    user = register_user(email, hash_password)
    if user:
        return ({'status': True, "message": "User added","code": 200})
    return ({'status': False, "message": "User not added, some error occured","code": 500})

def login_user_service(email, password):
    user = login_user(email)
    if user is None:
        return {'status': None, 'message': 'user not found', 'code': 404}
    if check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return {'message': 'login success', "token": access_token, 'code': 200, 'status': True }
    return {'error': 'error occured while logging in user', 'code': 500, 'status': False}

def add_task_service(email, title):
    result = add_task(email, title)
    if result is None:
        return {'status': None, 'message': f'Error in finding user with {email}', 'code': 400}
    if result == 1:
        return {'message': f'Task added for {email}', 'status': True, 'code': 201}
    return {'message': 'Error occured while adding task for user', 'code': 500, 'status': False}

def update_task_service(email, id):
    result = update_task(email,id)
    if result is None:
        return {'status': None, 'message': f'Error in finding user with {email}', 'code': 400}
    if result == 1:
         return {'message': f'Task updated for {email}', 'status': True, 'code': 201}
    return {'message': 'Error occured while updating task for user', 'code': 500, 'status': False}

def get_tasks_service(email):
    result = get_tasks(email)
    if len(result):
        return {'tasks': result, 'status': True, 'code': 200}
    return {'tasks': result, 'status': False, 'code': 404}

def get_tasks_pagination_service(email, page, limit):
    result = get_tasks_pagination(email,page,limit)
    if len(result):
         return {'tasks': result, 'status': True, 'code': 200}
    return {'tasks': result, 'status': False, 'code': 404}


def get_task_service(email, id):
    result = get_task(email, id)
    if result is None:
        return {'message': 'No task present with this ID', 'status': None, 'code': 404}
    return {'task': result, 'status': True, 'code': 200}

def get_users_service():
    result = get_users()
    if result is None:
        return {'message': 'No users found', 'code': 404, 'status': None}
    return { 'users': result, 'code': 200, 'status': True}

def delete_task_service(email, id):
    result = delete_task(email, id)
    if result == 1:
        return {'message': 'task deleted', 'status': True, 'code': 200}
    return {'message': 'error in deleting task', 'code': 500, 'status': False}
