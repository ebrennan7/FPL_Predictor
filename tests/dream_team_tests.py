import unittest
from main_predictor.dream_team import dream_team

class DreamTeamTests(unittest.TestCase):
    test_goalie = {'gw_points': 1, 'id': 1, 'name': 'Test Goalie', 'pos': 1, 'price': 1}
    test_defender = {'gw_points': 1, 'id': 1, 'name': 'Test Defender', 'pos': 2, 'price': 1}
    test_midfielder = {'gw_points': 1, 'id': 1, 'name': 'Test Midfielder', 'pos': 3, 'price': 1}
    test_striker = {'gw_points': 1, 'id': 1, 'name': 'Test Striker', 'pos': 4, 'price': 1}
    test_player = {'gw_points': 1, 'id': 1, 'name': 'Test Player', 'pos': 99, 'price': 1}

    def test_initial_team_build(self):
        dream_team.dream_team = []
        self.assertEqual(dream_team.dream_team, [])
        dream_team.InitialTeamBuild.build()
        self.assertEqual(len(dream_team.dream_team), 11)

    def test_too_many_goalies(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        while len(dream_team.dream_team) <= 11:
            dream_team.dream_team.append(self.test_goalie)

        dream_team.TeamValidityCheck.goalie_swap(tv_instance)
        self.assertEqual(len(dream_team.dream_team), dream_team.Constants.MAX_GOALKEEPER)

    def test_no_goalie(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        test_player = {'gw_points': 1, 'id': 1, 'name': 'Goalie 1', 'pos': 2, 'price': 1}
        while len(dream_team.dream_team) <= 11:
            dream_team.dream_team.append(test_player)
        dream_team.provisional_dream_team = [{'gw_points': 1, 'id': 1, 'name': 'Goalie 1', 'pos': 2, 'price': 1},
                                                   dict(gw_points=1, id=1, name='Goalie 2', pos=1, price=1)]
        dream_team.TeamValidityCheck.goalie_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), dream_team.Constants.MIN_GOALKEEPER)

    def test_too_many_defenders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_defender)
            dream_team.provisional_dream_team.append(self.test_player)

        dream_team.TeamValidityCheck.defender_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MAX_DEFENDER)

    def test_not_enough_defenders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_midfielder)
            dream_team.provisional_dream_team.append(self.test_defender)

        dream_team.TeamValidityCheck.defender_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MIN_DEFENDER)

    def test_not_enough_midfielders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_defender)
            dream_team.provisional_dream_team.append(self.test_midfielder)

        dream_team.TeamValidityCheck.midfielder_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MIN_MIDFIELDER)

    def test_too_many_midfielders(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_midfielder)
            dream_team.provisional_dream_team.append(self.test_player)

        dream_team.TeamValidityCheck.midfielder_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MAX_MIDFIELDER)

    def test_not_enough_strikers(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_defender)
            dream_team.provisional_dream_team.append(self.test_striker)

        dream_team.TeamValidityCheck.striker_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MIN_STRIKER)

    def test_too_many_strikers(self):
        tv_instance = dream_team.TeamValidityCheck()
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []

        while len(dream_team.provisional_dream_team) <= 11:
            dream_team.dream_team.append(self.test_striker)
            dream_team.provisional_dream_team.append(self.test_player)

        dream_team.TeamValidityCheck.striker_swap(tv_instance)

        self.assertEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MAX_STRIKER)

    def test_team_validity(self):
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []
        tv_instance = dream_team.TeamValidityCheck()

        dream_team.InitialTeamBuild.build()
        tv_instance.goalie_swap()
        tv_instance.defender_swap()
        tv_instance.midfielder_swap()
        tv_instance.striker_swap()

        self.assertEqual(len(dream_team.dream_team), 11)
        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), dream_team.Constants.MAX_GOALKEEPER)
        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), dream_team.Constants.MIN_GOALKEEPER)
        self.assertLessEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MAX_DEFENDER)
        self.assertGreaterEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MIN_DEFENDER)
        self.assertGreaterEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MIN_MIDFIELDER)
        self.assertLessEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MAX_MIDFIELDER)
        self.assertGreaterEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MIN_STRIKER)
        self.assertLessEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MAX_STRIKER)

    def test_team_build(self):
        dream_team.dream_team = []
        dream_team.provisional_dream_team = []
        itb = dream_team.TeamBuild()

        self.assertEqual(len(dream_team.dream_team), 11)
        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), dream_team.Constants.MAX_GOALKEEPER)
        self.assertEqual(sum(player['pos'] == 1 for player in dream_team.dream_team), dream_team.Constants.MIN_GOALKEEPER)
        self.assertLessEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MAX_DEFENDER)
        self.assertGreaterEqual(sum(player['pos'] == 2 for player in dream_team.dream_team), dream_team.Constants.MIN_DEFENDER)
        self.assertGreaterEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MIN_MIDFIELDER)
        self.assertLessEqual(sum(player['pos'] == 3 for player in dream_team.dream_team), dream_team.Constants.MAX_MIDFIELDER)
        self.assertGreaterEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MIN_STRIKER)
        self.assertLessEqual(sum(player['pos'] == 4 for player in dream_team.dream_team), dream_team.Constants.MAX_STRIKER)


if __name__ == '__main__':
    unittest.main()
