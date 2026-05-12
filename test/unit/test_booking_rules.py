import pytest

from booking_rules import (
    is_valid_place_number,
    has_enough_competition_places,
    is_within_booking_limit,
    has_enough_points,
    calculate_remaining_places,
    calculate_remaining_points,
)


@pytest.mark.parametrize(
    "places, expected",
    [
        (1, True),
        (0, False),
        (-1, False),
    ],
)
def test_is_valid_place_number(places, expected):
    assert is_valid_place_number(places) is expected


@pytest.mark.parametrize(
    "requested_places, available_places, expected",
    [
        (5, 10, True),
        (10, 10, True),
        (11, 10, False),
    ],
)
def test_has_enough_competition_places(requested_places, available_places, expected):
    assert has_enough_competition_places(requested_places, available_places) is expected


@pytest.mark.parametrize(
    "places, expected",
    [
        (5, True),
        (12, True),
        (13, False),
    ],
)
def test_is_within_booking_limit(places, expected):
    assert is_within_booking_limit(places) is expected


@pytest.mark.parametrize(
    "club_points, requested_places, expected",
    [
        (20, 10, True),
        (10, 10, True),
        (5, 10, False),
    ],
)
def test_has_enough_points(club_points, requested_places, expected):
    assert has_enough_points(club_points, requested_places) is expected


@pytest.mark.parametrize(
    "available_places, requested_places, expected",
    [
        (20, 5, 15),
        (12, 12, 0),
    ],
)
def test_calculate_remaining_places(available_places, requested_places, expected):
    assert calculate_remaining_places(available_places, requested_places) == expected


@pytest.mark.parametrize(
    "club_points, requested_places, expected",
    [
        (20, 5, 15),
        (12, 12, 0),
    ],
)
def test_calculate_remaining_points(club_points, requested_places, expected):
    assert calculate_remaining_points(club_points, requested_places) == expected
