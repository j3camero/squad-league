import csv
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

# Does one iteration of the algorithm to solve the Bradley Terry model.
# p is any vector of numbers all between 0 and 1. w is a the win matrix such
# that w[i][j] is the number of times that i beat j. The return value is a
# estimate of the skill values for each player. Calling this function
# iteratively solves the Bradley Terry model.
def OneIteration(p, w):
    new_p = []
    for i in range(len(p)):
        numer = 0
        denom = 0
        for j in range(len(p)):
            if i == j:
                continue
            if p[i] + p[j] == 0:
                continue
            numer += w[i][j]
            denom += (w[i][j] + w[j][i]) / (p[i] + p[j])
        if denom > 0:
            new_p.append(float(numer) / denom)
        else:
            new_p.append(0)
    return Normalize(new_p)

# Estimate the skill rating of each player given a list of (winner, loser)
# pairs. Works by iteratively calling OneIteration(p, w).
#   outcomes - a list of game outcomes in the form [(winner, loser), ...]
#   convergence_report_filename_csv - (optional) write a report in CSV format.
# Returns a list of the estimated skill rating for each player.
def EstimateSkillRatingsFromGameOutcomes(
        outcomes,
        convergence_report_filename_csv=None):
    n = max(max(winner, loser) for winner, loser in outcomes) + 1
    w = [[0 for j in range(n)] for i in range(n)]
    for winner, loser in outcomes:
        w[winner][loser] += 1
    report = None
    csv_writer = None
    p = Normalize([random.random() for i in range(n)])
    if convergence_report_filename_csv:
        report = open(convergence_report_filename_csv, 'wb')
        csv_writer = csv.writer(report)
        player_names = ['p' + str(i) for i in range(n)]
        csv_writer.writerow(['iteration', 'max_diff'] + player_names)
        csv_writer.writerow([0, 1] + p)
    stop_threshold = 0.0001
    i = 0
    while True:
        i += 1
        old_p = p
        p = OneIteration(p, w)
        max_diff = max(abs(a - b) for a, b in zip(p, old_p))
        if report:
            csv_writer.writerow([i, max_diff] + p)
        if max_diff < stop_threshold:
            break
    if report:
        report.close()
    return p
