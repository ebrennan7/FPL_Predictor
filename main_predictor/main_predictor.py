import requests
import json

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
best_player = {'name': None, 'max_value': 0}
for player in players:
    if float(player['ep_next']) > float(best_player['max_value']):
        best_player['max_value'] = player['ep_next']
        best_player['name'] = player['first_name'] + ' ' + player['second_name']

print(best_player)



