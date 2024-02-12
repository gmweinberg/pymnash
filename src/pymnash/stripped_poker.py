#!/usr/bin/env python

"""The stripped poker game in this package is based on this reddit thread
   https://www.reddit.com/r/GAMETHEORY/comments/1ak4wmc/question_on_strippeddown_poker/
   I have modified it so the number of cards revealed to the player can range from 0-7
"""
   

from itertools import permutations
from collections import defaultdict

def get_stripped_poker_payoffs(revealed):
    """Find the payoffs for the dealer for each player strategy with the number of revelaed cards.
       Player strategy is characterized by the number of revealed kings required to call (zero means always
       call, if we require more than revealed player will never call. It makes no sense not to call if we see 4
       kings, so we won;t bother checking n > 4.
       Returns a payoff dict where the key is a tuple (dealer action, player action) and the value
       is the 14 round payoff for that matrix element.
    """
    payoffs = defaultdict(int)
    seen = defaultdict(int)
    total = 0
    seq = ['K', 'K', 'K', 'K', 'Q', 'Q', 'Q', 'Q']
    for perm in permutations(seq):
        total += 1
        for dealer in ("B", "F"):
            kings = sum([1 for ii in range(1, revealed + 1) if perm[ii] == 'K']) # seen by player
            seen[kings] += 1
            for student in range(0, min(revealed + 2, 5)):
                if perm[0] == 'K':
                    if kings >= student:
                        payoffs[(dealer, student)] += 2
                    else:
                        payoffs[(dealer, student)] += 1
                else:
                    if dealer == 'F':
                        payoffs[(dealer, student)] -= 1
                    else:
                        if kings >= student:
                            payoffs[(dealer, student)] -= 2
                        else:
                            payoffs[(dealer, student)] += 1 # bluff succeeds
    for key in payoffs:
        payoffs[key] = 14 * payoffs[key] / total
    # print("seen", seen)
    payoffs = _game_format_payoffs(payoffs)
    return payoffs

def _game_format_payoffs(payoffs):
    """Reformat the payoffs as returned above in a manner pleasing to zero_sum_2_player"""
    student = set()
    for key in payoffs.keys():
        student.add(key[1])
    student = sorted(list(student))
    new = []
    for dealer in 'B', 'F':
        elm = []
        new.append(elm)
        for stud in student:
            elm.append(payoffs[(dealer, stud)])
    return new



