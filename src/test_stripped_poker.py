#!/usr/bin/env python

from itertools import permutations
from collections import defaultdict
from pymnash.game import zero_sum_2_player

def get_stripped_poker_payoffs(revealed):
    """Find the payoffs for the dealer for each player strategy with the number of revelaed cards.
       Player strategy is characterized by the number of revealed kings required to call (zero means always
       call, if we require more than revealed player will never call. It makes no sense not to call if we see 4
       kings, so we won;t bother checking n > 4."""
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




if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--revealed', help="number of cards revealed to student", default=1, type=int)
    parser.add_argument('--payoffs', help="show payoffs for strategies", action='store_true')
    parser.add_argument('--nash', help="show nash equilibria strategies", action='store_true')
    parser.add_argument('--iesds', help="show dominated strategies", action='store_true')
    args = parser.parse_args()
    payoffs = get_stripped_poker_payoffs(args.revealed)

    if args.payoffs:
        for key in payoffs:
            print(key, payoffs[key])

    if args.nash or args.iesds:
        payoffs = _game_format_payoffs(payoffs)
        # print('payoffs', payoffs)
        agame = zero_sum_2_player(payoffs)
    if args.nash:
        all_nash = agame.find_all_equilibria()
        print('nash')
        for anash in all_nash:
            print(anash)
            # anash looks like [{0: 4/9, 1: 5/9}, {0: 2/9, 1: 7/9}]
            profile = []
            for elm in anash:
                profile.append([(key, elm[key]) for key in elm])
            print(agame.get_profile_payoffs(profile))
    if args.iesds:
        agame.iesds()
        print('dominated strategies:')
        print(agame.dominated)
