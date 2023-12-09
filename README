This module contains functionality for finding Nash Equilibria of multi-player (more than 2 player) games.
Because the number of possibilities that need to be checked explodes as the number of players increases,
it reallyonly works for games with a relatively small number of players.

In order to find the Nash Equilibrium for a game, first feed in the payoff profile of the game as a numpy
tensor. There is one dimension for each player, with the length along that dimension being the number of
possible actions for that player, plus one more dimension with a length equal to the number of players.

Once that is created, one can ask if a given strategy profile is a Nash Equilibrim, search for Nash Equilibria with 
a given support, or try to find all Nash Equilibria. You can also check to see if a strategy is dominated by 
some other strategey or by a linear combination of two strategies.

This module uses the awesome power of Sympy to solve systems of equations. Sympy will even find general solutions
such as a player plays action 0 with probability 0, action 1 with probability p, 
and action 2 with probability 1 - p.

This package is intended more for students of game theory than for the practical value of finding Nash Equilibria,
I'm not at all sure they have any practical value. One observation you will make after playing around with this
is that for some multiplayer games, once some players have decided on a course of action it doesn't matter
what the other players do.
 
