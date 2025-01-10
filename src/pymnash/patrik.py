#!/usr/bin/env python
"""Patrik is described here
   https://www.reddit.com/r/GAMETHEORY/comments/1h4f26q/help_with_calculating_the_nash_equilibrium_for_my/
   the name comes because I heard about it from a guy who heard about it from a guy, and one of those
   guys is named Patrik
"""

from math import isqrt
import numpy as np
from .game import Game 
from .node import Node
from .nash_dag import Nash_DAG

class Patrik(Nash_DAG):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        key = (None,)
        node = self.generate_node(key)
        self.generate_subgraph(node)


    def generate_node(self, key):
        if self.verbose:
            print("generating node for key {}".format(key))
        terminal = False
        scores = None
        node_ = Node(key, terminal=terminal, scores=scores)
        self.nodes[key] = node_
        if key == (None,): # special root key
            node_.min_guess = 1
            node_.zero_played = False
            node_.prior_guesses = -1
            return node_
        node_.coin = key[0]
        node_.guesser = key[1]
        node_.prior_guesses = key[2]
        node_.zero_played = key[3]
        node_.min_guess = key[4] # minimum nozero guess that can be played at future nodes
        if node_.coin == node_.guesser:
            node_.terminal = True
            node_.scores = [0, 1]
        else:
            if node_.prior_guesses == 2:
                node_.terminal = True
                node_.scores = [1, 0]
        return node_


    def get_player_actions(self, node_):
        if node_.terminal:
            return [[], []]
        if node_.key == (None,):
            guesses = [ii for ii in range(6)]
            return [guesses, guesses]
        guesses = []
        if not node_.zero_played:
            guesses.append(0)
        min_guess = node_.min_guess
        if node_.coin + 1 > min_guess:
            min_guess = node_.coin + 1
        for ii in range(min_guess, 5):
            guesses.append(ii)
        guesses.append(5)
        return [guesses, guesses]


    def get_child(self, node_, player_actions):
        if player_actions[0] == 0:
            zero_played = True
        else:
            zero_played = node_.zero_played
        if player_actions[0] == 0:
            min_guess = node_.min_guess
        elif player_actions[0] < 5:
            min_guess = player_actions[0] + 1
        else:
            min_guess = 5
        return ((player_actions[0], player_actions[1], node_.prior_guesses + 1, zero_played, min_guess))


def get_key(coin, guesser, guesses, zero_gone, min_guess=1) -> tuple:
    """Helper function for creating key from human-readable values"""
    if coin == guesser:
        return (1,)
    if guesses == 2:
        return (0,)
    return (None, coin, guesser, guesses, zero_gone, min_guess)


def describe_key(key):
    """Helper function for showing key as human-readable values"""
    if key[0] is not None:
        if key[0] == 0:
            return "coin wins"
        else:
            return "guesser wins"
    if key[1] is None:
        return "root node"
    coin =  key[0]
    guesser = key[1]
    guesses = key[2]
    zero_gone = key[3]
    min_guess = key[4]
    return "coin={};guesser={};guesses={};zerogone={};min_guess={}".format(*key[1:])
