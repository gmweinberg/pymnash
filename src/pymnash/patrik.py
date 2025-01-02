#!/usr/bin/env python
"""Patrik is described here
   https://www.reddit.com/r/GAMETHEORY/comments/1h4f26q/help_with_calculating_the_nash_equilibrium_for_my/
   the name comes because I heard about it from a guy who heard about it from a guy, and one of those
   guys is named Patrik"""
from math import isqrt
import numpy as np
from .node import Node
from .nash_dag import Nash_DAG

class Patrik(Nash_DAG):
    def generate_node(self, name):
        terminal = False
        scores = None
        if name[0] is not None:
            terminal = True
            if name[0] == 0:
                scores = [1, 0]
            else:
                scores = [0, 1]
        node = Node(name, terminal=terminal, scores=scores)
        return node


    def get_successors(self, node):
        """For this game the node name is a tuple.
        The element 0 is the winner at this node, 0, 1, or None. Unless
        it is none, there are no more elements.
        The element 1 is the value chosen by the coin player.
        The element 2 is the value chosen by the guesser.
        If these are the same, there are no more elements (only child is guesser wins)
        Element 3 is number of guesses made (prior to this node)
        Element 4 is a boolean indicating 0 has been guessed
        Element 5 is highest non-zero number previously guessed (None initially)"""
        name = node.name
        if name[0] is not None:
            return []
        result = []
        if name[1] is None: # special root node is (None, None, None)
            for cp in range(6):
                for gp in range(6):
                    if cp == gp:
                        result.append((None, cp, gp))
                    else:
                        result.append((None, cp, gp, 0, False, None))
            return result
        if name[1] == name[2]:
            return [(1,)]
        if name[3] == 2:
            return [(0,)]
        zero_gone = name[1] == 0 or name[4]
        guesses = [] # possible guesses for either player
        if not zero_gone:
            guesses.append(0)
        if name[4] is None:
            for guess in range(1, 5):
                guesses.append(guess)
        else:
            for guess in range(name[4] + 1, 5):
                guesses.append(guess)
        if name[1] == 0:
            highest = name[5]
        else:
            highest = name[1]

        guesses.append(5) # can always guess 5, even if already guessed
        for cp in guesses:
            for gp in guesses:
                newname = (None, cp, gp, name[3] + 1, not zero_gone,  highest)
                result.append(newname)
        return result

    def create_game(self, nodes):
        """Create the pymnash game from the nodes indicating possible succesor states.
           The subgame nodes must already be scored for us to calculate this game scores."""
        stride = isqrt(len(nodes))
        game_array = np.zeros((stride, stride, 2))
        for ii in range(stride):
            for iii in range(stride):
                for iv in range(2):
                    game_array[ii][iii][iv] = nodes[ii * stride + iii].scores[iv]
        thegame = Game(game_array)
        equilibria = [elm for elm in thegame.find_all_equilibria()]
        if len(equilibria) != 1:
            raise Exception("multiple equilibria!")
        equilibrium = equilibria[0]
        print(equilibrium)


