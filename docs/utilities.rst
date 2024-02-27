====================
Utilities
====================

zero_sum_2_player_payoffs
-------------------------

This is a convenience method for creating the payoffs matrix for a zero sum two player game.
Since the payoffs for the payers are the same (except the minus sign) you only need to enter them once.
It just takes a list of lists (or equivalent), and returns 3 dimensional numpy array.

symmetric_2_player_payoffs
--------------------------

This is a convenience method for creating the payoffs matrix for a two player game for which
the payoffs are the same, that is, the payoff for the first at (x, y) is the same as
the payoff for the second player at (y, x). Both players get te same payout on the diagonal.
It takes as an input a list of lists (or equivalent) and returns a numpy array.


