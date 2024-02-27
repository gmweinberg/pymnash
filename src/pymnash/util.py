import numpy
from itertools import combinations, product

def coords_from_pos(thearray, pos):
    """Get the corrdinates from a one-dimensional position and shape. We will make the first index most signifcant."""
    # we should probably replace this with iterindices where it is used.
    coords = []
    for ii in range(len(thearray.shape) - 1):
        prod = numpy.prod(thearray.shape[1 + ii:])
        coord = pos // prod
        coords.append(coord)
        pos -= coord * prod
    coords.append(pos)
    return tuple(coords)

def mult(iterable):
    prod = 1
    for elm in iterable:
        prod *= elm
    return prod

def pos_from_coords(shape, coords):
    sum_ = 0
    for ii, coord in enumerate(coords):
        mul = mult([shape[iii] for iii in range(ii + 1, len(shape)) ])
        sum_ += coord * mul
    return sum_

def enumershape(shape):
    pieces = [[elm for elm in range(shape[ii])] for ii in range(len(shape))]
    ii = -1
    for elm in product(*pieces):
        ii += 1
        yield (ii, elm)


def iterprob(actions):
    """Generator for iterating through an array of player action probabilities.
       Yields a tuple (player_actions, probability) where player_actions is a tuple showing
        which player performed which action."""
    pos = [0] * len(actions)
    done = False
    while not done:
        pospos = 0
        while pos[pospos] == len(actions[pospos]) - 1:
            pospos += 1
            if pospos == len(actions):
                done = True
                break
        prob = 1
        for ii in range(len(actions)):
            prob *= actions[ii][pos[ii]]
        # print(pos, pospos)
        oldpos = tuple(pos)
        if not done:
            pos[pospos] += 1
            for ii in range(pospos):
                pos[ii] = 0
        # print('oldpos', oldpos, 'prob', prob)
        yield (oldpos, prob)
        
def itersupport(support_actions):
    """Generator for iterating through support_actions. Support_actions is a list of lists, first index in player.
       Inner list is a tuple, (player_action, probility).
       probability is either a symbol or a number
       yields a tuple (player_actions, probability). Probability is either a number or a symbol expression."""
    pos = [0] * len(support_actions)
    done = False
    while not done:
        pospos = 0
        while pos[pospos] == len(support_actions[pospos]) - 1:
            pospos += 1
            if pospos == len(support_actions):
                done = True
                break
        prob = 1
        palist = []
        for ii in range(len(support_actions)):
            # print(ii, support_actions[ii][pos[ii]])
            palist.append( support_actions[ii][pos[ii]][0])
            prob *= support_actions[ii][pos[ii]][1]
        # print(pos, pospos)
        if not done:
            pos[pospos] += 1
            for ii in range(pospos):
                pos[ii] = 0
        # print('oldpos', oldpos, 'prob', prob)
        yield (tuple(palist), prob)
    

def iterindices(shape):
    """Iterate over possible indices given a shape tuple."""
    pos = [0] * len(shape)
    done = False
    while not done:
        pospos = 0
        while pos[pospos] == shape[pospos] - 1:
            pospos += 1
            if pospos == len(shape):
                done = True
                break
        oldpos = tuple(pos)
        if not done:
            pos[pospos] += 1
            for ii in range(pospos):
                pos[ii] = 0
        yield oldpos
        
def subsets(aset):
   """Yield all subsets of an iterable (except the empty set)"""
   for alen in range(1, len(aset) + 1):
       for acombo in combinations(aset, alen):
           yield(acombo)
        
def iter_subset_combos(actions):
    """Generator to find combinations of subsets of a list of lists.
       Yields a list of lists."""
    pos = [0] * len(actions)
    action_subsets = []
    for i in range(len(actions)):
        #print(i, actions[i], list(subsets(actions[i])))
        action_subsets.append(list(subsets(actions[i]))) 
    done = False
    while not done:
        pospos = 0
        while pos[pospos] == len(action_subsets[pospos]) - 1:
            pospos += 1
            if pospos == len(actions):
                done = True
                break
        prob = 1
        sslist = []
        for ii in range(len(actions)):
            # print(ii, support_actions[ii][pos[ii]])
            sslist.append( action_subsets[ii][pos[ii]])
        # print(pos, pospos)
        if not done:
            pos[pospos] += 1
            for ii in range(pospos):
                pos[ii] = 0
        # print('oldpos', oldpos, 'prob', prob)
        yield sslist
        
def is_pure(profile):
    """Is the profile (list of lists) pure (each player is playing exactly one stratgy)? Returns a boolean."""
    for elm in profile:
        if len(elm) != 1:
            return False
    return True
    
def dict_to_list(adict):
    """Turn a dict into a list of pairs"""
    return [[key, adict[key]] for key in adict]

def list_to_dict(alist):
   """Turn a list of list pairs into a dict"""
   return {elm[0]:elm[1] for elm in alist}

def zero_sum_dict(adict):
    """Given adict, return a new dict where the values x are replaced with [x, -x]"""
    result = {key:[adict[key], -1 * adict[key]] for key in adict}
    return result

def zero_sum_2_player_payoffs(payoffs):
    """Convert payoffs array with just the results for one player to one for a two-player game."""
    result = []
    for elm in payoffs:
        sresult = []
        for sub in elm:
            sresult.append([sub, -sub])
        result.append(sresult)
    return numpy.array(result)

def symmetric_2_player_payoffs(payoffs):
    """For a 2-player game, create a symmetric payoffs array given the payoffs for one player."""
    result = numpy.zeros((len(payoffs), len(payoffs), 2))
    for ii, elm in enumerate(payoffs):
        for iii, sub in enumerate(elm):
            result[(ii, iii, 0)] = sub
            result[(iii, ii, 1)] = sub
    return result


def payout_array_from_dict(payout_dict):
    """Given a payout dict (key is tuple of player actions), return a payouts numpy array"""
    for akey in payout_dict.keys():
        allkeys = [set() for ii in range(len(akey))]
    for akey in  payout_dict.keys():
        for ii, action in enumerate(akey):
            allkeys[ii].add(action)
    lol = 'nope'
    allkeys = [sorted(list(elm)) for elm in allkeys]
    lol = 'nope'
    shape = [len(akey) for akey in allkeys]
    shape.append(len(shape))
    shape = tuple(shape)
    payoffs = numpy.zeros(shape)
    for akey in product(*allkeys):
        for ii, apayout in enumerate(payout_dict[tuple(akey)]):
            pos = list(akey)
            pos.append(ii)
            payoffs[tuple(pos)] = apayout
    return payoffs

def silly(pos):
    """A silly test function that gives a result based on pos. Pos is a list of ints."""
    #print('silly')
    result = 0
    for ii in range(len(pos)):
        result += (10 ** ii) * (pos[ii] + 1)
    return result


def test_pos_from_coords():
    shape = (3,3,2)
    for ii in range(3):
        for iii in range(3):
            for iv in range(2):
                print(pos_from_coords(shape, (ii, iii, iv)))
