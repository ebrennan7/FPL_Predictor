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

players_raw = parsed['elements']
players = []

for player in players_raw:
    players.append({
        'id': player['id'],
        'name': player['first_name'] + ' ' + player['second_name'],
        'gw_points': player['event_points'],
        'pos': player['element_type'],
        'price': player['now_cost']/10
    })


dream_team = sorted(players, key=lambda i: i['gw_points'], reverse=True)

for dream_player in dream_team[:11]:
    print(dream_player)