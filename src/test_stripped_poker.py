#!/usr/bin/env python

from itertools import permutations
from collections import defaultdict
from pymnash.game import zero_sum_2_player
from pymnash.stripped_poker import get_stripped_poker_payoffs
from pymnash.util import zero_sum_dict, payout_array_from_dict

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--revealed', help="number of cards revealed to student", default=1, type=int)
    parser.add_argument('--verbose', help="verbose", action='store_true')
    parser.add_argument('--payoffs', help="show payoffs for strategies", action='store_true')
    parser.add_argument('--nash', help="show nash equilibria strategies", action='store_true')
    parser.add_argument('--iesds', help="show dominated strategies", action='store_true')
    args = parser.parse_args()
    payoffs = get_stripped_poker_payoffs(args.revealed)

    if args.payoffs:
        print('payoffs', payoffs)

    if args.nash or args.iesds:
        #zs = zero_sum_dict(payoffs_dict)
        # payoffs = payout_array_from_dict(zs)
        # print('payoffs', payoffs)
        agame = zero_sum_2_player(payoffs)
        agame.verbose = args.verbose
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

# ./test_stripped_poker.py --revealed 2 --nash --payoffs --iesds
