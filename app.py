from flask import Flask, send_from_directory
from config import db, migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/users/*": {"origins": "*"}}, supports_credentials=True)  

app.config['JWT_SECRET_KEY'] = 'qwertyuiop'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

from routes.user import user_bp
app.register_blueprint(user_bp, url_prefix='/users')

# Configuración Swagger UI
SWAGGER_URL = '/apidocs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={
        'app_name': "Mi API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
