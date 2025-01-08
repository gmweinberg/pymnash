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


    def generate_node(self, key):
        """Create a new node with the given key and add it to the dictionary.
           Subclasses of Nash_DAG should extend this method by correctly setting terminal
           and setting scores on terminal nodes."""
        node_ = Node(key)
        self.nodes[key] = node_
        return node_

    def get_successors(self, node):
        """Get all nodes that can be reached from the given node."""
        raise Exception("Not implemented""")


    def generate_subgraph(self, node):
        for key in self.get_successors(node):
            if key in self.nodes:
                self.nodes[key].parents.add(node.key)
            else:
                newnode = self.generate_node(key)
                newnode.parents.add(node.key)
                self.nodes[key] = newnode
                if self.verbose:
                    print("new key", newnode.key)
                self.generate_subgraph(newnode)


    def create_game(self, nodes):
        """Create a game from a list of nodes. The nodes must already have
           scores before this node is called."""
        raise Exception("Not implemented")

    def set_scores(self, node)->bool:
        """Set the scores on this node if all its child nodes have scores.
           Returns a boolean indicating scores were set."""
        if node.key not in self.nodes:
            raise Exception("Unknown node {}".format(node.key))
        childs = 0
        nodes = []
        for key in self.get_successors(node):
            child = self.nodes[key]
            if child.scores is None:
                return False
            childs += 1
            nodes.append(child)
        if childs == 1:
            node.scores = child.scores
            # print("just 1 child") 
            return True
        thegame = self.create_game(nodes)
        equilibria = [equilibrium for equilibrium in thegame.find_all_equilibria()]
        if len(equilibria) != 1:
            raise Exception("This only works with a unique nash equilibrium")
        equilibrium = equilibria[0]
        print(equilibrium)
