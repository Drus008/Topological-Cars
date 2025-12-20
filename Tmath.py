from numpy import sin, cos, array

import numpy as np

def rotationMatrix(rads:float)->array:
    """
    It gives a 2x2 matrix of a rotation of the desired angle.
    
    Args:
        rads (float): the angle of the rotation in radians.
    
    Returns:
        The 2D matrix of the rotation,
    """
    s = sin(rads)
    c = cos(rads)
    return array([[c, -s], [s, c]])

def direcrion2D(angle:float)->array:
    """
    Given an angle it returns its direction.
    
    Args:
        angle: The angle (in radians) you want to have the direction.
    
    Returns:
        A 2D array with the direction.
    """

    return np.array([cos(angle), sin(angle)])

def baseChange(b1: array, b2: array, v:array)->array:
    """
    Its a function to change a vetor from the canonical base to another one.
    
    Args:
        b1 (array): The first vector of the base.
        b2 (array): The second vector of the base.
        v (array): The vector that you want to express in the base b1,b2.
    
    Returns:
        The coordinates of the vector v in the base b1, b2.
    """
    baseMatrix = np.array([b1,b2])
    return np.linalg.solve(baseMatrix, v)

def baseChangeOrt(b1: array, b2: array, v):
    """
    Its a function to change a vetor from the canonical base to another orthonormal base.

    It is faster than baseChange due to not neading to solve a linear system.
    
    Args:
        b1 (array): The first vector of the orthonormal base.
        b2 (array): The second vector of the orthonormal base.
        v (array): The vector that you want to express in the base b1,b2.
    
    Returns:
        The coordinates of the vector v in the base b1, b2.
    """
    baseMatrix = np.column_stack((b1,b2))
    return baseMatrix.T @ v

def baseReturnOrt(b1: array, b2: array, v):
    """
    Its a function to change a vetor expressed in some orthogonal base to the canonical base.
    
    Args:
        b1 (array): The first vector of the orthonormal base.
        b2 (array): The second vector of the orthonormal base.
        v (array): The coordinates of a vector expressed in the base b1,b1 that you want to express in canonical base.
    
    Returns:
        The coordinates of the vector v in the canonical base.
    """
    baseMatrix = np.column_stack((b1,b2))
    return baseMatrix @ v