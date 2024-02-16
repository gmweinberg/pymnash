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
    parser.add_argument('--plot-student', help="plot student actions vs dealer mix", action='store_true', 
                        dest='plot_student')
    parser.add_argument('--plot-dealer', help="plot dealer actions vs nash student mix", action='store_true', 
                        dest='plot_dealer')
    parser.add_argument('--file', help="file to save plot", default=None)
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


    if args.plot_student:
        if not all_nash:
            all_nash = agame.find_all_equilibria() # there's just one
        xind = 0
        yind = 1
        xactions = [key for key in all_nash[0][xind]]
        yactions = [key for key in all_nash[0][yind]]
        x_player = (xind, xactions[0], xactions[1])
        ps = agame.get_payoffs_slice(x_player, yind)
        fig0, ax0 = plt.subplots()
        y_player =  1
        min_y = max_y = None
        for aslice in ps:
            ax0.plot([0, 1], aslice)
            if min_y is None or aslice[0] < min_y:
                min_y = aslice[0]
            if aslice[1] < min_y:
                min_y = aslice[1]
            if max_y is None or aslice[0] > max_y:
                max_y = aslice[0]
            if aslice[1] > max_y:
                max_y = aslice[1]
        ax0.plot([all_nash[0][xind][xactions[1]], anash[xind][xactions[1]]], [min_y, max_y])
        plt.show()
        if args.file:
            fig0.savefig(args.file, transparent=False)

    if args.plot_dealer:
        if not all_nash:
            all_nash = agame.find_all_equilibria() # there's just one
        xind = 1
        yind = 0
        xactions = [key for key in all_nash[0][xind]]
        yactions = [key for key in all_nash[0][yind]]
        x_player = (xind, xactions[0], xactions[1])
        ps = agame.get_payoffs_slice(x_player, yind)
        fig0, ax0 = plt.subplots()
        y_player =  1
        min_y = max_y = None
        for aslice in ps:
            ax0.plot([0, 1], aslice)
            if min_y is None or aslice[0] < min_y:
                min_y = aslice[0]
            if aslice[1] < min_y:
                min_y = aslice[1]
            if max_y is None or aslice[0] > max_y:
                max_y = aslice[0]
            if aslice[1] > max_y:
                max_y = aslice[1]
        ax0.plot([all_nash[0][xind][xactions[1]], anash[xind][xactions[1]]], [min_y, max_y])
        plt.show()
        if args.file:
            fig0.savefig(args.file, transparent=False)


# ./test_stripped_poker.py --revealed 2 --nash --payoffs --iesds
