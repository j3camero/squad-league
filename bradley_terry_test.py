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
        self.assertAlmostEqual(p[0], 0.25, 3)
        self.assertAlmostEqual(p[1], 0.25, 3)
        self.assertAlmostEqual(p[2], 0.5, 3)

    def test_solve_two_players(self):
        trials = 1000
        outcomes = bradley_terry.GenerateRandomGameOutcomes([1, 2], trials)
        report = 'bradley-terry-solve-two-players.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertLess(p[0], 0.5)
        self.assertGreater(p[1], 0.5)

    def test_solve_three_players(self):
        trials = 1000
        outcomes = bradley_terry.GenerateRandomGameOutcomes([1, 2, 3], trials)
        report = 'bradley-terry-solve-three-players.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        # Test that the skill ratings come out in the right order.
        self.assertGreater(p[0], 0)
        self.assertGreater(p[1], p[0])
        self.assertGreater(p[2], p[1])
        self.assertLess(p[2], 1)

    def test_solve_ten_players(self):
        trials = 1000
        skills = [(i + 1) for i in range(10)]
        outcomes = bradley_terry.GenerateRandomGameOutcomes(skills, trials)
        report = 'bradley-terry-solve-ten-players.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertGreater(p[0], 0)
        self.assertLess(p[9], 1)
        # Top players should at least be ahead of the player ranked 5 behind.
        for i in range(5, 10):
            self.assertGreater(p[i], p[i - 5])

    def test_solve_hundred_players_dense(self):
        trials = 10 * 1000
        skills = [(i + 1) for i in range(100)]
        outcomes = bradley_terry.GenerateRandomGameOutcomes(skills, trials)
        report = 'bradley-terry-solve-hundred-players-dense.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertGreaterEqual(p[0], 0)
        self.assertLessEqual(p[99], 1)
        self.assertLess(sum(p[:50]), sum(p[50:]))

    def test_solve_hundred_players_sparse(self):
        trials = 500
        skills = [(i + 1) for i in range(100)]
        outcomes = bradley_terry.GenerateRandomGameOutcomes(skills, trials)
        report = 'bradley-terry-solve-hundred-players-sparse.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertGreaterEqual(p[0], 0)
        self.assertLessEqual(p[99], 1)
        self.assertLess(sum(p[:50]), sum(p[50:]))

    def test_solve_one_game(self):
        outcomes = [(1, 0)]
        report = 'bradley-terry-solve-one-game.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertLess(p[0], 0.5)
        self.assertGreater(p[1], 0.5)

    def test_solve_two_players_cycle(self):
        outcomes = [(1, 0), (0, 1)]
        report = 'bradley-terry-solve-two-players-cycle.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        self.assertAlmostEqual(p[0], 0.5, 3)
        self.assertAlmostEqual(p[1], 0.5, 3)

    def test_solve_three_players_cycle(self):
        outcomes = [(0, 1), (1, 2), (2, 0)]
        report = 'bradley-terry-solve-three-players-cycle.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        one_third = float(1) / 3
        self.assertAlmostEqual(p[0], one_third, 3)
        self.assertAlmostEqual(p[1], one_third, 3)
        self.assertAlmostEqual(p[2], one_third, 3)

    def test_solve_four_players(self):
        # Players 0, 1, and 2 are in a cycle, and 0 beats 3.
        outcomes = [(0, 1), (1, 2), (2, 0), (0, 3)]
        report = 'bradley-terry-solve-four-players.csv'
        p = bradley_terry.EstimateSkillRatingsFromGameOutcomes(outcomes, report)
        one_third = float(1) / 3
        self.assertAlmostEqual(p[0], one_third, 3)
        self.assertAlmostEqual(p[1], one_third, 3)
        self.assertAlmostEqual(p[2], one_third, 3)
        self.assertAlmostEqual(p[3], 0, 3)

if __name__ == '__main__':
    unittest.main()
