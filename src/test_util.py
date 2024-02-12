#!/usr/bin/env python
from itertools import product
from pymnash.util import zero_sum_dict, payout_array_from_dict

def matching_pennies_dict(n):
    """Create a payoff dictionary for n player matching pennies.
       Each player antes 1 and picks a number 0 to n-1, player x wins if sum modul0 n is x"""
    payoffs = {}
    actions =  [[ii for ii in range(n)] for iii in range(n)]
    #print(actions)
    for anaction in product(*actions):
        #print(anaction)
        payoff = [n-1 if sum(anaction) % n == ii else -1 for ii in range(n)]
        key = tuple([anaction[ii] for ii in range(len(anaction))])
        payoffs[key] = payoff
    return payoffs






if __name__ == '__main__':
    mp = matching_pennies_dict(3)
    #print('mp,', mp)
    payoffs = payout_array_from_dict(mp)
    print('payoffs', payoffs)


