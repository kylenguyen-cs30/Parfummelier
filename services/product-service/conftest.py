import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Configure app with testing and in-memory database settings
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory SQLite database
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()  # Initialize tables
        yield app
        db.session.remove()
        db.drop_all()  # Cleanup after tests

@pytest.fixture
def client(app):
    return app.test_client()
