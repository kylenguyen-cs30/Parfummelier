from flask import Flask
from app.routes import quiz_blueprint

def create_app():
    """Create and configure a Flask app for testing."""
    app = Flask(__name__)
    app.register_blueprint(quiz_blueprint, url_prefix='/')
    return app

def test_home():
    """Test the home route."""
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert b'Quiz Service launched' in response.data

def test_submit_quiz():
    """Test the quiz submission route."""
    app = create_app()
    client = app.test_client()

    quiz_data = {
        "answers": [
            "Reading a book in a cozy nook",
            "Watching your favorite series with a snack",
            "Meditating or practicing yoga",
            "Cooking up a new recipe",
            "Upbeat pop that makes you dance",
            "Classic rock with guitar riffs",
            "Soothing classical music",
            "Jazzy tunes with a laid-back vibe",
            "A freshly brewed cup of coffee",
            "A calming cup of herbal tea"
        ]
    }
    response = client.post('/submit-quiz/', json=quiz_data)
    assert response.status_code == 200
    assert b'Notebank created successfully' in response.data

def test_user_accords():
    """Test the user accords route."""
    app = create_app()
    client = app.test_client()

    # Submit quiz to create the notebank
    quiz_data = {
        "answers": [
            "Reading a book in a cozy nook",
            "Classic rock with guitar riffs",
            "A calming cup of herbal tea",
            "Mid-afternoon, when the sun is warm but not too hot",
            "Spicy and flavorful Mexican food",
            "Going to a live concert or music festival",
            "A colorful bird that sings all day",
            "Skiing in the snowy mountains",
            "Summer, with endless sunny days",
            "A mystery that keeps you on the edge of your seat"
        ]
    }
    client.post('/submit-quiz/', json=quiz_data)

    # Test retrieving accords
    response = client.get('/user-accords')
    assert response.status_code == 200
    
    # Print the accords data
    accords_data = response.get_json()
    print("Accords from /user-accords:", accords_data)

    assert 'accords' in accords_data

def test_accord_note_data():
    """Test the accord-note-data route."""
    app = create_app()
    client = app.test_client()

    response = client.get('/accord-note-data/')
    assert response.status_code == 200
    assert response.is_json
