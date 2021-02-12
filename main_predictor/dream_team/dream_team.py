import requests

dream_team = []
provisional_dream_team = []


class Option:
    OK = 0
    UNDERLOAD = 1
    OVERLOAD = 2

class Constants:
    GOALKEEPER = 1
    MAX_GOALKEEPER = 1
    MIN_GOALKEEPER = 1
    DEFENDER = 2
    MAX_DEFENDER = 5
    MIN_DEFENDER = 2
    MIDFIELDER = 3
    MAX_MIDFIELDER = 5
    MIN_MIDFIELDER = 2
    STRIKER = 4
    MAX_STRIKER = 3
    MIN_STRIKER = 1



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
        if sum(player['pos'] == Constants.GOALKEEPER for player in dream_team) < Constants.MIN_GOALKEEPER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.GOALKEEPER for player in dream_team) > Constants.MAX_GOALKEEPER:
            return Option.OVERLOAD
        else:
            return Option.OK

    def defender_check(self):
        if sum(player['pos'] == Constants.DEFENDER for player in dream_team) < Constants.MIN_DEFENDER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.DEFENDER for player in dream_team) > Constants.MAX_DEFENDER:
            return Option.OVERLOAD
        else:
            return Option.OK

    def midfieder_check(self):
        if sum(player['pos'] == Constants.MIDFIELDER for player in dream_team) < Constants.MIN_MIDFIELDER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.MIDFIELDER for player in dream_team) > Constants.MAX_MIDFIELDER:
            return Option.OVERLOAD
        else:
            return Option.OK

    def striker_check(self):
        if sum(player['pos'] == Constants.STRIKER for player in dream_team) < Constants.MIN_STRIKER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.STRIKER for player in dream_team) > Constants.MAX_STRIKER:
            return Option.OVERLOAD
        else:
            return Option.OK


    def goalie_swap(self):
        squad_number = len(dream_team) - 1

        # No Goalie
        while self.goalie_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            while self.goalie_check() == Option.UNDERLOAD:
                pos_of_player_to_go = dream_team[squad_number]['pos']
                print('pos', pos_of_player_to_go)
                self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.GOALKEEPER)
                squad_number -= 1

        # More than one Goalie
        while self.goalie_check() == Option.OVERLOAD:
            print('dream team', dream_team)
            for player in reversed(dream_team):
                if player['pos'] == Constants.GOALKEEPER and self.goalie_check() == Option.OVERLOAD:
                    print('removing', player['name'])
                    dream_team.remove(player)
                    Utilities.add_player()


    def defender_swap(self):
        squad_number = len(dream_team)-1
        while self.defender_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            print('pos', pos_of_player_to_go)
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.DEFENDER)
            squad_number -= 1

        while self.defender_check() == Option.OVERLOAD:
            for player in reversed(dream_team):
                if player['pos'] == Constants.DEFENDER and self.defender_check() == Option.OVERLOAD:
                    print('removing', player['name'])
                    dream_team.remove(player)
                    Utilities.add_player()

    def prepare_to_swap(self, squad_number, outgoing_pos, incoming_pos):
        if outgoing_pos == Constants.GOALKEEPER:
            if not self.goalie_check() == Option.UNDERLOAD:
                Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.DEFENDER:
            if not self.defender_check() == Option.UNDERLOAD:
                Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.MIDFIELDER:
            if not self.midfieder_check() == Option.UNDERLOAD:
                Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.STRIKER:
            if not self.striker_check() == Option.UNDERLOAD:
                Utilities.remove_player(squad_number, incoming_pos)



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



