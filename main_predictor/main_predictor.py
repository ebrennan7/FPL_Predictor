import requests

bootstrap_static = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
parsed = bootstrap_static.json()

gameweeks = parsed['events']
upcoming_gameweek = 'The season is finished'
for gameweek in gameweeks:
    if not gameweek['finished']:
        upcoming_gameweek = gameweek['name']
        break

print(upcoming_gameweek)

players = parsed['elements']
best_player = {'id': None, 'name': None, 'expected_points': 0, 'position': None}
for player in players:
    if float(player['ep_next']) > float(best_player['expected_points']):
        best_player['id'] = player['id']
        best_player['expected_points'] = player['ep_next']
        best_player['name'] = player['first_name'] + ' ' + player['second_name']
        best_player['position'] = player['element_type']

print(best_player)