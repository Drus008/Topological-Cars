from numpy import sin, cos, array

import numpy as np

def rotationMatrix(rads:float)->array:
    """
    It gives a 2x2 matrix of a rotation of the desired angle.
    
    Args:
        rads (float): the angle of the rotation in radians.
    
    Returns:
        The 2D matrix of the rotation.
    """
    s = sin(rads)
    c = cos(rads)
    return array([[c, -s], [s, c]])

def direction2D(angle:float)->array:
    """
    Given an angle, it returns its direction.
    
    Args:
        angle: The angle (in radians) you want to have the direction.
    
    Returns:
        A 2D array with the direction.
    """

    return array([cos(angle), sin(angle)])

def baseChange(b1: array, b2: array, v:array)->array:
    """
    It's a function to change a vector from the canonical basis to another one.
    
    Args:
        b1 (array): The first vector of the basis.
        b2 (array): The second vector of the basis.
        v (array): The vector that you want to express in the basis b1, b2.
    
    Returns:
        The coordinates of the vector v in the basis b1, b2.
    """
    baseMatrix = array([b1,b2])
    return np.linalg.solve(baseMatrix, v)

def baseChangeOrt(b1: array, b2: array, v):
    """
    It's a function to change a vector from the canonical basis to another orthonormal basis.

    It is faster than baseChange due to not needing to solve a linear system.
    
    Args:
        b1 (array): The first vector of the orthonormal basis.
        b2 (array): The second vector of the orthonormal basis.
        v (array): The vector that you want to express in the basis b1, b2.
    
    Returns:
        The coordinates of the vector v in the basis b1, b2.
    """
    baseMatrix = np.column_stack((b1,b2))
    return baseMatrix.T @ v

def baseReturnOrt(b1: array, b2: array, v):
    """
    It's a function to change a vector expressed in some orthogonal basis to the canonical basis.
    
    Args:
        b1 (array): The first vector of the orthonormal basis.
        b2 (array): The second vector of the orthonormal basis.
        v (array): The coordinates of a vector expressed in the basis b1, b2 that you want to express in canonical basis.
    
    Returns:
        The coordinates of the vector v in the canonical basis.
    """
    baseMatrix = np.column_stack((b1,b2))
    return baseMatrix @ v