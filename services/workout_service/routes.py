from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from sqlalchemy.orm import Session
from models import Workout
from database import SessionLocal
from config import Config
from elasticsearch_client import es 
import logging

workout_blueprint = Blueprint('workout', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@workout_blueprint.route('/workouts', methods=['POST'])
@token_required
def add_workout(current_user):
    session = SessionLocal()
    data = request.get_json()
    
    if not data or not data.get('workout_type') or not data.get('duration'):
        session.close()
        return jsonify({'message': 'Invalid input'}), 400
    
    new_workout = Workout(
        user=current_user,
        workout_type=data['workout_type'],
        duration=data['duration']
    )
    
    session.add(new_workout)
    session.commit()
    session.close()

    try:
        es.index(index='workout-entries', document={
            'username': current_user,
            'workout_type': data['workout_type'],
            'duration': data['duration'],
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        logging.debug("Successfully indexed workout data to Elasticsearch.")
    except Exception as e:
        logging.error(f"Error indexing workout data: {e}")

    return jsonify({'message': 'Workout added'}), 201


@workout_blueprint.route('/workouts', methods=['GET'])
@token_required
def get_workouts(current_user):
    session = SessionLocal()
    user_workouts = session.query(Workout).filter_by(user=current_user).all()
    
    workouts = [
        {'workout_type': workout.workout_type, 'duration': workout.duration, 'timestamp': workout.timestamp}
        for workout in user_workouts
    ]

    session.close()

    try:
        es.index(index='workout-retrievals', document={
            'username': current_user,
            'retrieval_timestamp': datetime.datetime.utcnow().isoformat(),
            'number_of_workouts': len(workouts)
        })
        logging.debug("Successfully indexed workout retrieval data to Elasticsearch.")
    except Exception as e:
        logging.error(f"Error indexing workout retrieval data: {e}")

    return jsonify({'workouts': workouts}), 200


@workout_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
