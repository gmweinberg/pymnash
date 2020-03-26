#!/usr/bin/python
import numpy as np
import argparse

from fractions import Fraction
from game import Game
from util import coords_from_pos

"""Process some test games to verify we can find their equilibria."""
prisoner_labels = ['capone', 'number6', 'hogan']
prisoner_actions = ['C', 'D'] # cooperate, defect

def battle_of_genders(n):
    """A generalization of the 'battle of the sexes' game which supports any number of genders. The number of possible moves for each player
       is equal to the total number of players. All players get zero payoff unless they all coordinate on a choice, each player has a particular favorite choice
        but all players get something as long as they all coordinate."""
    # We know there is one pure strategy per player, with all players playing that player's favorite.
    # There will also be one mixed  strategy for ever combination of pure strategies 
    boga = np.zeros(tuple([n] * (n + 1)), dtype=float)
    #print(boga)
    for ii in range(n):
        loc = boga
        for jj in range(n):
            loc = loc[ii]
        for kk in range(n):
            if kk == ii:
                loc[kk] = n
            else:
                 loc[kk] = 1
    return Game(boga)


def prisoners_dilemma(n):
    """For the multiplayer prisoner's dilemma we will say if everone cooperates then each person gets a -1 payoff.
       If exactly one player defectes he gets 0 and everyone else gets -5.
       If multiple player defect, the ones that defect get -3 and the ones that cooperate get -5.
    """
    # We will say for ever player choice '0' is cooperate and '1' is defect.
    # The innermost array is player id for payoffs
    # We know the only nash equilibrium is everybody defects.
    thearray = np.zeros(tuple(([2] * n + [n])), dtype=float)
    for ii in range(np.prod(thearray.shape)):
        coords = coords_from_pos(thearray, ii)
        player = coords[ n ] # index of the player we are looking at 
        he_defected = bool(coords[player])
        total_defected = sum(coords[:-1])
        if total_defected == 0:
            thearray[coords] = -1
        elif he_defected and total_defected  == 1:
            thearray[coords] = 0
        elif he_defected:
             thearray[coords] = -3
        else:
             thearray[coords] = -5
    return Game(thearray, prisoner_labels)



def matching_pennies(n):
    """For n player matching pennies each player can choose a number in the range 0 to n -1, and player m wins if the result is m modulo n.
       For the 2 x 2 case think of heads as zero and tails as 1, so player 0 wins with HH or TT, player 1 wins with HT or TH"""
    # The obvious equilibrium is everyone plays randomly. But there are many possibilities for multiple players. In the 3 player version, if 2 players
    # play randomly, the other player can play anything and it's still an equilibrium. As long as at least one player is playing randomly it doesn't really matter what the
    # other players do, but just one player randomising would not be an equilibrium.
    thearray = np.zeros(tuple([n] * (n + 1)), dtype=float)
    for ii in range(np.prod(thearray.shape)):
        coords = coords_from_pos(thearray, ii)
        player = coords[ n ] # index of the player we are looking at
        sum_played = sum(coords[:-1])
        if sum_played % n == player:
            thearray[coords] = n - 1
        else:
            thearray[coords] = -1
    #print(thearray)
    return Game(thearray)
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=3)
    parser.add_argument('--game', default='battle_of_genders')
    args = parser.parse_args()
    agame = None
    if args.game == 'matching_pennies':
        agame = matching_pennies(args.players)
        # for a test we will have 2 players randomize and everyone else will play pure strategies 
        frac = Fraction(1, args.players)
        profile = [[frac] * args.players, [frac] * args.players] + [[1] + [0] * (args.players - 1)] * (args.players - 2) # python 2 not supported!
        print('profile', profile)
    # print(agame.payoffs)
    print(agame.is_nash(profile))

    #prisoners_dilemma(2)
    print()

    #print(repr(prisoners_dilemma(3)))
    print()

    #print(repr(matching_pennies(3)))


