from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from sqlalchemy.orm import Session
from models import Workout
from database import SessionLocal
from config import Config

analytics_blueprint = Blueprint('analytics', __name__)


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


@analytics_blueprint.route('/analyticsdata', methods=['GET'])
@token_required
def get_analytics(current_user):
    session = SessionLocal()
    user_workouts = session.query(Workout).filter_by(user=current_user).all()
    
    total_duration = sum(workout.duration for workout in user_workouts)
    workout_types = {}

    for workout in user_workouts:
        workout_types[workout.workout_type] = workout_types.get(workout.workout_type, 0) + 1

    session.close()

    return jsonify({
        'total_duration': total_duration,
        'workout_types': workout_types
    }), 200


@analytics_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200