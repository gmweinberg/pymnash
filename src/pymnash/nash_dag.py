#!/usr/bin/env python
"""A Nash_DAG is a multi-round game where the players move simultaneously.
   The game ends at one of multiple terminal nodes, where each player gets a score.
   At non-terminal nodes the players are assumed to play the nash equilibrium strategy and the
   score of that node for each player is the sum of the probability of each successor node being reached times
   the score for that player of the successor.

"""

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


    def generate_node(self, name):
        """Create a new node with the given name and add it to the dictionary.
           Subclasses of Nash_DAG should extend this method by correctly setting terminal
           and setting scores on terminal nodes."""
        node_ = Node(name)
        self.nodes[name] = node_
        return node_

    def get_successors(self, node):
        """Get all nodes that can be reached from the given node."""
        raise Exception("Not implemented""")


    def generate_subgraph(self, node):
        for name in self.get_successors(node):
            if name not in self.nodes:
                node = self.generate_node(name)
                self.nodes[name] = node
                self.generate_subgraph(node)


    def create_game(self, nodes):
        """Create a game from a set of nodes. The nodes must already have
           scores before this node is called."""
        raise Exception("Not implemented")

    def generate_scores(self, node):
        """Set the scores on this node and all nodes below which are not yet scored.
           Call generate subgraph first."""
        if node.scores is not None:
            return
        nodes = []
        penultimate = False
        for name in self.get_successors(node):
            node = self.nodes[name]
            if node.terminal:
                penultimate = True
            if node.scores is not None:
                self.generate_scores(node)
            nodes.append(node)
        if penultimate:
            pass
        try:
            thegame = self.create_game(nodes)
        except Exception:
            print("wftf")
        equilibria = [equilibrium for equilibrium in thegame.find_all_equilibria()]
        if len(equilibria) != 1:
            raise Exception("This only works with a unique nash equilibrium")
        equilibrium = equilibria[1]
        raise Exception("Got here :-)")
