#!/usr/bin/python

"""Functions to create some sample test games"""

import numpy as np

from pymnash.game import Game
from pymnash.util import coords_from_pos, iterindices, enumershape, zero_sum_dict, payout_array_from_dict
from collections import defaultdict


def battle_of_genders(n):
    """A generalization of the 'battle of the sexes' game which supports any number of genders.
    The number of possible moves for each player is equal to the total number of players.
    All players get zero payoff unless they all coordinate on a choice, each player has a particular favorite choice
    but all players get something as long as they all coordinate."""
    # We know there is one pure strategy per player, with all players playing that player's favorite.
    # There will also be one mixed  strategy for ever combination of pure strategies
    boga = np.zeros(tuple([n] * (n + 1)), dtype=float)
    #print(boga)
    for ii in range(n):
        loc = boga
        for jj in range(n):
            loc = loc[ii]
        for kk in range(n):
            if kk == ii:
                loc[kk] = n
            else:
                 loc[kk] = 1
    return Game(boga)

def detente_of_genders(n, m):
    """Similar to battle of genders, there are n plyers total with m types of players
       (and m actions per player)
       Instead of requiring all players to coordinate, the score for all players choosing the same action
       is 2 * (c -1) if it is their preferred action and (c -1) if it is not (so any player
       choosing a unique action scores zero)."""
    shape = [m] * n # n players, m moves per player
    shape.append(n) # n player payoffs
    payoffs = np.zeros(tuple(shape), dtype=float)
    for pos in iterindices(shape[:-1]):
        counts = [0] * m
        for pospos in pos:
            counts[pospos] +=1
        for ii in range(n):
            type_ = int(ii/m)
            action = pos[ii]
            action_score = counts[action] - 1
            if action == type_:
                action_score *= 2
            there = list(pos)
            there.append(ii)
            payoffs[tuple(there)] = action_score
    return Game(payoffs)

def reducible(n):
    """A game just to test the iterated elimination of strictly dominated strategies. """
    # 2 player version scored come from steven tadelis game theory an introduction.
    # I will extend it with obvious dominant strategies of other players.
    twoplayer = [[[4,3], [5,1], [6,2]],
                 [[2,1], [8,4], [3,6]],
                 [[3,0], [9,6], [2,8]]]
    thetuple = tuple([3, 3] + [2] * (n - 2) +  [n])
    payoffs = np.zeros(thetuple)
    for indices in iterindices(payoffs.shape):
        player = indices[len(indices) - 1]
        if player in [0, 1]:
             payoffs[indices] = twoplayer[indices[0]][indices[1]][player]
        elif indices[player] == 0:
             payoffs[indices] = 1
    return Game(payoffs)

def combo_reducible(n):
    """A game for testing iesds2. It has a strategy that is not dominated by any single other strategy
       but can be dominated by a linear combination of strategies."""
    # The game comes from steven tadelis game theory an introduction, page 115 of first edition.
    if n != 2:
        raise Exception('This game is only supported for two players')
    payoffs = [[[5, 1], [1,4], [1, 0]],
               [[3,2], [0, 0], [3, 5]],
               [[4,3], [4,4], [0,3]]]
    payoffs = np.array(payoffs)
    return Game(payoffs)



def dunderheads(n):
    """Multi-player High-Low. Similar to battle of genders, except there are only two options and all players
        have the same preferrred option."""
    # There are two pure nash equilibria, the 'smart' on where evryone picks the preferred option, and the
    # 'dunderheaded' one where everyone picks the option they don't like.
    # There should also be a 'super-dunderheaded' solutions where all player mix their picks.
    # The probability of pcking the dunderheaded option will be higher, so the higher chance of getting a match
    # exactly compensates for the lower payoff.
    payoffs = np.zeros(tuple([2] * n + [n]), dtype=float)
    for indices in iterindices(payoffs.shape):
        good = True # everyone is playing the good choice
        bad = True
        for ii in range(len(indices) - 1):
            if indices[ii] == 1: #someone is playing the bad choice
                good = False
            elif indices[ii] == 0:
                bad = False
        if good:
            payoffs[indices] = 3.0
        if bad:
            payoffs[indices] = 1.0
    return Game(payoffs)



def prisoners_dilemma(n):
    """For the multiplayer prisoner's dilemma we will say if everone cooperates then each person gets a -1 payoff.
       If exactly one player defectes he gets 0 and everyone else gets -5.
       If multiple player defect, the ones that defect get -3 and the ones that cooperate get -5.
    """
    # We will say for ever player choice '0' is cooperate and '1' is defect.
    # The innermost array is player id for payoffs
    # We know the only nash equilibrium is everybody defects.
    payoffs = np.zeros(tuple(([2] * n + [n])), dtype=float)
    for ii in range(np.prod(payoffs.shape)):
        coords = coords_from_pos(payoffs, ii)
        player = coords[ n ] # index of the player we are looking at
        he_defected = bool(coords[player])
        total_defected = sum(coords[:-1])
        if total_defected == 0:
            payoffs[coords] = -1
        elif he_defected and total_defected  == 1:
            payoffs[coords] = 0
        elif he_defected:
             payoffs[coords] = -3
        else:
             payoffs[coords] = -5
    return Game(payoffs, prisoner_labels)


