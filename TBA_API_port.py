import requests


def get_teams_in_game(match_id):
    return requests.get(f"https://www.thebluealliance.com/api/v3/event/{match_id}/teams/simple",
        headers={"X-TBA-Auth-Key": "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"})

