import random

# The classic Bradley-Terry model.
#   a - the skill level of player A.
#   b - the skill level of player B.
# Returns True if A wins, False if B wins. The random probability is based on
# a coin flip with probability p = a / (a + b). There are no draws allowed; one
# player or the other must win.
def GenerateOneRandomGameOutcome(a, b):
    return random.random() < float(a) / float(a + b)

# Generate a list of game outcomes, in the form [(winner_id, loser_id), ...]
def GenerateRandomGameOutcomes(skill_levels, n):
    player_ids = range(len(skill_levels))
    outcomes = []
    for i in range(n):
        j, k = random.sample(player_ids, 2)
        if GenerateOneRandomGameOutcome(skill_levels[j], skill_levels[k]):
            outcomes.append((j, k))
        else:
            outcomes.append((k, j))
    return outcomes

# Returns a new vector whose items sum to 1.
def Normalize(skill_levels):
    divisor = sum(skill_levels)
    return [float(p) / divisor for p in skill_levels]
