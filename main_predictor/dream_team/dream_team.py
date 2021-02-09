import requests

dream_team = []
provisional_dream_team = []


class Utilities:
    @staticmethod
    def check_strikers():
        if sum(dream_player['pos'] == 4 for dream_player in dream_team) < 2:
            print('Not enough strikers')
            return False
        else:
            return True

    @staticmethod
    def remove_player(squad_number_to_go, pos):
        dream_team.pop(squad_number_to_go)
        for player in provisional_dream_team:
            if player['pos'] == pos:
                dream_team.append(player)
                provisional_dream_team.remove(player)
                break

    @staticmethod
    def add_player(new_player, pos):
        dream_team.append(new_player)


class InitialTeamBuild:

    def build(self):
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

        global provisional_dream_team
        global dream_team
        provisional_dream_team = sorted(players, key=lambda i: i['gw_points'], reverse=True)
        dream_team = []

        # Make sure positions are valid
        for dream_player in provisional_dream_team[:11]:
            provisional_dream_team.remove(dream_player)
            dream_team.append(dream_player)


class TeamValidityCheck:
    # Goalie Check!
    def goalie_check(self):
        squad_number = len(dream_team) - 1
        while not any(player['pos'] == 1 for player in dream_team):
            pos_of_player_to_go = dream_team[squad_number]['pos']
            print('position of player to be removed ', pos_of_player_to_go)
            if pos_of_player_to_go == 4:
                print('amount of strikers', sum(player['pos'] == 4 for player in dream_team))
                if sum(player['pos'] == 4 for player in dream_team) < 2:
                    print('not enough striker')
                    squad_number-=1
                else:
                    Utilities.remove_player(squad_number, 1)
            elif pos_of_player_to_go == 2:
                if sum(player['pos'] == 2 for player in dream_team) < 4:
                    print('not enough defenders')
                    squad_number-=1
                else:
                    Utilities.remove_player(squad_number, 1)
            elif pos_of_player_to_go == 3:
                if sum(player['pos'] == 3 for player in dream_team) < 3:
                    print('not enough mids')
                    squad_number-=1
                else:
                    Utilities.remove_player(squad_number, 1)



    # Defender Check!
    def defender_check(self):
        squad_number = len(dream_team)-1
        while sum(player['pos'] == 2 for player in dream_team) < 3:
            print('Not enough defenders')
            pos_of_player_to_go = dream_team[squad_number]['pos']
            if pos_of_player_to_go == 1 and sum(player['pos'] for player in dream_team) == 1 or pos_of_player_to_go == 2:
                print('defender for goalie')
                squad_number -= 1
            elif pos_of_player_to_go == 4 and not Utilities.check_strikers():
                squad_number -= 1
            else:
                Utilities.remove_player(squad_number, 2)


    def midfielder_check(self):
        squad_number = len(dream_team)-1
        while sum(player['pos'] == 3 for player in dream_team) > 5:
            for player in reversed(dream_team):
                if player['pos'] == 3:
                    dream_team.remove(player)
                    break
            for player in provisional_dream_team:
                Utilities.add_player(squad_number, player['pos'])


ib = InitialTeamBuild()
ib.build()
t = TeamValidityCheck()
t.defender_check()
t.goalie_check()
t.midfielder_check()


for dream_player in dream_team:
    print(dream_player)

print('\n', provisional_dream_team)



