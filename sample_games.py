#!/usr/bin/python
import numpy as np
import argparse

from game import Game
from util import coords_from_pos



"""Process some test games to verify we can find their equilibria."""

def battle_of_genders(n):
    """A generalization of the 'battle of the sexes' game which supports any number of genders. The number of possible moves for each player
       is equal to the total number of players. All players get zero payoff unless they all coordinate on a choice, each player has a particular favorite choice
        but all players get something as long as they all coordinate."""
    # We know there is one pure strategy per player, with all players playing that player's favorite.
    # We also know there is at least one mixed strategy
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
    print(boga)


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
    print(thearray)



def matching_pennies(n):
    """For n player matching pennies each player can choose a number in the range 0 to n -1, and player m wins if the result is m modulo n.
       For the 2 x 2 case think of heads as zero and tails as 1, so player 0 wins with HH or TT, player 1 wins with HT or TH"""
    thearray = np.zeros(tuple([n] * (n + 1)), dtype=float)
    for ii in range(np.prod(thearray.shape)):
        coords = coords_from_pos(thearray, ii)
        player = coords[ n ] # index of the player we are looking at
        sum_played = sum(coords[:-1])
        if sum_played % n == player:
            thearray[coords] = n - 1
        else:
            thearray[coords] = -1
    print(thearray)
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    #prisoners_dilemma(2)
    print()

    #prisoners_dilemma(3)
    print()

    matching_pennies(3)


