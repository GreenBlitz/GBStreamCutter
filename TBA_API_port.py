import requests


def get_game(event_key):
    return (requests.get(f"https://www.thebluealliance.com/api/v3/match/{event_key}",
                         headers={
                             "X-TBA-Auth-Key": "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"}))


def get_team_by_key(team_key):
    return requests.get(f"https://www.thebluealliance.com/api/v3/team/{team_key}",
                        headers={"X-TBA-Auth-Key": "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"}).json()


def get_teams_in_game(event_key):
    data = get_game(event_key).json()
    red_teams = []
    blue_teams = []
    for team in data["alliances"]["red"]["team_keys"]:
        red_teams.append(get_team_by_key(team)["nickname"])
    for team in data["alliances"]["blue"]["team_keys"]:
        blue_teams.append(get_team_by_key(team)["nickname"])
    return [red_teams, blue_teams]


def main():
    print(get_teams_in_game('2020week0_qm1'))


if __name__ == '__main__':
    main()
