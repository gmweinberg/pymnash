#!/usr/bin/python

"""Question from reddit https://www.reddit.com/r/GAMETHEORY/comments/178eqbx/is_my_translation_into_matrix_form_correct/"""
import numpy as np
import argparse

import json
from fractions import Fraction
from game import Game

def negadd():
    payoffs = np.zeros((3,3,2))
    for a1 in [0, 1, 2]:
        for a2 in [0, 1, 2]:
            payoffs[((a1, a2, 0))] = a1 + a1 * a2 - (2 * a2 + a1 * a1)
            payoffs[((a1, a2, 1))] = a2 + a1 * a2 - (2 * a1 + a2 * a2)
    #print(payoffs.shape)
    return Game(payoffs)

if __name__ == '__main__':
    theGame = negadd()
    print(repr(theGame.find_all_equilibria()))
