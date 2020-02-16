import requests


def get_game(event_key):
    return (requests.get(f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches",
                         headers={
                             "X-TBA-Auth-Key": "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"}))


def get_team_by_key(team_key):
    return requests.get(f"https://www.thebluealliance.com/api/v3/team/{team_key}",
                        headers={"X-TBA-Auth-Key": "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"}).json()


def get_teams_in_game(event_key):
    data = get_game(event_key).json()
    matches = {}
    for i in range(len(data)):
        teams = []
        for team in data[i]["alliances"]["red"]["team_keys"]:
            teams.append(get_team_by_key(team))
        for team in data[i]["alliances"]["blue"]["team_keys"]:
            teams.append(get_team_by_key(team))
        print(teams)
        matches[f"match{i}"] = teams


def main():
    print(get_teams_in_game('2020week0'))


if __name__ == '__main__':
    main()
