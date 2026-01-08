"""
Library for removing the internal faces of a structure formed by triangular surfaces.
"""
#==================================================================================
#IMPORTING THE LIBRARIES
#==================================================================================
import numpy as np
import copy
#==================================================================================
#FUNCTION FOR REMOVING INTERNAL FACES
#==================================================================================
def elim_infa (mconect_all_faces_triangle):
    """
    The function input is a TRIANGULAR connectivity matrix (with each face
    in a different row of the matrix and each row consisting of a list with the
    identification of the three vertices that make up the face). Internal faces
    MUST BE DUPLICATED, but it is not necessary for the duplicate faces to have
    the same vertex ordering. The output is a connectivity matrix without the 
    internal faces.
    """
    #===============================================================================
    #PUT THE FACES WITH THE SAME VERTEX ORDERING (ASCENDING)
    #===============================================================================
    mconect_all_faces_triangle_sort = copy.deepcopy(mconect_all_faces_triangle)
    for triangle in mconect_all_faces_triangle_sort:
        triangle.sort()
    triangulos_unicos = np.unique(mconect_all_faces_triangle_sort, axis=0)
    #===============================================================================
    #RELATION BETWEEN THE FACE INDEX AND THE NUMBER OF TIMES IT REPEATS
    #===============================================================================
    dict_faces = dict()
    for i in range(len(mconect_all_faces_triangle_sort)):
        if str(mconect_all_faces_triangle_sort[i]) in dict_faces.keys():
            dict_faces[str(mconect_all_faces_triangle_sort[i])].append(i)
        else:
            dict_faces[str(mconect_all_faces_triangle_sort[i])] = [i]
    #===============================================================================
    #CREATION OF A LIST CONTAINING ONLY THE INDICES OF THE DUPLICATE FACES
    #===============================================================================
    idx_duplicated_faces = np.array([])
    for face in dict_faces:
        if len(dict_faces[face]) != 1:
            idx_duplicated_faces = np.append (idx_duplicated_faces, dict_faces[face])
    idx_duplicated_faces.sort()
    #===============================================================================
    #REMOVAL OF INTERNAL FACES
    #===============================================================================
    mconect_faces_triangle_shell = []
    for i, face in enumerate(mconect_all_faces_triangle):
        if i not in idx_duplicated_faces:
            mconect_faces_triangle_shell.append(face)
    mconect_faces_triangle_shell = np.array(mconect_faces_triangle_shell)
    #===============================================================================
    #RETURN OF THE TRIANGULAR CONNECTIVITY MATRIX WITHOUT THE INTERNAL FACES
    #===============================================================================
    return mconect_faces_triangle_shell