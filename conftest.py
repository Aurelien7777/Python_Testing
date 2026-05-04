import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    # active le mode test de Flask
    app.config["TESTING"] = True
    # crée un faux navigateur
    with app.test_client() as client:
        # donne ce navigateur aux tests
        yield client


@pytest.fixture
def booking_test_data():
    club_test = {
        "name": "Test Club",
        "email": "test@test.com",
        "points": "20"
    }

    competition_test = {
        "name": "Test Competition",
        "date": "2026-10-10 10:00:00",
        "numberOfPlaces": "25"
    }

    clubs.append(club_test)
    competitions.append(competition_test)

    yield club_test, competition_test

    clubs.remove(club_test)
    competitions.remove(competition_test)