#!/usr/bin/env python
"""A Nash_DAG is a multi-round game where the players move simultaneously.
   The game ends at one of multiple terminal nodes, where each player gets a score.
   At non-terminal nodes the players are assumed to play the nash equilibrium strategy and the
   score of that node for each player is the sum of the probability of each successor node being reached times
   the score for that player of the successor.

"""
from itertools import product as cartesian_product
import numpy as np
from .game import Game
from .node import Node

class Nash_DAG:
    def __init__(self, *args, **kwargs):
        self.nodes = {}
        if "verbose" in kwargs:
            self.verbose = kwargs["verbose"]
        else:
            self.verbose = False
        self.default_start = kwargs.get('default_start')
        self.counter = 0
        self.analyzed = False


    def generate_node(self, key):
        """Create a new node with the given key and add it to the dictionary.
           Subclasses of Nash_DAG should extend this method by correctly setting terminal
           and setting scores on terminal nodes."""
        node_ = Node(key)
        self.nodes[key] = node_
        return node_

    def get_player_actions(self, node) -> list:
        """For each player generate a list of actions that can be generated from this node."""
        raise Exception("Not implemented")

    def get_child(self, node, player_actions) -> tuple:
        """Find the node that results when players lay the given actions at the
           given node. Return the key of the child node."""
        raise Exception("Not implemented""")


    def generate_subgraph(self, node):
        """Create all descendent nodes from the given node.
           This will not score the nodes (except terminal nodes)."""
        all_player_actions = self.get_player_actions(node)
        for actions in cartesian_product(*all_player_actions):
            key = self.get_child(node, actions)
            if key in self.nodes:
                self.nodes[key].parents.add(node)
            else:
                newnode = self.generate_node(key)
                newnode.parents.add(node.key)
                self.nodes[key] = newnode
                if self.verbose:
                    print("new key", newnode.key)
                self.generate_subgraph(newnode)

    def set_subscores(self, node, layer=0):
        """Set scores on all descendent nodes of this node.
           Subgraph must already have been generated."""
        if node.scores is not None:
            return True
        if self.set_scores(node):
            return True
        print("set subscores node", node.key, "layer", layer)
        all_player_actions = self.get_player_actions(node)
        for actions in cartesian_product(*all_player_actions):
            key = self.get_child(node, actions)
            child = self.nodes[key]
            done_child = False
            while not done_child:
                done_child = self.set_subscores(child, layer+1)


    def set_scores(self, node)->bool:
        """Set the scores on this node if all its child nodes have scores.
           Returns a boolean indicating scores were set."""
        if node.key not in self.nodes:
            raise Exception("Unknown node {}".format(node.key))
        if node.scores is not None:
            return True
        all_player_actions = self.get_player_actions(node)
        indices = [range(len(actions)) for actions in all_player_actions]
        shape = [len(actions) for actions in all_player_actions]
        shape.append(len(all_player_actions))
        shape = tuple(shape)
        game_array = np.zeros(shape)
        # for where we want the index of the action, not the action itself
        for action_indices in cartesian_product(*indices):
            actions = [sublist[i] for i, sublist in zip(action_indices, all_player_actions)]
            key = self.get_child(node, actions)
            child = self.nodes[key]
            if child.scores is None:
                return False
            for ii in range(len(child.scores)):
                where = list(action_indices)
                where.append(ii)
                game_array[tuple(where)] = child.scores[ii]
        thegame = Game(game_array)
        equilibria = [equilibrium for equilibrium in thegame.find_all_equilibria()]
        # In principle we can still set scores with multiple n.e. as long as all the n.e.
        # give the same returns to all players.
        if len(equilibria) != 1:
            print("equilibria", equilibria)
            raise Exception("This only works with a unique nash equilibrium")
        equilibrium = equilibria[0]
        if self.verbose:
            print("node", node.key, "equilibrium", equilibrium)
        player_probs = []
        for actions, probs in zip(all_player_actions, equilibrium):
            pa_dict = {}
            for new_key, old_key in zip(actions, range(len(probs))):
                pa_dict[new_key] = probs[old_key]
                player_probs.append(pa_dict)
        node.playerprobs = player_probs
        # we should factor something like tge below into game
        scores = [0] * len(all_player_actions)
        key_sets = [d.keys() for d in equilibrium]
        for keys in cartesian_product(*key_sets):
            values = tuple(equilibrium[i][k] for i, k in enumerate(keys))
            mult = np.prod(values)
            for ii in range(len(all_player_actions)):
                where = list(keys)
                where.append(ii)
                scores[ii] += mult * game_array[tuple(where)]
        node.scores = scores

        return True
