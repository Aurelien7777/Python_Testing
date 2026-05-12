MAX_PLACES_PER_BOOKING = 12


def is_valid_place_number(places_required):
    return places_required > 0


def has_enough_competition_places(places_required, competition_places):
    return places_required <= competition_places


def is_within_booking_limit(places_required, max_places=MAX_PLACES_PER_BOOKING):
    return places_required <= max_places


def has_enough_points(club_points, places_required):
    return club_points >= places_required


def calculate_remaining_places(competition_places, places_required):
    return competition_places - places_required


def calculate_remaining_points(club_points, places_required):
    return club_points - places_required
