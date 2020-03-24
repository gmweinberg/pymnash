import numpy

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
         
    

def silly(pos):
    """A silly test function that gives a result based on pos. Pos is a list of ints."""
    #print('silly')
    result = 0
    for ii in range(len(pos)):
        result += (10 ** ii) * (pos[ii] + 1)
    return result

