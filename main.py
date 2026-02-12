from flask import Flask,jsonify
from flask_cors import CORS
from app.routes import register_routes
from config import Config
from flask_jwt_extended import JWTManager
from app.models import connect_to_db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
JWTManager(app)

with app.app_context():
    connect_to_db()

register_routes(app)    

@app.errorhandler(Exception)
def handleError(e):
    return jsonify({'app_error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


