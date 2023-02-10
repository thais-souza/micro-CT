"""
Biblioteca para a eliminação das faces internas de uma estrutura formada por
superfícies triangulares.
"""
#==================================================================================
#IMPORTAÇÃO DAS BIBLIOTECAS
#==================================================================================
import numpy as np
import copy
#==================================================================================
#FUNÇÃO DE ELIMINAÇÃO DAS FACES INTERNAS
#==================================================================================
def elim_infa (mconect_all_faces_triangle):
    """
    A entrada da função é uma matriz de conectividade TRIANGULAR (com cada face
    em uma linha diferente da matriz e cada linha composta por uma lista com a 
    identificação dos três vértices que constituem a face). As faces internas 
    DEVEM ESTAR REPETIDAS, mas não é necessário as 
    faces repetidas estarem com o mesmo ordenamento dos vértices. 
    A saída é uma matriz de conectividade sem as faces internas.
    """
    #===============================================================================
    #COLOCAR AS FACES COM O MESMO ORDENAMENTO DOS VÉRTICES (CRESCENTE)
    #===============================================================================
    mconect_all_faces_triangle_sort = copy.deepcopy(mconect_all_faces_triangle)
    for triangle in mconect_all_faces_triangle_sort:
        triangle.sort()
    triangulos_unicos = np.unique(mconect_all_faces_triangle_sort, axis=0)
    #===============================================================================
    #RELAÇÃO ENTRE O ÍNDICE DA FACE E A QUANTIDADE DE VEZ QUE ELA SE REPETE
    #===============================================================================
    dict_faces = dict()
    for i in range(len(mconect_all_faces_triangle_sort)):
        if str(mconect_all_faces_triangle_sort[i]) in dict_faces.keys():
            dict_faces[str(mconect_all_faces_triangle_sort[i])].append(i)
        else:
            dict_faces[str(mconect_all_faces_triangle_sort[i])] = [i]
    #===============================================================================
    #CRIAÇÃO DE UMA LISTA SOMENTE COM OS ÍNDICES DAS FACES REPETIDAS
    #===============================================================================
    idx_duplicated_faces = np.array([])
    for face in dict_faces:
        if len(dict_faces[face]) != 1:
            idx_duplicated_faces = np.append (idx_duplicated_faces, dict_faces[face])
    idx_duplicated_faces.sort()
    #===============================================================================
    #ELIMINAÇÃO DAS FACES INTERNAS 
    #===============================================================================
    mconect_faces_triangle_shell = []
    for i, face in enumerate(mconect_all_faces_triangle):
        if i not in idx_duplicated_faces:
            mconect_faces_triangle_shell.append(face)
    mconect_faces_triangle_shell = np.array(mconect_faces_triangle_shell)
    #===============================================================================
    #RETORNO DA MATRIZ DE CONECTIVIDADE TRIANGULAR SEM AS FACES INTERNAS
    #===============================================================================
    return mconect_faces_triangle_shell