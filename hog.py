"""The Game of Hog."""
#Partner: Marcus Lee

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    sum, if_one_appears = 0, False # initialization
    while num_rolls > 0:
        current_dice = dice()
        if current_dice == 1:
            if_one_appears = True # this is based on the "Pig Out" rule
        sum += current_dice
        num_rolls -= 1
    if if_one_appears:
        return 1
    return sum  
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        return 1 + max(opponent_score % 10, opponent_score // 10) # Breaks down number into digits, find max digit
    return roll_dice(num_rolls, dice)
    # END Question 2

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3

def is_swap(score0, score1):
    """Return True if ending a turn with SCORE0 and SCORE1 will result in a
    swap.

    Swaps occur when the last two digits of the first score are the reverse
    of the last two digits of the second score.
    """
    # BEGIN Question 4
    return ((score0 - (score0 // 100) * 100) % 10 == (score1 - (score1 // 100) * 100) // 10) and \
            ((score0 - (score0 // 100) * 100) // 10 == (score1 - (score1 // 100) * 100) % 10)
    # First line compares last digit of score0 with first digit of score1
    # Second line compares first digit of score0 with second digit of score1
    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1

    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """

    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    while (score0 < goal) and (score1 < goal):
        if who == 0: # Player 0's turn
            score0 += take_turn(strategy0(score0, score1), score1, select_dice(score0, score1))
        else: # Player 1's turn
            score1 += take_turn(strategy1(score1, score0), score0, select_dice(score1, score0))
        if is_swap(score0, score1):
            score0, score1 = score1, score0

        who = other(who)

    # END Question 5
    return score0, score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    # BEGIN Question 6
    
    def make_averaged_return(*arg):
        result = 0
        count = 0
        while num_samples > count:
            result += fn(*arg)
            count += 1
        return result / num_samples    
    return make_averaged_return
    # END Question 6

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    average_score = make_averaged(roll_dice, num_samples) # average score will return the average score for rolling num_dice number of dice
    average_roll_list = [average_score(num_dice, dice) for num_dice in range(1, 11)] # average_roll_list complies the average scores of rolling 1-10 dice num_samples of times into a list
    return average_roll_list.index(max(average_roll_list)) + 1 # and then we just find the index of the high average score (+1 due to Python's counting from 0)
    # END Question 7

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    if take_turn(0, opponent_score) >= margin:
        return 0
    return num_rolls # Replace this statement
    # END Question 8

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS if rolling 0 dice results in a harmful swap. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    # BEGIN Question 9
    free_bacon_score = take_turn(0, opponent_score) + score # the score you'd get from using free bacon
    if is_swap(free_bacon_score, opponent_score):
        if free_bacon_score > opponent_score: # harmful swap
            return num_rolls
        elif free_bacon_score < opponent_score: # beneficial swap
            return 0
        else: # neutral result
            return bacon_strategy(score, opponent_score, margin, num_rolls)
    else: # swap does not occur
        return bacon_strategy(score, opponent_score, margin, num_rolls)
    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN Question 10
    margin = 8

    if score > 67:
        margin = 3

    if 0 == swap_strategy(score, opponent_score, margin):
        return 0
    # print ("Exit123")
    return 6 # Replace this statement
    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--final', action='store_true',
                        help='Display the final_strategy win rate against always_roll(5)')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
    elif args.final:
        from hog_eval import final_win_rate
        win_rate = final_win_rate()
        print('Your final_strategy win rate is')
        print('    ', win_rate)
        print('(or {}%)'.format(round(win_rate * 100, 2)))
