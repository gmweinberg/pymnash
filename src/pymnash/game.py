"""A class for a multi-player normal form game"""
import traceback
from copy import deepcopy
import numpy as np
from sympy import symbols
from sympy.core import expr
from sympy import preorder_traversal
from sympy.solvers import solve
#from sympy.core.expr import Expr
from sympy.core import Number
from sympy.core import Symbol
from sympy.core import Expr
from sympy.core.numbers import Float as FloatType

from pymnash.util import iterprob, iterindices, itersupport, iter_subset_combos, is_pure, dict_to_list, list_to_dict

class Game(object):
    """ A class for a multi-player normal form game."""


    def __init__(self, payoffs, player_labels = None, action_labels = None):
        """Payoffs is an np.array of floats, giving payouts to all players.
           If labels are omitted or incomplete we'll just fill them in with stringified ints."""
        # For now I'm not using player/acion labels.
        self.verbose = False
        if type(payoffs) != np.ndarray:
            raise Exception('Payoffs must be numpy array')
        self.payoffs = payoffs
        self.player_count = self.num_players()
        player_count = self.player_count
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
        self.dominated = [[] for ii in range(self.num_players())]

    def __repr__(self):
         return 'payoffs {}\nplayer_labels {}\naction_labels {}'.format(self.payoffs,
                self.player_labels, self.action_labels)

    def eq(self, val1, val2):
        """Check whether val1 and val2 are 'close enough' to count as equal."""
        return val1 + self._wiggle > val2 and val2 + self._wiggle > val1

    def gt(self, val1, val2):
        """Check whether val1 > val2, giving ourselves a little 'wiggle room' for rounding errors."""
        return val1 > val2 + self._wiggle

    def get_profile_payoffs(self, profile):
        """Find all player payoffs given the strategy profile. Returns a list of floats."""
        payoffs = [0] * self.player_count
        for acombo in itersupport(profile):
            combo_actions = acombo[0]
            for player in range(self.player_count):
                payoffs[player] += self.payoffs[(combo_actions)][player] * acombo[1]
        return payoffs

    def is_dominated(self, profile, profile_payoffs=None):
        """Check if there exists a pure strategy for at least one player which gives that player a payoff
           than the specified profile."""
        if profile_payoffs is None:
            profile_payoffs = self.get_profile_payoffs(profile)
        for player in range(self.player_count):
            old_player_profile = profile[player]
            for anaction in range(self.payoffs.shape[player]):
                action_payoff = 0
                profile[player] = [[anaction, 1]]
                for acombo in itersupport(profile):
                    combo_actions = acombo[0]
                    action_payoff +=  self.payoffs[(combo_actions)][player] * acombo[1]
                profile[player] = old_player_profile
                if action_payoff > profile_payoffs[player] + self._wiggle:
                    if self.verbose:
                        print("is_dominated profile {} is dominated for player {} by pure strategy {}".format(profile,
                          player, anaction))
                    return True
        return False

    def is_nash(self, profile):
        """Check if the supplied strategy profile is a nash equilibrium.
           Profile is a list of lists, each list is strategy profile for one player.
           Returns a boolean."""
        # In order to be a valid nash equilibrium, each player must be indifferent
        # as to which action in his support he plays
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
                        print('rejected utility', utility, 'support_utility', support_utility,
                              'nonsupport_utility', nonsupport_utility)
                     return False

        return is_nash

    def num_actions(self, player):
        """Return the number of available actions for the player with given index. Returns an int."""
        return self.payoffs.shape[player]

    def num_players(self):
        """Return the number of players for this game"""
        return len(self.payoffs.shape) - 1


    def find_pure(self):
        """Find any pure nash equilibria for this game. Returns a list of lists, one entry per equilibrium found.
           Inner list is the actions for each player."""
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
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game.
           Returns None, updates self.dominated in place"""
        progress = True
        while progress:
            progress = False
            if self.iesds1():
                progress = True
            if self.iesds2():
                progress = True


    def iesds1(self):
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game,
           considering stratgies dominated by a single other strategy.
           Updates dominated in place.
           returns a boolean indicating it found at least 1 new dominated strategy. """
        real_progress = False
        progress = True
        dominated = self.dominated
        num_players = self.num_players()
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
                             real_progess = True
                             if self.verbose:
                                  print('player', player, 'action', action1, 'dominated by', action0)
        return real_progress

    def iesds2(self):
        """Perform iteratated elimination of strictly dominated strategies to get a reduced game,
           considering stratgies dominated by a linear combo of 2 other strategies.
           Returns a boolean indicating it found at least one new dominated strategy"""
        # For strategy 0 to be dominated by a combo of strategies 1 and 2, for every combo of other players'
        # strategies it must be the case that at least one of
        # strategies 1 and 2 score better than strategy 0 at every point. If both perform better, we don't get any
        # new information as to what combinations perform better, but if
        # only strategy 1 performs better we have a minimum ratio of strategy 1 to strategy
        # 2 for a dominating combo, and if only stratgey 2 perfoms better we get a maximum ratio.

        num_players = self.num_players()
        progress = True
        real_progress = False
        dominated = self.dominated
        while progress:
            progress = False
            for player in range(num_players):
                for action_a in range(self.payoffs.shape[player]):

                    if action_a in dominated[player]:
                        continue
                    for action_b in range(self.payoffs.shape[player]):
                        if action_b in dominated[player]:
                             continue
                        if action_b == action_a:
                             continue
                        for action_c in range(action_b + 1, self.payoffs.shape[player]):
                            if action_c in dominated[player]:
                                continue
                            if action_c == action_a:
                                continue
                            if self._combo_dominates(player, action_a, action_b, action_c):
                                progress = True
                                real_progress = True
                                dominated[player].append(action_a)
        return real_progress

    def _combo_dominates(self, player, strat_a, strat_b, strat_c):
        """Helper function for iesds2. Checks if there is some combo of strategies b and c that dominates strategy a.
           returns a boolean"""
        dominated = self.dominated
        min_p = None # minimum probability of playing b which might dominate a
        max_p = None
        pslice = [slice(None)] * len(self.payoffs.shape) # just interested in payoffs for player
        pslice[-1] = player
        sslice = deepcopy(pslice)
        sslice[player] = strat_a
        a_payoffs = self.payoffs[tuple(sslice)]
        sslice = deepcopy(pslice)
        sslice[player] = strat_b
        b_payoffs = self.payoffs[tuple(sslice)]
        sslice = deepcopy(pslice)
        sslice[player] = strat_c
        c_payoffs = self.payoffs[tuple(sslice)]
        for indices in iterindices(a_payoffs.shape):
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
                ut_a = a_payoffs[indices]
                ut_b = b_payoffs[indices]
                ut_c = c_payoffs[indices]
                if self.gt(ut_a, ut_b) and self.gt(ut_a, ut_c):
                    return False
                if self.gt(ut_b, ut_a) and self.gt(ut_c, ut_a):
                    continue
                if self.eq(ut_b, ut_c):
                    continue
                p = (ut_a - ut_c) / (ut_b - ut_c) # probability b at which the combo scores the same as playing a
                if ut_b > ut_c:
                    if min_p is None or p > min_p:
                        min_p = p
                else:
                    if max_p is None or p < max_p:
                        max_p = p
                    if min_p is not None and max_p is not None and min_p > max_p:
                        return False
        if self.verbose:
            print("player", player, "strategy", strat_a, "dominated by ", strat_b, strat_c, min_p, max_p)
        return True

    def _get_indifference_probs(self, support):
        """Find the combinations of probabilities such that each player is indifferent to which action in his
           own support which he plays given the probabilities of the other players.
           Support is a list of lists, players and actions. Each player could have any number of actions,
           the number of possible actions  will vary by player.
           Returns a list of dicts."""
        support_symbols = [] # list of lists. Value is a tuple (player_action (int), symbol)
        symbols_list = [] # put all symbols in one list for solver
        for player in range(len(support)):
            support_symbols.append([])
            for action in support[player]:
                name = 'prob_{}_{}'.format(player, action)
                asymbol = symbols(name)
                support_symbols[player].append((action, asymbol))
                symbols_list.append(asymbol)
        symbol_type = type(symbols_list[0])

        # print(repr(support_symbols))
        # probabilities for each player action must equal one
        psums = [] # list of probability sum equations
        for player in range(len(support)):
            eq = -1
            for action in support_symbols[player]:
                eq += action[1]
            psums.append(eq)
        #print(repr(psums))
        indiff_equations = []
        for player in  range(len(support_symbols)):
            if len(support_symbols[player]) == 1: # player is sticking with 1 strategy, no indifference for him
                continue
            ppayoffs = [] # each element is the expected payoff to the chosen player for the chosen action
            old_ss = support_symbols[player]
            for player_action in support[player]:
                support_symbols[player] = [(player_action, 1)]
                apayoff = 0
                for acombo in itersupport(support_symbols):
                    combo_actions = acombo[0]
                    apayoff += self.payoffs[(combo_actions)][player] * acombo[1]
                ppayoffs.append(apayoff)
            for payoff_index in range(1, len(ppayoffs)):
                an_equality = ppayoffs[0] - ppayoffs[payoff_index]
                indiff_equations.append(an_equality)
            support_symbols[player] = old_ss
        all_equations = psums + indiff_equations
        try:
             initial_solutions = solve(all_equations, symbols_list)
        except Exception:
             # This means there are no solutions with the given support
             #print("sympy threw an exception, here the equations ans symbols", all_equations, symbols_list)
             return []
        if not initial_solutions:
            return []
        if type(initial_solutions) == dict:
            support_result = self._sympy_dict_to_profile(initial_solutions)
            for aprofile in support_result:
                for val in aprofile.values():
                    #print('type', type(val))
                    if type(val) == FloatType:
                        if float(val) > 1 or float(val) <= 0:
                            return []
            #print(" a dict?? WFTT???")
            #print([initial_solutions])
            #print(support_result)
            return  [support_result]
        real_solutions = []
        for asolution in initial_solutions:
            support_result = [ {} for ii in range(self.player_count)]
            ok = True
            for val in asolution:
                try:
                    if type(val) != symbol_type and val > 1 or val <= 0:
                        ok = False
                        break

                except Exception:
                    pass # can't compare symbol with number, carry on
            if ok:
                sd = {}
                for ii, elm in enumerate(symbols_list):
                    name = str(elm)
                    pieces = name.split('_')
                    player = int(pieces[1])
                    action = int(pieces[2])
                    support_result[player][action] = asolution[ii]
                real_solutions.append(support_result)
        #for asolution in real_solutions:
        #    print(asolution)
        return real_solutions

    def _sympy_dict_to_profile(self, pd):
        """Given a sympy dictionary indicating solutions to indifference equations, return a support structure."""
        #The probabilities in the profile here might be a number or an expression
        profile = [ {} for ii in range(self.player_count)]

        for elm in pd.keys():
            name = str(elm)
            pieces = name.split('_')
            player = int(pieces[1])
            action = int(pieces[2])
            profile[player][action] = pd[elm]
        # The profile also must include self-referntial values for symbolic probabilities e.g
        # if sympy says player 0 has an action profile of 0: 1 - p_0_1 the we must also include in his
        # action dict a value 1: p_0_1
        for elm in pd.values():
            if isinstance(elm, Expr):
                for arg in  preorder_traversal(elm):
                    if isinstance(arg, Symbol):
                        name = str(arg)
                        pieces = name.split('_')
                        player = int(pieces[1])
                        action = int(pieces[2])
                        profile[player][action] = arg
        return profile

    def _carnate_profile(self, profile):
        """Given a support dict which may contain sympy expressions as values, return a suport with float values."""
        # We need this to evaluate the payoff to a player of a strategy profile that is an expression rather
        # than a number e.g. player 0 will play actions 0 and 1 in any probabilities that add to 1.
        # We will treat such a case as the plyer choosing all actions in the support with equal probability.
        profile_result = [{} for ii in range(self.player_count)]
        for player_index, player_actions in enumerate(profile):
            even = 1.0 / len(player_actions)
            for action in player_actions:
                action_prob = player_actions[action]
                if isinstance(action_prob, Number):
                    profile_result[player_index][action] = float(action_prob)
                elif isinstance(action_prob, Expr):
                    profile_result[player_index] = {anaction: even for anaction in player_actions}
                    continue
                else:
                    profile_result[player_index][action] = float(action_prob)
        return profile_result


    def find_all_equilibria(self):
        """Attempt to find all nash equilibria for a game. Returns a list of dicts, keys are symbols,
           values are probabilities (numbers or symbols)."""
        result = []
        action_shape = self.payoffs.shape[:-1]
        possible_actions = [list(range(player_actions)) for player_actions in action_shape]
        #print(possible_actions)
        # we should first eliminate dominated strategies. we will skip that step for now
        for acombo in iter_subset_combos(possible_actions):
           if is_pure(acombo):
               # print(acombo)
               profile = [[[player_action[0], 1]] for player_action in acombo]
               if not self.is_dominated(profile):
                    profile_dict = [list_to_dict(player_profile) for player_profile in profile]
                    result.append(profile_dict)
           else:
               #print("checking combo", acombo)
               combo_solutions = self._get_indifference_probs(acombo)
               for asol in combo_solutions:
                   # print('asol', asol)
                   #listy = [dict_to_list(psol) for psol in asol]
                   #print('psol', psol)
                   carnate = self._carnate_profile(asol)
                   listy = [dict_to_list(elm) for elm in carnate]
                   if not self.is_dominated(listy):
                       result.append(asol)
        return result
