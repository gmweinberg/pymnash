=============
Basic Usage
=============
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


