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

# Make new list with relevant properties
for player in players_raw:
    players.append({
        'id': player['id'],
        'name': player['first_name'] + ' ' + player['second_name'],
        'gw_points': player['event_points'],
        'pos': player['element_type'],
        'price': player['now_cost']/10
    })


provisional_dream_team = sorted(players, key=lambda i: i['gw_points'], reverse=True)
dream_team = []
# Make sure positions are valid
for dream_player in provisional_dream_team[:11]:
    provisional_dream_team.remove(dream_player)
    dream_team.append(dream_player)

# dream_team = sorted(dream_team, key=lambda i: i['pos'])

# Goalie Check!
if not any(player['pos'] == 1 for player in dream_team):
    pos_of_player_to_go = dream_team[-1]['pos']
    print('position of player to be removed ', pos_of_player_to_go)
    if pos_of_player_to_go == 4:
        print('amount of strikers', sum(player['pos'] == 4 for player in dream_team))
        if sum(player['pos'] == 4 for player in dream_team) < 2:
            print('not enough striker')
        else:
            dream_team.pop()
            for player in provisional_dream_team:
                if player['pos'] == 1:
                    dream_team.append(player)
                    provisional_dream_team.remove(player)
                    break

for dream_player in dream_team:
    print(dream_player)

print(provisional_dream_team)