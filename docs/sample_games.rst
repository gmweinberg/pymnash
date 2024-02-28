=============================
Sample Games
=============================

The sample_games module contains functions for creating game objects, primarily for testing the
functionality of the Game class, although some users may find some of them to be of some interest in and of themselves.
Most of the functions take only one parameter "n", the number of players. Some of them take
a second parameter "m", the meaning of which is explained in the particular game.

Battle of the Genders
----------------------

``battle_of_genders(n)``

This is a generalization of the game `"battle of the sexes" <https://en.wikipedia.org/wiki/Battle_of_the_sexes_%28game_theory%29>`_ which allows any number of genders. 
The number of possible actions is equal to the
number of players. All players get zero unless they all coordinate on the same action, but each player has a separate preferred action.

For each possible action there will be one Nash Equilibrium in which all players play that action. There will also 
be mixed equilibria for each possible combination of actions. Finally, for more than 2 players there will 
be pointelss equilibrai where the players fail to coordinate on an action, 
but no one player can "fix" things because at least2 other players are failing to coordinate.

Detente of the Genders
----------------------

``detente_of_genders(n,m)``

Similar to battle of the genders, this allows players to score points without full cooperation.
There are n total players with m distinct genders. Each gender has a preferred action. The score for each player is
the number of players coordinating with that player minus 1. If the action of that player is that player's preferred 
action, that player's score is multiplied by 2.

Dunderheads
-----------

``dunderheads(n)``

This is a genarlization of high-low. Similar to battle of the sexes, except all players have the same preferred option.
Nonetheless, there are Nash Equilibria where the players coordinate on the low action, and mixed equilibria also.

Prisoner's Dilemma
------------------

``prisoners_dilemma(n)``

For the multi-player version of the prisonr's dilemma, all players who cooperate get the sucker payoff if at least one
player defects. Like the two-player version, the dominant strategy is for everyone to defect.

Matching Pennies
----------------

``matching pennies(n)``

This game is zero sum. In this game each player picks a number from 0 to n-1. The numbers are summed up, and the result modulo n is calculated, each player has a winning number. Each player might as well play randomly. As long as
at leats one player is in fact playing randomly, it doesn;t matter what anyone else does, which means as long as
at least 2 players are playing randomly, anything anyone else does is a Nash Equilibrium.

How Low Dare You Go
---------------------

``how_low_dare_you_go(n, m)``

This game is based on a game that Kevin Stone used to host on Usenet long ago. Each player picks an integer in 
the range 0 to m, the winner is the player with the lowest unique pick.

It turns out you don't need many players / options before solving this game in the general sense becomes intractable.

All Pay Auction
------------------

``all_pay_auction(n,m)``

In this game all players may bid integer amounts 0-m. There is a prize amount (1.5m for 2 players, 2m for more)
which is split among all players who bid the most. In addition all players lose their bids (so for losers
the payoff is negative their bid, for winners the payoff is their share of the prize minus their bid).

Stag Hunt
----------

``stag_hunt(n, m)``

In `Stag Hunt <https://en.wikipedia.org/wiki/Stag_hunt>`_ each player has two options, chase rabbits or hunt the stag.
It requires at least m players to successfully get the stag. If an insifficient number of players hunt the stag,
all stag hunters get zero, but if a sufficient number hunt the stag, the hunters share the stag value.
All rabbit chases get a small payoff in any case.


Reducible
------------

``reducible(n)``

This game was just created to test that the iterated elimination of strictly dominated strategies (iesds) code actually works.

Combo Reducible
----------------

``combo_reducible(n)``

This game is also just for testing that iesds works. It has a strategy that is not dominated by any one strategy but is dominated by a linear combination of 2 strategies.

Mixed Dom
----------

``mixed_dom(n, m)``

This game is two-player only.  One player has m possible actions, the other has m + 1 although it turns out the
last strategy is stricty dominated. It requires all m stratgies to dominate the dominated strategy, so
my current iesds code will fail to mark it as dominated, since it only knows how to eliminate strategies which
are dominated either by a single strategy or a combination of 2, but not larger comibinations.
It is based on a comment by "kevinwangg" in `This reddit thread <https://www.reddit.com/r/GAMETHEORY/comments/18d5zxx/dominated_by_3_or_more_strategies/>`_


