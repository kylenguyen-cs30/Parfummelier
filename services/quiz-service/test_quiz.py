import pytest
from flask import Flask
from app.routes import quiz_blueprint, user_notebanks

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(quiz_blueprint, url_prefix="/quiz")
    app.config["TESTING"] = True
    return app

def test_home(client):
    response = client.get("/quiz/")
    assert response.status_code == 200
    assert response.json == {"message": "Quiz Service launched"}

def test_submit_quiz_valid(client):
    answers = [
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
    response = client.post("/quiz/submit-quiz/", json={"answers": answers})
    assert response.status_code == 200
    assert "notebank" in response.json

def test_submit_quiz_invalid_length(client):
    answers = ["Reading a book in a cozy nook"] * 9  # Only 9 answers
    response = client.post("/quiz/submit-quiz/", json={"answers": answers})
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data is not None
    assert response_data["description"] == "Quiz must have exactly 10 answers."

def test_accord_note_data(client):
    # Test with a valid notebank
    notebank = ["Bergamot", "Lavender", "Patchouli"]
    response = client.post("/quiz/accord-note-data/", json={"notebank": notebank})
    assert response.status_code == 200
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert all(isinstance(item, str) for item in response_data)

def test_update_notebank_valid(client):
    initial_answers = [
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
    client.post("/quiz/submit-quiz/", json={"answers": initial_answers})

    updated_answers = [
        "A glass of rich red wine",
        "A refreshing mojito cocktail",
        "Sunrise, when the world feels fresh and quiet",
        "Mid-afternoon, when the sun is warm but not too hot",
        "Early evening, just before the stars come out",
        "Late at night, when everything feels calm",
        "A classic Italian pasta dish",
        "Spicy and flavorful Mexican food",
        "French pastries and delicate desserts",
        "Fresh and simple Japanese cuisine"
    ]
    response = client.put("/quiz/update-notebank/", json={"answers": updated_answers})
    assert response.status_code == 200
    assert "updated_notebank" in response.json

def test_update_notebank_invalid_length(client):
    answers = ["Reading a book in a cozy nook"] * 9  # Only 9 answers
    response = client.put("/quiz/update-notebank/", json={"answers": answers})
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data is not None
    assert response_data["description"] == "Quiz must have exactly 10 answers."
