# # from flask import Blueprint, request, jsonify
# # from app import mongo
# # import bcrypt
# # from flask_jwt_extended import create_access_token
# # from datetime import timedelta

# # auth = Blueprint('auth', __name__)


# # @auth.route('/signup', methods=['POST'])
# # def signup():
# #     try:
# #         data = request.get_json()

# #         if not data
# #         return jsonify({"msg": "Missing JSON in request"}), 404

# #         email = data.get('email')
# #         password = data.get('password')
# #         name = data.get('name')

# #         if not email or not password:
# #             return jsonify({"error": "Missing email or password"}), 400

# #         existing_user = mongo.db.users.find_one({"email": email})
# #         if existing_user:
# #             return jsonify({"msg": "User already exist"}), 409

# #         hashed_password = bcrypt.hashpw(password.encode())


from flask import Blueprint, request, jsonify
from app import mongo
import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
# from flasgger import swag_from
from pprint import pprint


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
# @swag_from('docs/signup.yaml')
def signup():

    try:
        data = request.get_json()

        if not data:

            return jsonify({'msg': 'Missing JSON in request'}), 400

        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not email or not password:
            return jsonify({'error': 'Missing email and password'}), 401

        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            # response = {'error': 'User already exists'}
            # pprint(f"Signup error: {response}")
            return jsonify({"msg": "User already exists"}), 409

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            'email': email,
            'password': hashed_password,
            'name': name
        }

        result = mongo.db.users.insert_one(user_data)

        access_token = create_access_token(
            identity=email,
            expires_delta=timedelta(days=7)
        )
        return jsonify({
            'msg': 'User created successfully',
            # 'user_id': str(result.inserted_id),
            'access_token': access_token
        }), 201

    except Exception as e:
        # print(f"Error: {str(e)}")
        return jsonify({"msg": "Error during signup", "error": str(e)}), 500


@auth.route("/login", methods=["Post"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = mongo.db.users.find_one({'email': email})

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        access_token = create_access_token(
            identity=email,
            expires_delta=timedelta(days=7)
        )

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
