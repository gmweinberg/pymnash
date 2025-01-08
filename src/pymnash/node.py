#
"""Node is just a data structure.
   Name is an identifier to use in a dictionary.
   Terminal indicates it is a terminal node.
   Scores is a list of player scores at this node.
"""
class Node:
    def __init__(self, key, terminal=False, scores = None):
        self.key = key
        self.terminal = terminal
        self.scores = scores
        self.parents = set()
        self.probs = None




