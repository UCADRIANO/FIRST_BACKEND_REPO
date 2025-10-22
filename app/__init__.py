# from flask import Flask
# from flask_pymongo import PyMongo
# from dotenv import load_dotenv
# from flask_jwt_extended import JWTManager
# import os

# load_dotenv()

# mongo = PyMongo()
# jwt = JWTManager()


# def create_app():
#     flask_app = Flask(__name__)

#     flask_app.config['MONGO_URI'] = os.getenv('MONGO_URI')
#     flask_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

#     @flask_app.route("/")
#     def home():
#         return "Hellow, World!"

#     mongo.init_app(flask_app)
#     jwt.init_app(flask_app)

#     # Check mongo db connection

#     try:
#         with flask_app.app_context():
#             mongo.db.command('ping')
#             print("Conneded to MongoDB")
#     except Exception as e:
#         print("Error connecting to MongoDB:", e)

#         from .auth import auth as auth_blueprint
#         flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')

#     return flask_app

from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    flask_app = Flask(__name__)

    flask_app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    flask_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    CORS(flask_app, origins=["*"])

    @flask_app.route("/")
    def home():
        return "Hello, World!"

    # Initialize extensions
    mongo.init_app(flask_app)
    jwt.init_app(flask_app)

    from app.auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')


    # Test MongoDB connection
    try:
        with flask_app.app_context():
            mongo.db.command('ping')
            print("\n✅ MongoDB connected successfully!\n")
    except Exception as e:
        print(f"\n❌ MongoDB connection failed: {e}\n")

    # Register blueprints
    # from .main import main as main_blueprint
    # from .auth import auth as auth_blueprint

    # flask_app.register_blueprint(main_blueprint)
    # flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return flask_app


app = create_app()
