"""A class for a multi-player normal form game"""
import pdb
from copy import deepcopy
import numpy as np
from fractions import Fraction
from util import iterprob, iterindices

class Game(object):
    """ A class for a multi-player normal form game."""


    def __init__(self, payoffs, player_labels = None, action_labels = None):
        """Payoffs is an np.array of floats, giving payouts to all players.
           If labels are omitted or incomplete we'll just fill them in with stringified ints."""
        self.verbose = False
        if type(payoffs) != np.ndarray:
            raise Exception('Payoffs must be numpy array')
        self.payoffs = payoffs
        player_count = payoffs.shape[len(payoffs.shape) - 1]
        if player_labels is None:
            self.player_labels =  [str(ii) for ii in range(player_count)]
        elif len(player_labels) >= player_count:
            self.player_labels = list(player_labels[0:player_count])
        else:
            self.player_labels = list(player_labels)
            for ii in range(player_count - len(player_labels)):
                self.player_labels.append(str(ii + len(player_labels)))
        action_count = payoffs.shape[0] # TODO: support different action lables for different players
        if action_labels is None:
             self.action_labels = [str(ii) for ii in range(action_count)]
        elif len(action_labels) >= action_count:
            self.action_labels = list(action_labels[0:action_count])
        else:
            self.action_labels = list(action_labels)
            for ii in range(action_count - len(action_labels)):
                self.action_labels.append(str(ii + len(action_labels)))
        self._wiggle = 0.000001

    def __repr__(self):
         return 'payoffs {}\nplayer_labels {}\naction_labels {}'.format(self.payoffs, self.player_labels, self.action_labels)

    def eq(self, val1, val2):
        """Check whether val1 and val2 are 'close enough' to count as equal."""
        return val1 + self._wiggle > val2 and val2 + self._wiggle > val1

    def gt(self, val1, val2):
        """Check whether val1 > val2, giving ourselves a little 'wiggle room' for rounding errors."""
        return val1 > val2 + self._wiggle
       

    def is_nash(self, profile):
        """Check if the supplied strategy profile is a nash equilibrium. Profile is a list of lists, each list is strategy profile for one player.
           Returns a boolean."""
        # In order to be a valid nash equilibrium, each player must be indifferent as to which action in his support he plays
        # (suppport is actions played with non-zero probability)
        # also, a player must not be able to do better by playing an action not in his suport.
        # of course, no probability can be negative and all probabilities must sum to 1.
        is_nash = True
        shape = self.payoffs.shape
        for player, player_profile in enumerate(profile):
            prob_sum = 0
            support_utility = None
            nonsupport_utility = None
            for prob in player_profile:
                if prob < 0:
                    raise Exception('negative probability')
                prob_sum += prob
            if not self.eq(prob_sum, 1):
                if self.verbose:
                    print('prob_sum', prob_sum)
                raise Exception('probabilities do not sum to 1')
            others_profile = deepcopy(profile)
            del others_profile[player]
            # check the utility 
            for jj, prob in enumerate(player_profile):
                if self.verbose:
                    print('player', player, 'others_profile', others_profile)
                in_support = prob > 0
                myslice = [slice(None)] * len(shape)
                myslice[-1] = player
                relevant_payoffs = self.payoffs[tuple(myslice)]
                if self.verbose:
                    print("all payoffs for player", player, relevant_payoffs)
                myslice = [slice(None)] * (len(shape) - 1)
                myslice[player] = jj
                relevant_payoffs = relevant_payoffs[tuple(myslice)]
                if self.verbose:
                    print("payoffs for player", player, relevant_payoffs)
                utility = 0
                for (thetuple, theprob) in iterprob(others_profile):
                    utility += relevant_payoffs[thetuple] * theprob
                # utility = Fraction(utility).limit_denominator() # Fractions are not great for more than 2 players
                if self.verbose:
                    print('player', player, 'action', jj, 'utility', utility, 'in_support', in_support)
                is_nash = True
                if in_support:
                    if nonsupport_utility is not None and self.gt(nonsupport_utility, utility):
                        is_nash = False
                    if support_utility is None:
                        support_utility = utility
                    elif not self.eq(support_utility, utility):
                         is_nash = False
                else:
                    if support_utility is not None and self.gt(utility, support_utility):
                        is_nash = False
                    if nonsupport_utility is None or utility > nonsupport_utility:
                        nonsupport_utility = utility
                if not is_nash:
                     if self.verbose:
                        print('rejected utility', utility, 'support_utility', support_utility,  'nonsupport_utility', nonsupport_utility)
                     return False
                
        return is_nash

    def num_actions(self, player):
        """Return the number of available actions for the player with given index. Returns an int."""
        return self.payoffs.shape[player]

    def num_players(self):
        """Return the number of players for this game"""
        return len(self.payoffs.shape) - 1


    def find_pure(self):
        """Find any pure nash equilibria for this game. Returns a list of lists, one entry per equilibrium found. Inner list is the actions for each player."""
        # Iterate though the list of pure stretegies, check if it is a nash equilibrium
        eq = []
        shape = self.payoffs.shape[:-1]
        for indices in iterindices(shape):
             # convert indices into an action profile playing the pure actions at that index
             profile = [0] * len(shape)
             for player, action in enumerate(indices):
                 profile[player] = [0] * self.num_actions(player)
                 profile[player][action] = 1
             is_nash = self.is_nash(profile)
             print('profile', profile, 'is_nash', is_nash)
             if is_nash:
                 eq.append(indices)
        return eq


    def iesds(self):
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game."""
        pass


    def iesds1(self):
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game, considering stratgies dominated by a  single other strategy"""
        num_players = self.num_players()
        progress = True
        dominated = [[] for ii in range(num_players)] # [[]]] * num_players makes all inner lsist the same list instead of separate ists with same value
        while progress:
            progress = False
            for player in range(num_players):
                for action0 in range(self.payoffs.shape[player]):
                    if action0 in dominated[player]:
                         continue
                    aslice = [slice(None)] * len(self.payoffs.shape)
                    aslice[-1] = player
                    aslice[player] = action0
                    action0_payoffs = self.payoffs[tuple(aslice)]
                    for action1 in range(self.payoffs.shape[player]):
                        skip = False
                        if action1 in dominated[player]:
                            skip = True
                            continue
                        if action0 == action1:
                            skip = True
                            continue
                        aslice = [slice(None)] * len(self.payoffs.shape)
                        aslice[-1] = player
                        aslice[player] = action1
                        action1_payoffs = self.payoffs[tuple(aslice)]
                        adominated = True
                        for indices in iterindices(action0_payoffs.shape):
                            skip2 = False
                            for ii, index in enumerate(indices):
                                inner_player = ii
                                if inner_player >= player:
                                    inner_player += 1
                                if index in dominated[inner_player]:
                                    skip2 = True
                                    break
                            if skip2:
                                 continue
                            ut0 = action0_payoffs[indices]
                            ut1 = action1_payoffs[indices]
                            if not self.gt(ut0, ut1):
                                adominated = False
                                if self.verbose:
                                    pass
                                    # print('player', player, 'action0', action0, 'action1', action1, 'u0', ut0, 'u1', ut1)
                                break
                        if (not skip) and adominated:
                             dominated[player].append(action1)
                             progress = True
                             if self.verbose:
                                  print('player', player, 'action', action1, 'dominated by', action0)
        return dominated

