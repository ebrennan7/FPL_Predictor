import requests
import datetime

dream_team = []
provisional_dream_team = []
total_points = 0
total_price = 0

class Option:
    OK = 0
    UNDERLOAD = 1
    OVERLOAD = 2
    HAS_ROOM = 3


class Constants:
    GOALKEEPER = 1
    MAX_GOALKEEPER = 1
    MIN_GOALKEEPER = 1
    DEFENDER = 2
    MAX_DEFENDER = 5
    MIN_DEFENDER = 3
    MIDFIELDER = 3
    MAX_MIDFIELDER = 5
    MIN_MIDFIELDER = 2
    STRIKER = 4
    MAX_STRIKER = 3
    MIN_STRIKER = 1


class Utilities:
    @staticmethod
    def remove_player(squad_number_to_go, pos):
        dream_team.pop(squad_number_to_go)
        for player in provisional_dream_team:
            if player['pos'] == pos:
                dream_team.append(player)
                provisional_dream_team.remove(player)
                break

    @staticmethod
    def add_player():
        value_matched_players = []
        points_clash = 0
        for player in provisional_dream_team:
            if player['gw_points'] >= points_clash:
                points_clash = player['gw_points']
                value_matched_players.append(player)
            else:
                break

        value_sorted_players = sorted(value_matched_players, key=lambda i: i['price'])
        # value_matched_players = []
        for player in value_sorted_players:
            if player['pos'] == 1 and TeamValidityCheck.goalie_check() == Option.UNDERLOAD:
                dream_team.append(player)
                break
            elif player['pos'] == 2 and TeamValidityCheck.defender_check() == Option.HAS_ROOM:
                dream_team.append(player)
                break
            elif player['pos'] == 3 and TeamValidityCheck.midfielder_check() == Option.HAS_ROOM:
                dream_team.append(player)
                break
            elif player['pos'] == 4 and TeamValidityCheck.striker_check() == Option.HAS_ROOM:
                dream_team.append(player)
                break
            # else:
            #     points_clash = 0
            #     break


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
        provisional_dream_team = sorted(players, key=lambda i: (i['gw_points'], -i['price']), reverse=True)
        dream_team = []

        # Make sure positions are valid
        for dream_player in provisional_dream_team[:11]:
            provisional_dream_team.remove(dream_player)
            dream_team.append(dream_player)


class TeamValidityCheck:

    @staticmethod
    def goalie_check():
        if sum(player['pos'] == Constants.GOALKEEPER for player in dream_team) < Constants.MIN_GOALKEEPER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.GOALKEEPER for player in dream_team) > Constants.MAX_GOALKEEPER:
            return Option.OVERLOAD
        else:
            return Option.OK

    @staticmethod
    def defender_check():
        if sum(player['pos'] == Constants.DEFENDER for player in dream_team) < Constants.MIN_DEFENDER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.DEFENDER for player in dream_team) > Constants.MAX_DEFENDER:
            return Option.OVERLOAD
        elif sum(player['pos'] == Constants.DEFENDER for player in dream_team) < Constants.MAX_DEFENDER:
            return Option.HAS_ROOM
        else:
            return Option.OK

    @staticmethod
    def midfielder_check():
        if sum(player['pos'] == Constants.MIDFIELDER for player in dream_team) < Constants.MIN_MIDFIELDER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.MIDFIELDER for player in dream_team) > Constants.MAX_MIDFIELDER:
            return Option.OVERLOAD
        elif sum(player['pos'] == Constants.MIDFIELDER for player in dream_team) < Constants.MAX_MIDFIELDER:
            return Option.HAS_ROOM
        else:
            return Option.OK

    @staticmethod
    def striker_check():
        if sum(player['pos'] == Constants.STRIKER for player in dream_team) < Constants.MIN_STRIKER:
            return Option.UNDERLOAD
        elif sum(player['pos'] == Constants.STRIKER for player in dream_team) > Constants.MAX_STRIKER:
            return Option.OVERLOAD
        elif sum(player['pos'] == Constants.STRIKER for player in dream_team) < Constants.MAX_STRIKER:
            return Option.HAS_ROOM
        else:
            return Option.OK

    def goalie_swap(self):
        squad_number = len(dream_team) - 1
        # No Goalie
        while self.goalie_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.GOALKEEPER)
            squad_number -= 1

        # More than one Goalie
        while self.goalie_check() == Option.OVERLOAD:
            for player in reversed(dream_team):
                if player['pos'] == Constants.GOALKEEPER and self.goalie_check() == Option.OVERLOAD:
                    dream_team.remove(player)
                    Utilities.add_player()

    def defender_swap(self):
        squad_number = len(dream_team)-1
        while self.defender_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.DEFENDER)
            squad_number -= 1

        while self.defender_check() == Option.OVERLOAD:
            for player in reversed(dream_team):
                if player['pos'] == Constants.DEFENDER and self.defender_check() == Option.OVERLOAD:
                    dream_team.remove(player)
                    Utilities.add_player()

    def midfielder_swap(self):
        squad_number = len(dream_team)-1
        while self.midfielder_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.MIDFIELDER)
            squad_number -= 1

        while self.midfielder_check() == Option.OVERLOAD:
            for player in reversed(dream_team):
                if player['pos'] == Constants.MIDFIELDER and self.midfielder_check() == Option.OVERLOAD:
                    dream_team.remove(player)
                    Utilities.add_player()

    def striker_swap(self):
        squad_number = len(dream_team)-1
        while self.striker_check() == Option.UNDERLOAD:
            pos_of_player_to_go = dream_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.STRIKER)
            squad_number -= 1

        while self.striker_check() == Option.OVERLOAD:
            for player in reversed(dream_team):
                if player['pos'] == Constants.STRIKER and self.striker_check() == Option.OVERLOAD:
                    dream_team.remove(player)
                    Utilities.add_player()

    def prepare_to_swap(self, squad_number, outgoing_pos, incoming_pos):
        if outgoing_pos == Constants.GOALKEEPER and not self.goalie_check() == Option.UNDERLOAD:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.DEFENDER and not self.defender_check() == Option.UNDERLOAD:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.MIDFIELDER and not self.midfielder_check() == Option.UNDERLOAD:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.STRIKER and not self.striker_check() == Option.UNDERLOAD:
            Utilities.remove_player(squad_number, incoming_pos)


class TeamBuild:
    def __init__(self):
        ib = InitialTeamBuild()
        ib.build()
        t = TeamValidityCheck()

        t.goalie_swap()
        t.defender_swap()
        t.midfielder_swap()
        t.striker_swap()


begin_time = datetime.datetime.now()
tb = TeamBuild()
for dream_player in sorted(dream_team, key=lambda i: i['pos']):
    total_points += dream_player['gw_points']
    total_price += dream_player['price']
    print(dream_player)

print('\nTotal Points:', total_points, 'Total Price', total_price)
print('Run time:', datetime.datetime.now() - begin_time)



