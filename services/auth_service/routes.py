from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
import jwt
import datetime
from config import Config
from elasticsearch_client import es  
import logging

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    session = SessionLocal()
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400
    
    username = data['username']
    existing_user = session.query(User).filter_by(username=username).first()
    
    if existing_user:
        session.close()
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=username, password_hash=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.close()

    try:
        es.index(index='user-registrations', document={
            'username': username,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        logging.debug("Successfully indexed registration data to Elasticsearch.")
    except Exception as e:
        logging.error(f"Error indexing registration data: {e}")

    return jsonify({'message': 'User registered successfully'}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    session = SessionLocal()
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        session.close()
        return jsonify({'message': 'Invalid input'}), 400

    user = session.query(User).filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        session.close()
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, Config.SECRET_KEY)
    
    session.close()
    
    try:
        es.index(index='user-logins', document={
            'username': data['username'],
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        logging.debug("Successfully indexed login data to Elasticsearch.")
    except Exception as e:
        logging.error(f"Error indexing login data: {e}")

    return jsonify({'token': token})

@auth_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
