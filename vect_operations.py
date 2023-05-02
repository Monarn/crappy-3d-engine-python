from math import sqrt
import numpy as np

def multiply_matrices(matrix1, matrix2):
    """
    Multiplies two matrices and returns the result as a new matrix.

    Args:
    matrix1 (list of lists): A matrix represented as a list of lists.
    matrix2 (list of lists): A matrix represented as a list of lists.

    Returns:
    list of lists: The resulting matrix.
    """
    # Determine the number of rows and columns for each matrix.
    rows1 = len(matrix1)
    cols1 = len(matrix1[0])
    rows2 = len(matrix2)
    cols2 = len(matrix2[0])

    # Check that the matrices can be multiplied.
    if cols1 != rows2:
        raise ValueError("Matrices cannot be multiplied.")

    # Create the resulting matrix.
    result = [[0 for j in range(cols2)] for i in range(rows1)]

    # Multiply the matrices.
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result

def multiply_matrix_vector(matrix, vector):
    """
    Multiplies a matrix with a vector and returns the result as a new vector.

    Args:
    matrix (list of lists): A matrix represented as a list of lists.
    vector (list): A vector represented as a list.

    Returns:
    list: The resulting vector.
    """
    # Determine the number of rows and columns for the matrix.
    rows = len(matrix)
    cols = len(matrix[0])

    # Check that the number of columns in the matrix matches the length of the vector.
    if cols != len(vector):
        raise ValueError("Matrix and vector cannot be multiplied.")

    # Create the resulting vector.
    result = [0 for i in range(rows)]

    # Multiply the matrix and vector.
    for i in range(rows):
        for j in range(cols):
            result[i] += matrix[i][j] * vector[j]

    return result

def normalize(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

def dot(vec1, vec2):
    return (vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2])

def cross(a, b):
    result = [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]

    return result

def vector_sub(vec1, vec2):
    return [vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]]

def vector_add(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]]

def vector_mult(a, b):
    return np.array([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

def vector_mult_by_scal(vec2, scal):
    return [scal * vec2[0], scal * vec2[1], scal * vec2[2]]

def rotate(vector, axis, angle):
    """
    Rotate a vector around an arbitrary axis by a given angle.
    
    Args:
        vector (np.array): the vector to rotate.
        axis (np.array): the rotation axis.
        angle (float): the rotation angle in radians.
        
    Returns:
        np.array: the rotated vector.
    """
    axis = normalize(axis)
    a = np.cos(angle / 2.0)
    b, c, d = -axis * np.sin(angle / 2.0)
    rotation_matrix = np.array([[a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c)],
                                [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
                                [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c]])
    return np.dot(rotation_matrix, vector)

