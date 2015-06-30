"""Simple method to detect points on the interior or exterior of a closed 
polygon.  Returns a boolean for single points, or an array of booleans for a 
line masking the segment(s) of the line within the polygon.

For each point, operates via a ray-casting approach -- the function projects 
a semi-infinite ray parallel to the positive horizontal axis, and counts how 
many edges of the polygon this ray intersects.  For a simply-connected 
polygon, this determines whether the point is inside (even number of crossings) 
or outside (odd number of crossings) the polygon, by the Jordan Curve Theorem.
"""
import numpy as np

def contains(polyx,polyy,linex,liney):
    """Calculate whether given points are within a 2D simply-connected polygon.
    Returns a boolean 

    ARGS:
        polyx: array-like.
            Array of x-coordinates of the vertices of a polygon.
        polyy: array-like.
            Array of y-coordinates of the vertices of a polygon.  Must match 
            dimension of polyx.
        linex: array-like or float.
            x-coordinate(s) of test point(s).
        liney: array-like or float.
            y-coordiante(s) of test point(s).  Must match dimension of linex.

    RETURNS:
        mask: boolean or array of booleans.
            For each (linex,liney) point, True if point is in the polygon, 
            else False.
    """
    # check type, dimensions of polyx,polyy
    try:
        # check that polyx, polyy are iterable
        iter(polyx)
        iter(polyy)
    except TypeError:
        raise TypeError("polyx, polyy must be iterable")
    if len != len(polyy):
        raise ValueError("polyx, poly must be of same size")
    if len(polyx) < 3:
        raise ValueError("polygon must consist of at least three points")

    # handler for single-value vs. array versions for linex, liney
    single_val = True
    try:
        iter(linex)
    except TypeError:
        linex = np.asarray([linex],dtype=float)
    else:
        linex = np.asarray(linex,dtype=float)
        single_val = False

    try:
        iter(liney)
    except TypeError:
        liney = np.asarray([liney],dtype=float)
    else:
        liney = np.asarray(liney,dtype=float)
        single_val = False

    if linex.shape != liney.shape:
        raise ValueError("linex, liney must be of same shape")
    
    # generator for points in polygon
    def lines():
        p0x = polyx[-1]
        p0y = polyy[-1]
        p0 = (p0x,p0y)
        for i,x in enumerate(polyx):
            y = polyy[i]
            p1 = (x,y)
            yield p0,p1
            p0 = p1

    mask = np.array([False for i in range(len(linex))])
    for i,x in enumerate(linex):
        y = liney[i]
        result = False

        for p0,p1 in lines():
            if ((p0[1] > y) != (p1[1] > y)) and (x < ((p1[0]-p0[0])*(y-p0[1])/(p1[1]-p0[1]) + p0[0])):
                result = not result 
        mask[i] = result

    # recast mask -- single Boolean if single_val inputs, else return array of booleans
    if single_val:
        mask = mask[0]

    return mask
