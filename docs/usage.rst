=============
Basic Usage
=============

Overview
--------
This module contains functionality for finding Nash Equilibria of multi-player (more than 2 player) games.
Because the number of possibilities that need to be checked explodes as the number of players increases,
it really only works for games with a relatively small number of players and actions.

This module uses the awesome power of Sympy to solve systems of equations. Sympy will even find general solutions
such as a player plays action 0 with probability 0, action 1 with probability p, 
and action 2 with probability 1 - p.

This package is intended more for students of game theory than for the practical value of finding Nash Equilibria,
I'm not at all sure they have any practical value. One observation you will make after playing around with this
is that for some multiplayer games, once some players have decided on a course of action it doesn't matter
what the other players do.

Players and actions
-------------------
Players are just represented by an index (player 0, player 1...) and their actions are also
just an index.

Payoff Structure
------------------
The payoff structure for an n player game is an n+1 dimensional tensor of numpy floats. For each
player, the length of the tensor index corresponding to the player index is equal to the numer
of actions for that player. The final index has a length equal to the number of players.
So for example, a 3 player game for which the first two players each have three available actions and
the third player only has 2 would be a tensor with dimensions [3,3,2,3]. The element at position
[0,1,0,2] would be the payoff for player 2 when player 0 plays action 0, player 1 plays action 1,
and player 2 plays action 0.

Finding nash equilibria
-------------------------
create a game.Game object by feeding in the payoff structure and call the find_all_equilibria method e.g.::

        import numpy as np
        payoffs = np.array([[[[1., 1., 1.],
                 [1., 1., 0.]],
                [[1., 0., 1.],
                 [1., 6., 6.]]],
               [[[0., 1., 1.],
                 [6., 1., 6.]],
                [[6., 6., 1.],
                 [4., 4., 4.]]]])

        from pymnash.game import Game
        agame = Game(payoffs)
        ne = agame.find_all_equilibria()
        print(ne)

This should give output::

    [[{0: 1}, {0: 1}, {0: 1}], [{1: 1}, {1: 1}, {1: 1}], [{0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}]]


The ne object is a list of dicts. Each element of the list corresponds to a Nash Equilibrium,
the dicts are the player actions and probabilities. For the example given, the three Nash Equlibria are

#. All players play action 0

#. All players play action 1

#. All players play action 0 with probability 0.911437827766148 and action 1 with probability  0.0885621722338523

