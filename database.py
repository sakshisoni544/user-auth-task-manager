import sqlite3
from werkzeug.security import check_password_hash

connection = None
cursor = None

def connect_to_db():
    global connection, cursor
    connection = sqlite3.connect('user-tasks.db',check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('create table if not exists users (id integer primary key autoincrement, email text unique, password text)')
    cursor.execute('create table if not exists tasks (id integer primary key autoincrement, user_id integer, title text, completed integer)')

    
def register_user(email, password):
        try:
         cursor.execute('insert into users(email, password) values(?, ?)', (email, password))
         connection.commit()
         return True
        except: 
            return False
    

def login_user(email, password):
    cursor.execute('select password from users where email = ?', (email,))
    row = cursor.fetchone()
    if not row:
        return None
    if check_password_hash(row[0], password):
        return True
    return False   

def add_task(email, title, completed = 0):
    id = get_user_id(email)
    cursor.execute('insert into tasks(user_id, title, completed) values(?, ?, ?)', (id, title, completed))
    connection.commit()
    return cursor.rowcount

def update_task(email,task_id):
    user_id = get_user_id(email)
    cursor.execute('update tasks set completed = 1 where id = ? and user_id = ?', (task_id,user_id))
    connection.commit()
    return cursor.rowcount

def get_user_id(email):
    cursor.execute('select id from users where email = ?', (email, ))
    row = cursor.fetchone()
    if row is None:
        return None
    return row[0]

def get_tasks(email):
    user_id = get_user_id(email)
    tasks= []
    try:
        for data in cursor.execute('select * from tasks where user_id = ?', (user_id,)):
            tasks.append({'id': data[0], "user_id": data[1], "title": data[2], 'completed': data[3] })
        return tasks
    except:
        return []   
    
def get_task(email, id):
    user_id = get_user_id(email)
    cursor.execute('select * from tasks where id = ? and user_id = ?', (id,user_id))
    data = cursor.fetchone()
    if data is None:
        return None
    return ({'id': data[0], "user_id": data[1], "title": data[2], 'completed': data[3] })   

def get_users():
    users = []
    try:
        for data in cursor.execute('select * from users'):
            users.append({"id": data[0], "email": data[1]})
        return users   
    except:
        return [] 
    
def delete_task(email, id):
    user_id = get_user_id(email)
    cursor.execute('delete from tasks where id = ? and user_id = ?', (id,user_id))
    connection.commit()
    return cursor.rowcount    