def matching_pennies(n):
    """For n player matching pennies each player can choose a number in the range 0 to n -1, and player m
       wins if the result is m modulo n.
       For the 2 x 2 case think of heads as zero and tails as 1, so player 0 wins with HH or TT,
       player 1 wins with HT or TH"""
    # The obvious equilibrium is everyone plays randomly. But there are many possibilities for multiple players.
    # In the 3 player version, if 2 players
    # play randomly, the other player can play anything and it's still an equilibrium.
    # As long as at least one player is playing randomly it doesn't really matter what the
    # other players do, but just one player randomising would not be an equilibrium.
    payoffs = np.zeros(tuple([n] * (n + 1)), dtype=float)
    for ii in range(np.prod(payoffs.shape)):
        coords = coords_from_pos(payoffs, ii)
        player = coords[ n ] # index of the player we are looking at
        sum_played = sum(coords[:-1])
        if sum_played % n == player:
            payoffs[coords] = n - 1
        else:
            payoffs[coords] = -1
    #print(payoffs)
    return Game(payoffs)

def how_low_dare_you_go(n, m):
    """n players have m choices of numbers, m > n. The winning player is the player who picks
       the lowest non-negative integer not chosen by any other player."""
    # we will restrict the game to m choices so we have a hope of finding solutions.
    # In principle this game could be played with an infinite number of possible
    # moves, nobody igoing to play a number all that much higher than the number of players in any case.
    payoffs = np.zeros(tuple(([m] * n + [n])), dtype=float)
    for jj, coords in enumershape(payoffs.shape[:-1]):
        counts = defaultdict(int) # number of players picking this number
        win = None
        for iii in range(len(coords)):
            counts[coords[iii]] += 1
        for ii in sorted(counts.keys()):
            if counts[ii] == 1:
                win = ii
                break
        if win is not None:
            done = False
            for player_index in range(len(coords)):
                if coords[player_index] == win:
                    pos = list(coords)
                    pos.append(player_index)
                    payoffs[tuple(pos)] = 1
    return Game(payoffs)

def mixed_dom(n, m):
    """A two-player game where one player has a dominated strategy, but it takes a combination of
       m strategies to defeat it (one player has m strategies, the other has m + 1).
       Based on a comment by kevinwangg in the thread
       https://www.reddit.com/r/GAMETHEORY/comments/18d5zxx/dominated_by_3_or_more_strategies/
    """
    if n != 2:
        raise ValueError("This game is only supported for 2 players")
    payoffs = np.zeros(tuple((m + 1, m, 2)), dtype=float)
    for ii in range(m):
        payoffs[ii][ii][0] = m + 1
        payoffs[ii][ii][1] = -1 * (m + 1)
        payoffs[m][ii][0] = 1
        payoffs[m][ii][1] = -1
    return Game(payoffs)

def chicken(n):
    """For this variation of multi-player cheicken, each player has 2 possible actions
       (0 = chicken, 1 = hawk).  If everyne is a chicken, everyone scores 0.
       If there is just one hawk, he gets 5 points and the chickens each lose 1.
       If there is more than 1 hawk, they each score -10 and the chickens get zero.
    """
    payoffs = np.zeros(tuple([2] * n + [n]), dtype=float)
    shape = payoffs.shape[:-1]
    for pos in iterindices(shape):
        hawks = 0
        for ii in range(len(shape)):
            if pos[ii] == 1:
                hawks += 1
        for ii in range(n):
            where = tuple(list(pos) + [ii])
            if hawks == 1:
                if pos[ii] == 1:
                    payoffs[where] = 5
                else:
                    payoffs[where] = -1
            elif hawks > 1:
                if pos[ii] == 1:
                    payoffs[where] = -10
    return Game(payoffs)

def stag_hunt(n, m):
    """Each player has 2 options, 0 = hunt the stag, 1 = chase rabbits.
       We need a critical number m of stag hunters to catch the stag.
       If an insufficient number goes after the stag, they get 0
       If a sufficient number go after the stag, they share the value which I will say is 4 * n.
    """
    payoffs = np.zeros(tuple([2] * n + [n]), dtype=float)
    shape = payoffs.shape[:-1]
    for pos in iterindices(shape):
        hunters = 0
        for ii in range(len(shape)):
            if pos[ii] == 1:
                hunters += 1
        for ii in range(n):
            where = tuple(list(pos) + [ii])
            if pos[ii] == 0:
                payoffs[where] = 1
            else:
                if hunters >= m:
                    payoffs[where] = 4 * n / hunters
    return Game(payoffs)

def all_pay_auction(n, m):
    """In this discrete version of all_pay_auction, each of n players can bid an integer amount
       from 0 to m. The prize is split between all players who bid the maximum.
       The prize must be more than the maximum bid for one player and less than the total
       bid to keep the game interesting, I will make it 1.5 * m for 2 players and 2 * m for more"""
    if n == 2:
        prize = 1.5 * m
    else:
        prize = 2 * m
    payoffs = np.zeros(tuple([m + 1] * n + [n]), dtype=float)
    shape = payoffs.shape[:-1]
    for  pos in iterindices(shape):
        max_bid = None
        for ii, elm in enumerate(pos):
            if max_bid is None or elm > max_bid:
                max_bid = elm
                winners = [ii]
            elif elm == max_bid:
                winners.append(ii)
        lol = 'nope'
        for ii in range(n):
            where = list(pos)
            where.append(ii)
            if ii in winners:
                payoffs[tuple(where)] = prize / len(winners) - where[ii]
            else:
                payoffs[tuple(where)] = -where[ii]
    return Game(payoffs)


__all__ = ['battle_of_genders', 'detente_of_genders', 'reducible', 'combo_reducible', 
           'dunderheads', 'prisoners_dilemma',
           'matching_pennies', 'how_low_dare_you_go', 'mixed_dom', 'chicken', 'stag_hunt',
           'all_pay_auction']

