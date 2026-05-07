from booking_rules import (
    is_valid_place_number,
    has_enough_competition_places,
    is_within_booking_limit,
    has_enough_points,
    calculate_remaining_places,
    calculate_remaining_points,
)


def test_place_number_is_valid_when_greater_than_zero():
    assert is_valid_place_number(1) is True


def test_place_number_is_invalid_when_zero():
    assert is_valid_place_number(0) is False


def test_place_number_is_invalid_when_negative():
    assert is_valid_place_number(-1) is False


def test_has_enough_competition_places_when_requested_is_less():
    assert has_enough_competition_places(5, 10) is True


def test_has_enough_competition_places_when_requested_is_equal():
    assert has_enough_competition_places(10, 10) is True


def test_has_not_enough_competition_places_when_requested_is_greater():
    assert has_enough_competition_places(11, 10) is False


def test_booking_is_within_limit_when_less_than_12():
    assert is_within_booking_limit(5) is True


def test_booking_is_within_limit_when_equal_to_12():
    assert is_within_booking_limit(12) is True


def test_booking_is_not_within_limit_when_more_than_12():
    assert is_within_booking_limit(13) is False


def test_club_has_enough_points_when_points_are_greater():
    assert has_enough_points(20, 10) is True


def test_club_has_enough_points_when_points_are_equal():
    assert has_enough_points(10, 10) is True


def test_club_has_not_enough_points_when_points_are_lower():
    assert has_enough_points(5, 10) is False


def test_remaining_places_are_calculated():
    assert calculate_remaining_places(20, 5) == 15


def test_remaining_places_can_be_zero():
    assert calculate_remaining_places(12, 12) == 0


def test_remaining_points_are_calculated():
    assert calculate_remaining_points(20, 5) == 15


def test_remaining_points_can_be_zero():
    assert calculate_remaining_points(12, 12) == 0