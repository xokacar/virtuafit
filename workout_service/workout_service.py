from flask import Flask, request, jsonify
import jwt
from functools import wraps
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

workouts = {}  

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/workouts', methods=['POST'])
@token_required
def add_workout(current_user):
    data = request.get_json()
    if not data or not data.get('workout_type') or not data.get('duration'):
        return jsonify({'message': 'Invalid input'}), 400
    
    workout = {
        'type': data['workout_type'],
        'duration': data['duration'],
        'timestamp': datetime.datetime.utcnow()
    }
    
    if current_user not in workouts:
        workouts[current_user] = []
    workouts[current_user].append(workout)
    
    return jsonify({'message': 'Workout added'}), 201

@app.route('/workouts', methods=['GET'])
@token_required
def get_workouts(current_user):
    user_workouts = workouts.get(current_user, [])
    return jsonify({'workouts': user_workouts}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
