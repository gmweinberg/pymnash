import numpy
from fractions import Fraction

def coords_from_pos(thearray, pos):
    """Get the corrdinates from a one-dimensional position and shape. We will make the first index most signifcant."""
    coords = []
    for ii in range(len(thearray.shape) - 1):
        prod = numpy.prod(thearray.shape[1 + ii:])
        coord = pos // prod
        coords.append(coord)
        pos -= coord * prod
    coords.append(pos)
    return tuple(coords)

def iterprob(actions):
    """Generator for iterating through an array of player action probabilities. Yields a tuple (player_actions, probability) where player_actions is a tuple showing
        which player performed which action."""
    pos = [0] * len(actions)
    done = False
    while(not done):
        pospos = 0
        while pos[pospos] == len(actions[pospos]) - 1:
            pospos += 1
            if pospos == len(actions):
                done = True
                break
        prob = 1
        for ii in range(len(actions)):
            prob *= Fraction(actions[ii][pos[ii]]).limit_denominator()
        # print(pos, pospos)
        oldpos = tuple(pos)
        if not done:
            pos[pospos] += 1
            for ii in range(pospos):
                pos[ii] = 0
        # print('oldpos', oldpos, 'prob', prob)
        yield (oldpos, prob)


def silly(pos):
    """A silly test function that gives a result based on pos. Pos is a list of ints."""
    #print('silly')
    result = 0
    for ii in range(len(pos)):
        result += (10 ** ii) * (pos[ii] + 1)
    return result

