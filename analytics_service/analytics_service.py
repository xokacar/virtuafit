from flask import Flask, request, jsonify
import jwt
from functools import wraps
import datetime
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

@app.route('/analytics', methods=['GET'])
@token_required
def get_analytics(current_user):
    user_workouts = workouts.get(current_user, [])
    total_duration = sum(workout['duration'] for workout in user_workouts)
    workout_types = {}
    
    for workout in user_workouts:
        workout_types[workout['type']] = workout_types.get(workout['type'], 0) + 1
    
    return jsonify({
        'total_duration': total_duration,
        'workout_types': workout_types
    }), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
