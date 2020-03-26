"""A class for a multi-player normal form game"""
from copy import deepcopy
import numpy as np
from fractions import Fraction
from util import iterprob

class Game(object):
    """ A class for a multi-player normal form game."""


    def __init__(self, payoffs, player_labels = None, action_labels = None):
        """Payoffs is an np.array of floats, giving payouts to all players.
           If labels are omitted or incomplete we'll just fill them in with stringified ints."""
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

    def __repr__(self):
         return 'payoffs {}\nplayer_labels {}\naction_labels {}'.format(self.payoffs, self.player_labels, self.action_labels)

    def is_nash(self, profile):
        """Check if the supplied strategy profile is a nash equilibrium. Profile is a list of lists, each list is strategy profile for one player.
           Returns a boolean."""
        # In order to be a valid nash equilibrium, each player must be indifferent as to which action in his support he plays
        # (suppport is actions played with non-zero probability)
        # also, a player must not be able to do better by playing an action not in his suport.
        # of course, no probability can be negative and all probabilities must sum to 1.
        # I am using the Fractions class to test that the sums of floats are equal. We may have to change this.
        shape = self.payoffs.shape
        for ii, player_profile in enumerate(profile):
            prob_sum = 0
            support_utility = None
            nonsupport_utility = None
            for prob in player_profile:
                if prob < 0:
                    raise Exception('negative probability')
                prob_sum += Fraction(prob).limit_denominator()
            if prob_sum != 1:
                raise Exception('probabilities do not sum to 1')
            others_profile = deepcopy(profile)
            del others_profile[ii]
            # check the utility 
            for jj, prob in enumerate(player_profile):
                in_support = prob > 0
                myslice = [slice(None)] * (len(shape) - 1)
                myslice[ii] = jj # player index ii is playing strategy jj
                relevant_payoffs = self.payoffs[tuple(myslice)]
                # print("relevant payoffs 1", relevant_payoffs)
                myslice = [slice(None)] * (len(shape) - 2)
                myslice[-1] = ii
                relevant_payoffs = relevant_payoffs[tuple(myslice)]
                # print("relevant payoffs 2", relevant_payoffs)
                utility = 0
                for (thetuple, theprob) in iterprob(others_profile):
                    utility += relevant_payoffs[thetuple] * theprob
                utility = Fraction(utility).limit_denominator()
                print('player', ii, 'action', jj, 'utility', utility, 'in_support', in_support)
                if in_support:
                    if nonsupport_utility is not None and nonsupport_utility > utility:
                        return False
                    if support_utility is None:
                        support_utility = utility
                    elif support_utility != utility:
                         return False
                else:
                    if support_utility is not None and utility > support_utility:
                        return False
                    if nonsupport_utility is None or utility > nonsupport_utility:
                        nonsupport_utility = utility 
        return True
        
    


    def iesds(self):
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game."""
        pass

