import requests

dream_team = []
provisional_dream_team = []


class Option:
    OK = 0
    UNDERLOAD = 1
    OVERLOAD = 2


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
        print('player removed')
        dream_team.pop(squad_number_to_go)
        for player in provisional_dream_team:
            if player['pos'] == pos:
                dream_team.append(player)
                provisional_dream_team.remove(player)
                break

    @staticmethod
    def add_player():
        print('adding player')
        value_matched_players = []
        points_clash = 0
        for player in provisional_dream_team:
            if player['gw_points'] >= points_clash:
                points_clash = player['gw_points']
                value_matched_players.append(player)

        value_sorted_players = sorted(value_matched_players, key=lambda i: i['price'])
        dream_team.append(value_sorted_players[0])


class InitialTeamBuild:

    @staticmethod
    def build():
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

    def goalie_check(self):
        if sum(player['pos'] == 1 for player in dream_team) < 1:
            return Option.UNDERLOAD
        elif sum(player['pos'] == 1 for player in dream_team) > 1:
            return Option.OVERLOAD
        else:
            return Option.OK

    def defender_check(self):
        if sum(player['pos'] == 2 for player in dream_team) < 3:
            return Option.UNDERLOAD
        elif sum(player['pos'] == 2 for player in dream_team) > 5:
            return Option.OVERLOAD
        else:
            return Option.OK

    def midfieder_check(self):
        if sum(player['pos'] == 3 for player in dream_team) < 2:
            return Option.UNDERLOAD
        elif sum(player['pos'] == 3 for player in dream_team) > 5:
            return Option.OVERLOAD
        else:
            return Option.OK

    def striker_check(self):
        if sum(player['pos'] == 4 for player in dream_team) < 1:
            return Option.UNDERLOAD
        elif sum(player['pos'] == 4 for player in dream_team) > 3:
            return Option.OVERLOAD
        else:
            return Option.OK


    def goalie_swap(self):
        squad_number = len(dream_team) - 1

        # No Goalie
        while self.goalie_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            if pos_of_player_to_go == 4:
                if self.striker_check() == Option.UNDERLOAD:
                    print('not enough striker')
                    squad_number -= 1
                else:
                    Utilities.remove_player(squad_number, 1)
            elif pos_of_player_to_go == 2:
                if self.defender_check() == Option.UNDERLOAD:
                    print('not enough defenders')
                    squad_number -= 1
                else:
                    Utilities.remove_player(squad_number, 1)
            elif pos_of_player_to_go == 3:
                if self.midfieder_check() == Option.UNDERLOAD:
                    print('not enough mids')
                    squad_number -= 1
                else:
                    Utilities.remove_player(squad_number, 1)

        # More than one Goalie
        while self.goalie_check() == Option.OVERLOAD:
            print('dream team', dream_team)
            for player in reversed(dream_team):
                if player['pos'] == 1 and self.goalie_check() == Option.OVERLOAD:
                    print('removing', player['name'])
                    dream_team.remove(player)
                    Utilities.add_player()


    def defender_swap(self):
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


    # def midfielder_swap(self):
    #     squad_number = len(dream_team)-1
    #     while sum(player['pos'] == 3 for player in dream_team) > 5:
    #         for player in reversed(dream_team):
    #             if player['pos'] == 3:
    #                 dream_team.remove(player)
    #                 break
    #         for player in provisional_dream_team:
    #             Utilities.add_player(player['pos'])


class TeamBuild:
    def build(self):
        ib = InitialTeamBuild()
        ib.build()
        t = TeamValidityCheck()


        t.goalie_swap()
        t.defender_swap()


tb = TeamBuild()
tb.build()

for dream_player in sorted(dream_team, key=lambda i: i['pos']):
    print(dream_player)

print('\n', provisional_dream_team)



