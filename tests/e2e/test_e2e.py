import pytest
import requests

BASE_URL = "http://34.77.94.55"  # Replace with your NGINX External IP

@pytest.fixture(scope="session")
def get_token():
    """Authenticate and return the token for other tests."""
    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    assert response.status_code == 200, "Failed to log in"
    return response.json().get("token")


def test_auth_service_health():
    """Check health of the auth service."""
    url = f"{BASE_URL}/auth/health"
    response = requests.get(url)
    
    assert response.status_code == 200, "Auth service health check failed"
    assert response.json().get("status") == "ok", "Unexpected health check response"


def test_analytics_service_health():
    """Check health of the analytics service."""
    url = f"{BASE_URL}/analytics/health"
    response = requests.get(url)
    
    assert response.status_code == 200, "Analytics service health check failed"
    assert response.json().get("status") == "ok", "Unexpected health check response"


def test_workout_service_health():
    """Check health of the workout service."""
    url = f"{BASE_URL}/workout/health"
    response = requests.get(url)
    
    assert response.status_code == 200, "Workout service health check failed"
    assert response.json().get("status") == "ok", "Unexpected health check response"


def test_user_registration():
    """Test user registration."""
    url = f"{BASE_URL}/auth/register"
    response = requests.post(url, json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    if response.status_code == 400:
        assert response.json().get("message") == "User already exists", "Unexpected error message"
    else:
        assert response.status_code == 201, "User registration failed"
        assert response.json().get("message") == "User registered successfully", "Unexpected success message"


def test_user_login(get_token):
    """Test login functionality."""
    assert get_token is not None, "Failed to retrieve token"


def test_add_workout(get_token):
    """Test adding a workout."""
    url = f"{BASE_URL}/workout/workouts"
    headers = {"x-access-token": get_token}
    
    response = requests.post(url, json={
        "workout_type": "Running",
        "duration": 30
    }, headers=headers)
    
    assert response.status_code == 201, "Failed to add workout"
    assert response.json().get("message") == "Workout added", "Unexpected response message"


def test_get_workouts(get_token):
    """Test retrieving workouts for the logged-in user."""
    url = f"{BASE_URL}/workout/workouts"
    headers = {"x-access-token": get_token}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, "Failed to retrieve workouts"
    workouts = response.json().get("workouts")
    
    assert isinstance(workouts, list), "Workouts response is not a list"
    assert len(workouts) > 0, "No workouts returned"
    assert "workout_type" in workouts[0], "Workout data does not have 'workout_type'"
    assert "duration" in workouts[0], "Workout data does not have 'duration'"


def test_analytics_data(get_token):
    """Test retrieving analytics data."""
    url = f"{BASE_URL}/analytics/analyticsdata"
    headers = {"x-access-token": get_token}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, "Failed to retrieve analytics data"
    analytics_data = response.json()
    
    assert "total_duration" in analytics_data, "Analytics data does not have 'total_duration'"
    assert "workout_types" in analytics_data, "Analytics data does not have 'workout_types'"
