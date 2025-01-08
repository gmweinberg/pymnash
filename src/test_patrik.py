#!/usr/bin/env python
from argparse import ArgumentParser
from ast import literal_eval
from pymnash.patrik import Patrik, nodename, describe_node
from pymnash.node import Node

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--childs", help="show child nodes of given node")
    parser.add_argument("--score", help="attempt to score given node")
    parser.add_argument("--count", help="count number nof nodes", action="store_true")
    args = parser.parse_args()
    thegame = Patrik()
    # print("nodes", thegame.nodes)

    thegame.generate_subgraph(thegame.nodes[(None, None, None)])

    if args.count:
        print("node count {}".format(len(thegame.nodes)))
    if args.childs:
        nodename = literal_eval(args.childs)
        node1 = thegame.nodes[nodename]
        print("childs:")
        for name in thegame.get_successors(node1):
            print(name, describe_node(name))
    if args.score:
        nodename = literal_eval(args.score)
        node2 = thegame.nodes[nodename]
        didit = thegame.set_scores(node2)
        if not didit:
            print("Initial attempt failed, setting child scores")
            for subname in thegame.get_successors(node2):
                subnode = thegame.nodes[subname]
                thegame.set_scores(subnode)
            thegame.set_scores(node2)
        wtf = "wtf"




# ./test_patrik --childs "(None,None,None)"
# ./test_patrik --childs (None, 0, 1, 1, False, 1)"
