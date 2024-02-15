#!/usr/bin/env python

from itertools import permutations
from collections import defaultdict
import matplotlib.pyplot as plt
from pymnash.game import zero_sum_2_player
from pymnash.stripped_poker import get_stripped_poker_payoffs

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--revealed', help="number of cards revealed to student", default=1, type=int)
    parser.add_argument('--verbose', help="verbose", action='store_true')
    parser.add_argument('--payoffs', help="show payoffs for strategies", action='store_true')
    parser.add_argument('--nash', help="show nash equilibria strategies", action='store_true')
    parser.add_argument('--iesds', help="show dominated strategies", action='store_true')
    parser.add_argument('--plot', help="plot student actions vs dealer mix", action='store_true')
    args = parser.parse_args()
    payoffs = get_stripped_poker_payoffs(args.revealed)
    agame = zero_sum_2_player(payoffs)
    agame.verbose = args.verbose
    all_nash = None

    if args.payoffs:
        print('payoffs', agame.payoffs)
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


    if args.plot:
        if False:
            fig0, ax0 = plt.subplots()
            x_player = (0,0,1)
            y_player = 0
            ps = agame.get_payoffs_slice(x_player, y_player)
            for aslice in ps:
                ax0.plot([0, 1], aslice)
            # plt.show()

        if True:
            fig1, ax1 = plt.subplots()
            xind = 1
            action0 = 0
            action1 = 1
            x_player = (xind, action0, action1)
            y_player = 0
            ps = agame.get_payoffs_slice(x_player, y_player)
            for aslice in ps:
                ax1.plot([0, 1], aslice)
            if all_nash:
                for anash in all_nash:
                    if anash[xind].get(action1):
                        pass
                        ax1.plot([anash[xind][action1], anash[xind][action1]], [aslice[0], aslice[1]])
        plt.show()

# ./test_stripped_poker.py --revealed 2 --nash --payoffs --iesds
