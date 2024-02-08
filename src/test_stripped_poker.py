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
            for player in range(0, min(revealed + 2, 5)):
                if perm[0] == 'K':
                    if kings >= player:
                        payoffs[(dealer, player)] += 2
                    else:
                        payoffs[(dealer, player)] += 1
                else:
                    if dealer == 'F':
                        payoffs[(dealer, player)] -= 1
                    else:
                        if kings >= player:
                            payoffs[(dealer, player)] -= 2
                        else:
                            payoffs[(dealer, player)] += 1 # bluff succeeds
    for key in payoffs:
        payoffs[key] = 14 * payoffs[key] / total
    print("seen", seen)
    return payoffs


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--revealed', help="number of cards revealed to player", default=1, type=int)
    parser.add_argument('--payoffs', help="show payoffs for strategies", action='store_true')
    args = parser.parse_args()
    payoffs = get_stripped_poker_payoffs(args.revealed)

    if args.payoffs:
        for key in payoffs:
            print(key, payoffs[key])

