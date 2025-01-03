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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nodename = (None, None, None)
        node = self.generate_node(nodename)
        self.generate_subgraph(node)

    def generate_node(self, name):
        terminal = False
        scores = None
        if name[0] is not None:
            terminal = True
            if name[0] == 0:
                scores = [1, 0]
            else:
                scores = [0, 1]
        node_ = Node(name, terminal=terminal, scores=scores)
        self.nodes[name] = node_
        return node_


    def get_successors(self, node):
        """For this game the node name is a tuple.
        The element 0 is the winner at this node, 0, 1, or None. 
           Unless it is none, there are no more elements.
        The element 1 is the value chosen by the coin player.
        The element 2 is the value chosen by the guesser.
           If these are the same, the only child is guesser wins
        Element 3 is number of guesses made (prior to node)
        Element 4 is a boolean indicating 0 has been guessed
        Element 5 is lowest int that could have been played at this node"""
        name = node.name
        if name[0] is not None: # terminal nodes
            return []
        result = []
        if name[1] is None: # special root node is (None, None, None)
            for cp in range(6):
                for gp in range(6):
                    result.append((None, cp, gp, 0, False, 1))
            return result
        coin = name[1]
        guesser = name[2]
        if coin == guesser:
            return [(1,)]
        guesses_made = name[3]
        if guesses_made == 2:
            return [(0,)]
        zero_gone = name[1] == 0 or name[4]
        min_guess = name[5]
        if coin is not None and coin >= min_guess:
            min_guess = coin + 1
        
        guesses = [] # possible guesses for either player
        if not zero_gone:
            guesses.append(0)
        for guess in range(min_guess, 5):
            guesses.append(guess)

        guesses.append(5) # can always guess 5, even if already guessed
        for cp in guesses:
            for gp in guesses:
                newname = (None, cp, gp, guesses_made + 1, zero_gone,  min_guess)
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

def nodename(coin, guesser, guesses, zero_gone, min_guess=1) -> tuple:
    """Helper function for creating nodename from human-readable values"""
    if coin == guesser:
        return (1,)
    if guesses == 2:
        return (0,)
    return (None, coin, guesser, guesses, zero_gone, min_guess)

def describe_node(name):
    """Helper function for showing nodename as human-readable values"""
    if name[0] is not None:
        if name[0] == 0:
            return "coin wins"
        else:
            return "guesser wins"
    if name[1] is None:
        return "root node"
    coin =  name[1]
    guesser = name[2]
    guesses = name[3]
    zero_gone = name[4]
    min_guess = name[5]
    return "coin={};guesser={};guesses={};zerogone={};min_guess={}".format(*name[1:])


