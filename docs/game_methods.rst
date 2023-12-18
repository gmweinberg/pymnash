=======================
Game Methods
=======================

If you just want the Nash Equilibria of a relatively small game, it is easiest to just call
find_all_equilibria. However, if the game is too large for the call to complete in a reasonable time, or
if you just feel like playing around, it might be worthwhile calling some of the other methods.

find_all(self)
--------------
Finds all Nash Equilibria. Reutrns a list of lists of dicts. Each element of the outer list corresponds to
a Nash Equilibium. Each element of the inner list represents the stratey profile for a particular player in that
Equlibrium::

        from pymnash.sample_games import stag_hunt
        stag = stag_hunt(3, 2)
        ne = stag.find_all_equilibria()
        print(ne)

The results should be

``[[{0: 1}, {0: 1}, {0: 1}], [{1: 1}, {1: 1}, {1: 1}], [{0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}]]``


This represents 3 equilibria, one where all players play action 0 (chase rabbits) one where all players play action 1 (hunt the stag), and one where the players all hunt the stag or chase rabbots with equal probabilities.


find_support_equilibria(self, support)
--------------------------------------
Tries to find nash equilibria with the given support. Support is a list of lists,
outer list is per player, inner list is the actions that player will perform with nonzero probability.::

    from pymnash.sample_games import battle_of_genders
    battle = battle_of_genders(3)
    ne = battle.find_support_equilibria([[0,1], [0,1], [0,1]])

The results should be

``[[{0: 0.750000000000000, 1: 0.250000000000000}, {0: 0.250000000000000, 1: 0.750000000000000}, {0: 0.500000000000000, 1: 0.500000000000000}]]``


find_pure(self, simple=True)
----------------------------

Finds Nash Equilibria in pure strategies.
If "simple" is true, the result will be in a simplified format becuase there are no probabilities:
The result is just a list of tuples, because there are no probabilities. Each element of the outer list 
represents an equilibrium, each element of the tuple is the actions preformed by the players in order.

If simple is False, the result will be in the same format as for find_all_equilibria::

        from pymnash.sample_games import battle_of_genders
        battle = battle_of_genders(3)
        ne = battle.find_pure()
        print(ne)

The results should be

``[(0, 0, 0), (2, 1, 0), (1, 2, 0), (2, 0, 1), (1, 1, 1), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 2, 2)]``

The pure Nash Equilibria represent the three cases where all players coordinate on the same action,
and also the 6 more where no two players play the same action.


is_nash(self, profile)
----------------------

Check if the supplied strategt profile is a Nash Equilibrium. The profile is a list of dicts, each dict is the
strategy profile for one player. This is the same as the output from find_all, so if you plug in a
Nash Equilibrium you got from find_all, it should return True.::

        from pymnash.sample_games import stag_hunt
        stag = stag_hunt(3, 2)
        profile =  [{0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}, {0: 0.911437827766148, 1: 0.0885621722338523}]
        print(stag.is_nash(profile))

Should print True. The pitfalls of floating-point math may occasionally lead to this function giving the wrong answer.

iesds(self)
-----------

Attempts to find strictly dominated strategies. Returns a list of lists, the outer list corresponds to a player,
the inner list is dominated strategies (so any Nash Equilibria do not involve those stratgeies)::

    from pymnash.sample_games import reducible
    red = reducible(3)
    print(red.iesds())
    print(red.find_all_equilibria())

output::

    [[1, 2], [1, 2], [1]]
    [[{0: 1}, {0: 1}, {0: 1}]]

For this game, players 0 and 1 each have 3 possible actions, but actions 1 and 2 are dominated.
Player 2 only has 2 actions, but action 1 is dominated.
So the only Nash Equilibrium is all players playing action 0 with probability 1.

This method currenly only searches for actions which are either dominated by a singek action or by a
combination of 2 acions. So for games like the mixed_dom sample game where it may take a larger
combination of actions to dominate an action, this method will fail to find the dominated action.
