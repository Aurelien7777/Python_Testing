def test_show_summary_then_points_page(client, booking_test_data):
    club_test, competition_test = booking_test_data

    response = client.post("/showSummary", data={"email": club_test["email"]})

    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = client.get("/points")

    assert response.status_code == 200
    assert club_test["name"].encode() in response.data
    assert str(club_test["points"]).encode() in response.data


def test_show_summary_with_unknown_email(client):
    response = client.post(
        "/showSummary", data={"email": "unknown@test.com"}, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Sorry, that email was not found" in response.data


def test_purchase_places_with_valid_number_of_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Iron Temple", "places": "2"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data


def test_purchase_places_with_too_many_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not authorized to book this number of places" in response.data


def test_book_less_or_12_places(client, booking_test_data):

    club_test, competition_test = booking_test_data

    places_before = int(competition_test["numberOfPlaces"])
    places_required = 12

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert competition_test["numberOfPlaces"] == places_before - places_required


def test_book_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13",
        },
    )

    assert response.status_code == 200
    assert (
        b"You are not authorized to book more than 12 places per competition!"
        in response.data
    )


def test_book_valid_competition(client, booking_test_data):
    club_test, competition_test = booking_test_data

    response = client.get(
        f'/book/{competition_test["name"]}/{club_test["name"]}', follow_redirects=True
    )

    assert response.status_code == 200
    assert b"How many places?" in response.data


def test_book_in_past_competition(client):

    response = client.get(
        "/book/Spring%20Festival/Iron%20Temple", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"You cannot book places for a past competition" in response.data


def test_club_points_are_deducted_after_booking(client, booking_test_data):
    club_test, competition_test = booking_test_data

    points_before = int(club_test["points"])
    places_required = 12

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Test Competition",
            "club": "Test Club",
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert club_test["points"] == points_before - places_required


def test_display_list_of_club_and_their_current_point(client, booking_test_data):
    club_test, competition_test = booking_test_data

    points_club = int(club_test["points"])
    name_club = club_test["name"]

    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})

    assert response.status_code == 200
    assert name_club.encode() in response.data
    assert str(points_club).encode() in response.data


def test_booking_egal_or_less_places_than_available(client, booking_test_data):

    club_test, competition_test = booking_test_data
    places_required = 12
    places_competition = 12
    competition_test["numberOfPlaces"] = places_competition

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert places_competition - places_required >= 0
    assert b"Great-booking complete!" in response.data
    assert (
        b"You are not authorized to book more than available places!"
        not in response.data
    )
    assert competition_test["numberOfPlaces"] == places_competition - places_required


def test_booking_more_places_than_available(client, booking_test_data):

    club_test, competition_test = booking_test_data
    places_required = 12
    places_competition = 11
    competition_test["numberOfPlaces"] = places_competition

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert places_competition - places_required < 0
    assert (
        b"You are not authorized to book more than available places!" in response.data
    )
    assert b"Great-booking complete!" not in response.data
    assert int(competition_test["numberOfPlaces"]) == places_competition


def test_book_less_than_0_place(client, booking_test_data):
    club_test, competition_test = booking_test_data

    place_required = -1
    place_before = int(competition_test["numberOfPlaces"])
    points_before = int(club_test["points"])

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": str(place_required),
        },
    )

    assert response.status_code == 200
    assert place_before == int((competition_test["numberOfPlaces"]))
    assert points_before == int(club_test["points"])
    assert b"You must book at least 1 place" in response.data


def test_book_with_invalid_club(client, booking_test_data):
    club_test, competition_test = booking_test_data

    response = client.get(
        f"/book/{competition_test['name']}/Unknown Club", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_book_with_invalid_competition(client, booking_test_data):
    club_test, competition_test = booking_test_data

    response = client.get(
        f"/book/Unknown Competition/{club_test['name']}", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_purchase_places_with_non_numeric_value(client, booking_test_data):
    club_test, competition_test = booking_test_data

    points_before = int(club_test["points"])
    places_before = int(competition_test["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": "abc",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Please enter a valid number of places" in response.data
    assert int(club_test["points"]) == points_before
    assert int(competition_test["numberOfPlaces"]) == places_before
    

def test_complete_booking_workflow(client, booking_test_data):

    club_test, competition_test = booking_test_data

    points_before = int(club_test["points"])
    places_before = int(competition_test["numberOfPlaces"])
    places_required = 5

    response = client.post(
        "/showSummary", data={"email": club_test["email"]}, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = client.get(
        f"/book/{competition_test['name']}/{club_test['name']}", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"How many places?" in response.data

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club_test["points"]) == points_before - places_required
    assert int(competition_test["numberOfPlaces"]) == places_before - places_required


def test_failed_booking_workflow(client, booking_test_data):

    club_test, competition_test = booking_test_data

    points_before = int(club_test["points"])
    places_before = int(competition_test["numberOfPlaces"])

    response = client.post(
        "/showSummary", data={"email": club_test["email"]}, follow_redirects=True
    )

    assert response.status_code == 200

    response = client.get(
        f"/book/{competition_test['name']}/{club_test['name']}", follow_redirects=True
    )

    assert response.status_code == 200

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": "-5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You must book at least 1 place" in response.data
    assert int(club_test["points"]) == points_before
    assert int(competition_test["numberOfPlaces"]) == places_before

