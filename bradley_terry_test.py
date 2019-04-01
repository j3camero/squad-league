# Some of these tests use random numbers, so technically could be flaky.
# Flakiness has been avoided by selecting extremely wide bounds for the
# assertions that are beyond the reach of ordinary probability.
import unittest

import bradley_terry

class TestStringMethods(unittest.TestCase):

    def test_random_game_outcome(self):
        # Generate some random game outcomes with 75% win probability (3:1).
        games = 1000
        wins = 0
        for i in range(games):
            if bradley_terry.GenerateOneRandomGameOutcome(3, 1):
                wins += 1
        # The win rate should be between 50% and 100%.
        self.assertGreater(wins, games / 2)
        self.assertLess(wins, games)

    def test_generate_random_game_outcomes(self):
        trials = 1000
        skills = [1, 1, 2]
        outcomes = bradley_terry.GenerateRandomGameOutcomes(skills, trials)
        # Sanity check that winner != loser.
        self.assertNotEqual(outcomes[0][0], outcomes[0][1])
        # Count the number of wins by player.
        wins = [0, 0, 0]
        for winner, loser in outcomes:
            wins[winner] += 1
        # Each player should win some games.
        self.assertGreater(wins[0], 0)
        self.assertGreater(wins[1], 0)
        self.assertGreater(wins[2], 0)
        # Player 2 should win more games due to higher skill.
        self.assertGreater(wins[2], trials / 3)
        # The wins should add up to the total number of games played.
        self.assertEqual(sum(wins), trials)

    def test_normalize(self):
        p = bradley_terry.Normalize([1, 1, 2])
        self.assertAlmostEqual(p[0], 0.25)
        self.assertAlmostEqual(p[1], 0.25)
        self.assertAlmostEqual(p[2], 0.5)

    def test_solve_two_players(self):
        trials = 1000
        outcomes = bradley_terry.GenerateRandomGameOutcomes([1, 2], trials)
        report = 'bradley-terry-solve-two-players.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertLess(p[0], 0.5)
        self.assertGreater(p[1], 0.5)

if __name__ == '__main__':
    unittest.main()
