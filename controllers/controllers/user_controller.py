from flask import Blueprint, request, jsonify
from models import db, User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # Create a JWT token for the user
        token= user.generate_token()
        print(token) # Debugging line to check the token do NOT include this in production code
        # Return the token to the client
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401