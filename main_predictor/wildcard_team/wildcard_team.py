import requests
import datetime
from main_predictor import constants

Constants = constants.Dream_Team_Constants
wildcard_team = []
provisional_wildcard_team = []
total_points = 0
total_price = 0

class Utilities:
    @staticmethod
    def remove_player(squad_number_to_go, pos):
        wildcard_team.pop(squad_number_to_go)
        for player in provisional_wildcard_team:
            if player['pos'] == pos:
                wildcard_team.append(player)
                provisional_wildcard_team.remove(player)
                break

    @staticmethod
    def add_player():
        value_matched_players = []
        points_clash = 0
        for player in provisional_wildcard_team:
            if player['ep_next'] >= points_clash:
                points_clash = player['ep_next']
                value_matched_players.append(player)
            else:
                break

        value_sorted_players = sorted(value_matched_players, key=lambda i: i['price'])
        for player in value_sorted_players:
            if player['pos'] == 1 and TeamValidityCheck.goalie_check() == Constants.UNDERLOAD \
                    or player['pos'] == 2 and TeamValidityCheck.defender_check() == Constants.HAS_ROOM or TeamValidityCheck.defender_check() == Constants.AT_MINIMUM \
                    or player['pos'] == 3 and TeamValidityCheck.midfielder_check() == Constants.HAS_ROOM or TeamValidityCheck.midfielder_check() == Constants.AT_MINIMUM \
                    or player['pos'] == 4 and TeamValidityCheck.striker_check() == Constants.HAS_ROOM:
                wildcard_team.append(player)


            # if (player['pos'] != 1 or TeamValidityCheck.goalie_check() != Constants.UNDERLOAD) and (
            #         player['pos'] != 2 or TeamValidityCheck.defender_check() != Constants.HAS_ROOM or TeamValidityCheck.defender_check() != Constants.AT_MINIMUM) and (
            #         player['pos'] != 3 or TeamValidityCheck.midfielder_check() != Constants.HAS_ROOM) and (
            #         player['pos'] != 4 or TeamValidityCheck.striker_check() != Constants.HAS_ROOM):
            #     continue
            # wildcard_team.append(player)
            # break


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

        if upcoming_gameweek == "Gameweek 1":
            print("The season hasn't started. Try again after the first Gameweek has been played.")
            return False
        else:
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
                    'price': player['now_cost'] / 10,
                    'ep_next': float(player['ep_next'])
                })

            global provisional_wildcard_team
            global wildcard_team
            provisional_wildcard_team = sorted(players, key=lambda i: (i['ep_next'], -i['price']), reverse=True)
            wildcard_team = []

            # Make sure positions are valid
            for dream_player in provisional_wildcard_team[:11]:
                provisional_wildcard_team.remove(dream_player)
                wildcard_team.append(dream_player)

            return True


