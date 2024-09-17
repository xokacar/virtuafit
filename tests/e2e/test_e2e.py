import pytest
import requests

# Define both base URLs
BASE_URLS = [
    "http://34.77.94.55",      # NGINX External IP
    "http://34.107.208.185"    # Google Cloud Load Balancer IP
]

@pytest.fixture(scope="session", params=BASE_URLS)
def base_url(request):
    """Provide base URL for tests, parameterized over multiple endpoints."""
    return request.param

@pytest.fixture(scope="session")
def get_token(base_url):
    """Authenticate and return the token for other tests."""

    username = "testuser001"
    password = "testpassword001"
    

    register_url = f"{base_url}/auth/register"
    registration_response = requests.post(register_url, json={
        "username": username,
        "password": password
    })
    
    if registration_response.status_code == 201:
        print(f"User registered successfully on {base_url}.")
    elif registration_response.status_code == 400:

        print(f"User already exists on {base_url}.")
    else:
        raise Exception(f"Failed to register user on {base_url}: {registration_response.text}")
    

    login_url = f"{base_url}/auth/login"
    login_response = requests.post(login_url, json={
        "username": username,
        "password": password
    })
    
    if login_response.status_code != 200:
        raise AssertionError(f"Failed to log in on {base_url}: {login_response.text}")
    
    token = login_response.json().get("token")
    if not token:
        raise AssertionError(f"Token not found in login response on {base_url}.")
    
    return token

def test_auth_service_health(base_url):
    """Check health of the auth service."""
    url = f"{base_url}/auth/health"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Auth service health check failed on {base_url}: {response.text}"
    assert response.json().get("status") == "ok", "Unexpected health check response"

def test_analytics_service_health(base_url):
    """Check health of the analytics service."""
    url = f"{base_url}/analytics/health"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Analytics service health check failed on {base_url}: {response.text}"
    assert response.json().get("status") == "ok", "Unexpected health check response"

def test_workout_service_health(base_url):
    """Check health of the workout service."""
    url = f"{base_url}/workout/health"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Workout service health check failed on {base_url}: {response.text}"
    assert response.json().get("status") == "ok", "Unexpected health check response"

def test_user_registration(base_url):
    """Test user registration."""
    url = f"{base_url}/auth/register"
    response = requests.post(url, json={
        "username": "testuser001",    
        "password": "testpassword001" 
    })
    
    if response.status_code == 400:
        assert response.json().get("message") == "User already exists", f"Unexpected error message on {base_url}: {response.text}"
    else:
        assert response.status_code == 201, f"User registration failed on {base_url}: {response.text}"
        assert response.json().get("message") == "User registered successfully", f"Unexpected success message on {base_url}: {response.text}"

def test_user_login(get_token, base_url):
    """Test login functionality."""
    assert get_token is not None, f"Failed to retrieve token on {base_url}"

def test_add_workout(get_token, base_url):
    """Test adding a workout."""
    url = f"{base_url}/workout/workouts"
    headers = {"x-access-token": get_token}
    
    response = requests.post(url, json={
        "workout_type": "Running",
        "duration": 30
    }, headers=headers)
    
    assert response.status_code == 201, f"Failed to add workout on {base_url}: {response.text}"
    assert response.json().get("message") == "Workout added", f"Unexpected response message on {base_url}: {response.text}"

def test_get_workouts(get_token, base_url):
    """Test retrieving workouts for the logged-in user."""
    url = f"{base_url}/workout/workouts"
    headers = {"x-access-token": get_token}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, f"Failed to retrieve workouts on {base_url}: {response.text}"
    workouts = response.json().get("workouts")
    
    assert isinstance(workouts, list), f"Workouts response is not a list on {base_url}"
    assert len(workouts) > 0, f"No workouts returned on {base_url}"
    assert "workout_type" in workouts[0], f"Workout data does not have 'workout_type' on {base_url}"
    assert "duration" in workouts[0], f"Workout data does not have 'duration' on {base_url}"

def test_analytics_data(get_token, base_url):
    """Test retrieving analytics data."""
    url = f"{base_url}/analytics/analyticsdata"
    headers = {"x-access-token": get_token}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, f"Failed to retrieve analytics data on {base_url}: {response.text}"
    analytics_data = response.json()
    
    assert "total_duration" in analytics_data, f"Analytics data does not have 'total_duration' on {base_url}"
    assert "workout_types" in analytics_data, f"Analytics data does not have 'workout_types' on {base_url}"
