#!/usr/bin/env python
from argparse import ArgumentParser
from ast import literal_eval
from pymnash.patrik import Patrik, describe_key
from pymnash.node import Node

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--node", help="node key to show values for")
    #parser.add_argument("--actions", help="show player actions at given node", action="store_true")
    parser.add_argument("--childs", help="show child nodes of given node", action="store_true")
    parser.add_argument("--score", help="attempt to score given node", action="store_true")
    parser.add_argument("--solve", help="solve from node", action="store_true")
    parser.add_argument("--count", help="count total number of nodes", action="store_true")
    parser.add_argument("--verbose", help="verbose", action="store_true")
    args = parser.parse_args()
    thegame = Patrik(verbose=args.verbose)
    # print("nodes", thegame.nodes)

    if args.count:
        print("node count {}".format(len(thegame.nodes)))

    if args.node:
        key = literal_eval(args.node)
    else:
        key = (None,)
    node = thegame.nodes[key]

    if args.childs:
        print("child nodes")
        for key in thegame.get_child_nodes(node):
            print(key)

        #nodename = literal_eval(args.childs)
        #node1 = thegame.nodes[nodename]
        #print("childs:")
        #for name in thegame.get_successors(node1):
        #    print(name, describe_key(name))
    if args.score:
        didit = thegame.set_scores(node)

    if args.solve:
        thegame.set_subscores(node)



# ./test_patrik.py --node (2, 2, 1, False, 3)" --score
