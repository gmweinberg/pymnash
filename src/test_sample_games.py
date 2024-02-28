#!/usr/bin/python

"""Functions to create some sample test games"""

from collections import defaultdict
import argparse

from pymnash.sample_games import *

game_names = {"battle_of_genders":battle_of_genders, "reducible":reducible, "combo_reducible":combo_reducible,
               "dunderheads":dunderheads, "prisoners_dilemma":prisoners_dilemma, "matching_pennies":matching_pennies,
              "how_low_dare_you_go":how_low_dare_you_go, "mixed_dom":mixed_dom, 'chicken':chicken,
              'stag_hunt':stag_hunt, 'detente_of_genders':detente_of_genders, 'all_pay_auction':all_pay_auction}

m_games = [how_low_dare_you_go, mixed_dom, stag_hunt, detente_of_genders, all_pay_auction,
          ]


def get_game_fun(name):
    """Find the factory function based on the game name"""
    if name in game_names:
        return game_names[name]
    for game_name in game_names.keys():
        if game_name.startswith(name):
            return game_names[game_name]
    raise ValueError("Unknown game {}".format(name))

def get_canned_profile(fun, num_players):
    """Return a sample strategy profile for the game."""
    if fun == battle_of_genders:
        inner = [0] * num_players
        profile = [list(inner) for ii in range(num_players)]
        for ii in range(num_players):
            profile[ii][ii] = 1
        return profile
    if fun == dunderheads:
        aroot = 3.0 ** (1/(num_players - 1.0))
        profile = [[1 / (aroot + 1), aroot/(aroot + 1)]] * num_players
        return profile
    if fun == reducible:
        profile = [[1, 0, 0]] * 2 +  [[1, 0]] * (num_players - 2)
        return profile
    if fun == matching_pennies:
        frac = 1 / num_players
        profile = [[frac] * num_players,
                   [frac] * num_players] + [[1] + [0] * (num_players - 1)] * (num_players - 2)
        return profile

    raise Exception("Unsupported")

if __name__ == '__main__':
    from argparse import ArgumentParser
    from ast import literal_eval
    parser = ArgumentParser()
    parser.add_argument('--players', help = "number of players", type=int, default=3)
    parser.add_argument('--m', type=int, default=None, help="integer parameter that exists for some games")
    parser.add_argument('--game', help="game name", default='battle_of_genders')
    parser.add_argument('--pure', action='store_true', help='find pure strategy equilibria')
    parser.add_argument('--payoffs', help='show payoff matrix', action='store_true')
    parser.add_argument('--others', help='show payoffs for one player given payoffs of others')
    parser.add_argument('--profile', help='test if profile is equilibrium')
    parser.add_argument('--canned', help='test if canned profile is equilibrium', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--iesds', action='store_true')
    parser.add_argument('--combo', action='store_true', help='check if a combo of strategies dominates a strategy')
    parser.add_argument('--support', help='try to find nash equilibria with the given support', default = None)
    parser.add_argument('--all', help='try to find all nash equilibria for this game', action='store_true')
    args = parser.parse_args()
    agame = None
    profile = None
    game_fun = get_game_fun(args.game)
    if game_fun in m_games:
        agame = game_fun(args.players, args.m)
    else:
        agame = game_fun(args.players)

    if args.payoffs:
        print('payoffs:')
        print(repr(agame.payoffs))
        print('')
    if args.others:
        others = literal_eval(args.others)
        print('one_player', agame.one_player_payoffs(others))
    if args.pure:
        print('pure:')
        print(repr(agame.find_pure()))
    if args.canned:
        profile = get_canned_profile(game_fun, args.players)
        print('profile:')
        print(profile)
        is_nash = agame.is_nash(profile)
        print('is_nash:', is_nash)
    if args.profile:
        profile = literal_eval(args.profile)
        print('profile:')
        print(profile)
        is_nash = agame.is_nash(profile)
        print('is_nash:', is_nash)
    if args.iesds:
        agame.iesds()
        print('dominated strategies:')
        print(agame.dominated)
    if args.combo:
        thecombo = literal_eval(args.combo)
        print(agame._combo_dominates(1, 0, 1, 2))
    if args.support:
        support = literal_eval(args.support)
        indifference_probs = agame._get_indifference_probs(support)
        print('support:')
        print(support)
        ne = agame.find_support_equilibria(support)
        print('nash equilibria:')
        print(ne)
    if args.all:
        all_nash = agame.find_all_equilibria()
        for anash in all_nash:
            print(anash)
            # anash looks like [{0: 4/9, 1: 5/9}, {0: 2/9, 1: 7/9}]
            profile = []
            for elm in anash:
                profile.append([(key, elm[key]) for key in elm])
            print(agame.get_profile_payoffs(profile))

#./test_sample_games.py --game battle --support "[[0,1,2], [0,1,2], [0,1,2]]" # this will give unique probs
#./test_sample_games.py --game battle --support "[[1,2], [1,2], [1,2]]"
#./test_sample_games.py --game battle --players 4 --support "[[1,2], [1,2], [0,3], [0, 3]]" # this should give lines of solutions.

#./test_sample_games.py --game detente --players 4 --m 2 --others "[[1, [[0,1]]], [2, [[0, 0.5], [1, 0.5]]], [3, [[0, 0.5], [1, 0.5]]]]"