class TeamValidityCheck:

    @staticmethod
    def goalie_check():
        if sum(player['pos'] == Constants.GOALKEEPER for player in wildcard_team) < Constants.MIN_GOALKEEPER:
            return Constants.UNDERLOAD
        elif sum(player['pos'] == Constants.GOALKEEPER for player in wildcard_team) > Constants.MAX_GOALKEEPER:
            return Constants.OVERLOAD
        elif sum(player['pos'] == Constants.GOALKEEPER for player in wildcard_team) == Constants.MIN_GOALKEEPER:
            return Constants.AT_MINIMUM
        else:
            return Constants.OK

    @staticmethod
    def defender_check():
        if sum(player['pos'] == Constants.DEFENDER for player in wildcard_team) < Constants.MIN_DEFENDER:
            return Constants.UNDERLOAD
        elif sum(player['pos'] == Constants.DEFENDER for player in wildcard_team) > Constants.MAX_DEFENDER:
            return Constants.OVERLOAD
        elif sum(player['pos'] == Constants.DEFENDER for player in wildcard_team) == Constants.MIN_DEFENDER:
            return Constants.AT_MINIMUM
        elif sum(player['pos'] == Constants.DEFENDER for player in wildcard_team) < Constants.MAX_DEFENDER:
            return Constants.HAS_ROOM

        else:
            return Constants.OK

    @staticmethod
    def midfielder_check():
        if sum(player['pos'] == Constants.MIDFIELDER for player in wildcard_team) < Constants.MIN_MIDFIELDER:
            return Constants.UNDERLOAD
        elif sum(player['pos'] == Constants.MIDFIELDER for player in wildcard_team) > Constants.MAX_MIDFIELDER:
            return Constants.OVERLOAD
        elif sum(player['pos'] == Constants.MIDFIELDER for player in wildcard_team) == Constants.MIN_MIDFIELDER:
            return Constants.AT_MINIMUM
        elif sum(player['pos'] == Constants.MIDFIELDER for player in wildcard_team) < Constants.MAX_MIDFIELDER:
            return Constants.HAS_ROOM
        else:
            return Constants.OK

    @staticmethod
    def striker_check():
        if sum(player['pos'] == Constants.STRIKER for player in wildcard_team) < Constants.MIN_STRIKER:
            return Constants.UNDERLOAD
        elif sum(player['pos'] == Constants.STRIKER for player in wildcard_team) > Constants.MAX_STRIKER:
            return Constants.OVERLOAD
        elif sum(player['pos'] == Constants.STRIKER for player in wildcard_team) == Constants.MIN_STRIKER:
            return Constants.AT_MINIMUM
        elif sum(player['pos'] == Constants.STRIKER for player in wildcard_team) < Constants.MAX_STRIKER:
            return Constants.HAS_ROOM
        else:
            return Constants.OK

    def goalie_swap(self):
        squad_number = len(wildcard_team) - 1
        # No Goalie
        while self.goalie_check() == Constants.UNDERLOAD:
            pos_of_player_to_go = wildcard_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.GOALKEEPER)
            squad_number -= 1

        # More than one Goalie
        while self.goalie_check() == Constants.OVERLOAD:
            for player in reversed(wildcard_team):
                if player['pos'] == Constants.GOALKEEPER and self.goalie_check() == Constants.OVERLOAD:
                    wildcard_team.remove(player)
                    Utilities.add_player()

    def defender_swap(self):
        squad_number = len(wildcard_team)-1
        while self.defender_check() == Constants.UNDERLOAD:
            pos_of_player_to_go = wildcard_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.DEFENDER)
            squad_number -= 1

        while self.defender_check() == Constants.OVERLOAD:
            for player in reversed(wildcard_team):
                if player['pos'] == Constants.DEFENDER and self.defender_check() == Constants.OVERLOAD:
                    wildcard_team.remove(player)
                    Utilities.add_player()

    def midfielder_swap(self):
        squad_number = len(wildcard_team)-1
        while self.midfielder_check() == Constants.UNDERLOAD:
            pos_of_player_to_go = wildcard_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.MIDFIELDER)
            squad_number -= 1

        while self.midfielder_check() == Constants.OVERLOAD:
            for player in reversed(wildcard_team):
                if player['pos'] == Constants.MIDFIELDER and self.midfielder_check() == Constants.OVERLOAD:
                    wildcard_team.remove(player)
                    Utilities.add_player()

    def striker_swap(self):
        squad_number = len(wildcard_team)-1
        while self.striker_check() == Constants.UNDERLOAD:
            pos_of_player_to_go = wildcard_team[squad_number]['pos']
            self.prepare_to_swap(squad_number, pos_of_player_to_go, Constants.STRIKER)
            squad_number -= 1

        while self.striker_check() == Constants.OVERLOAD:
            for player in reversed(wildcard_team):
                if player['pos'] == Constants.STRIKER and self.striker_check() == Constants.OVERLOAD:
                    wildcard_team.remove(player)
                    Utilities.add_player()

    def prepare_to_swap(self, squad_number, outgoing_pos, incoming_pos):
        if outgoing_pos == Constants.GOALKEEPER and not self.goalie_check() == Constants.AT_MINIMUM:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.DEFENDER and not self.defender_check() == Constants.AT_MINIMUM:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.MIDFIELDER and not self.midfielder_check() == Constants.AT_MINIMUM:
            Utilities.remove_player(squad_number, incoming_pos)
        if outgoing_pos == Constants.STRIKER and not self.striker_check() == Constants.AT_MINIMUM:
            Utilities.remove_player(squad_number, incoming_pos)


class TeamBuild:
    def __init__(self):
        ib = InitialTeamBuild()
        if ib.build():
            t = TeamValidityCheck()

            t.goalie_swap()
            t.defender_swap()
            t.midfielder_swap()
            t.striker_swap()


if __name__ == "__main__":
    begin_time = datetime.datetime.now()
    tb = TeamBuild()
    for dream_player in sorted(wildcard_team, key=lambda i: i['pos']):
        total_points += dream_player['gw_points']
        total_price += dream_player['price']
        print(dream_player)

    print('\nTotal Points:', total_points, 'Total Price', total_price)
    print('Run time:', datetime.datetime.now() - begin_time)



