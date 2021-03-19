import unittest
import mock
from main_predictor.dream_team import dream_team
import wait_response


class DreamTeamTests(unittest.TestCase):

    def test_initial_team_build(self):
        self.assertEqual(dream_team.dream_team, [])
        dream_team.InitialTeamBuild.build()
        self.assertEqual(len(dream_team.dream_team), 11)

    def test_too_many_goalies(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = [{'gw_points': 1, 'id': 1, 'name': 'Goalie 1', 'pos': 1, 'price': 1},
                                                   dict(gw_points=1, id=1, name='Goalie 2', pos=1, price=1)]
        dream_team.TeamValidityCheck.goalie_swap(tv_instance)
        self.assertEqual(len(dream_team.dream_team), 1)

    def test_no_goalie(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        test_player = {'gw_points': 1, 'id': 1, 'name': 'Goalie 1', 'pos': 2, 'price': 1}
        while len(dream_team.dream_team) <= 11:
            dream_team.dream_team.append(test_player)
        dream_team.provisional_dream_team = [{'gw_points': 1, 'id': 1, 'name': 'Goalie 1', 'pos': 2, 'price': 1},
                                                   dict(gw_points=1, id=1, name='Goalie 2', pos=1, price=1)]
        dream_team.TeamValidityCheck.goalie_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), 1)

    def test_too_many_defenders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []
        test_defender = {'gw_points': 1, 'id': 1, 'name': 'Test Defender', 'pos': 2, 'price': 1}
        test_player = {'gw_points': 1, 'id': 1, 'name': 'Test Player', 'pos': 99, 'price': 1}
        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(test_defender)
            dream_team.provisional_dream_team.append(test_player)

        dream_team.TeamValidityCheck.defender_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), 5)

    def test_not_enough_defenders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        test_defender = {'gw_points': 1, 'id': 1, 'name': 'Test Defender', 'pos': 2, 'price': 1}
        test_player = {'gw_points': 1, 'id': 1, 'name': 'Test Player', 'pos': 3, 'price': 1}
        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(test_player)
            dream_team.provisional_dream_team.append(test_defender)

        dream_team.TeamValidityCheck.defender_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), 3)





if __name__ == '__main__':
    unittest.main()
