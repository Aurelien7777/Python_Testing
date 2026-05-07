def test_complete_booking_workflow(client, booking_test_data):

    club_test, competition_test = booking_test_data

    points_before = int(club_test["points"])
    places_before = int(competition_test["numberOfPlaces"])
    places_required = 5

    response = client.post(
        "/showSummary",
        data={"email": club_test["email"]},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome" in response.data

    response = client.get(
        f"/book/{competition_test['name']}/{club_test['name']}",
        follow_redirects=True
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
        follow_redirects=True
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
        "/showSummary",
        data={"email": club_test["email"]},
        follow_redirects=True
    )

    assert response.status_code == 200

    response = client.get(
        f"/book/{competition_test['name']}/{club_test['name']}",
        follow_redirects=True
    )

    assert response.status_code == 200

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": "-5",
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"You must book at least 1 place" in response.data
    assert int(club_test["points"]) == points_before
    assert int(competition_test["numberOfPlaces"]) == places_before