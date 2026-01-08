"""
Library for creating the connectivity and coordinate matrices for a structure
formed by cubic elements.
"""
#==================================================================================
#LIBRARIES IMPORT
#==================================================================================
import numpy as np
#==================================================================================
#FUNCTION FOR CREATING THE CONNECTIVITY AND COORDINATE MATRICES
#==================================================================================
def create_mcs (EZ, EY, EX, W, H, L):
    """
    Function for creating the connectivity and coordinate matrices. It receives
    as parameters the number of elements in the Z direction, in the Y direction, 
    and in the X direction, as well as the size of the structure in the same 
    directions Z, Y, X. Returns two matrices. The first is the connectivity 
    matrix, where each row is a list of the vertex indices that compose each
    cubic element, and the second is the coordinate matrix, where each row 
    corresponds to the coordinates of the vertex with that index.
    """
    #==================================================================================
    # DETERMINATION OF THE PARAMETERS BASED ON THE STRUCTURE
    #==================================================================================
    NX = EX + 1              #Number of points on the X axis
    NY = EY + 1              #Number of points on the Y axis
    NZ = EZ + 1              #Number of points on the Z axis
    NPP = NX * NY            #Number of points per layer
    NEP = EX * EY            #Number of elements per layer
    NP = NPP * NZ            #Number of points in total
    NE = NEP * EZ            #Number of elements in total
    #==================================================================================
    # DETERMINATION OF THE COORDINATES OF THE EXISTING POINTS
    #==================================================================================
    X = np.concatenate (([0.0] , np.linspace ( 0 , L , NX )))
    Y = np.concatenate (([0.0] , np.linspace ( 0 , H , NY )))
    Z = np.concatenate (([0.0] , np.linspace ( 0 , W , NZ )))
    #==================================================================================
    # INITIALIZATION OF THE CONNECTIVITY AND COORDINATE MATRICES
    #==================================================================================
    mconect = np.full ( ( NE + 1, 8 ),0)
    mcoord = np.zeros ( ( NP + 1, 3 ))
    #==================================================================================
    # DETERMINATION OF THE CONNECTIVITY AND COORDINATE MATRICES
    #==================================================================================
    elemento = 1
    linha_elementar = 1
    profundidade_elementar = 1
    no_atual = 1
    while elemento <= NE:
        if elemento == 1:
            #==================================================================================
            #FIRST ELEMENT OF THE FIRST LAYER
            #==================================================================================
            mconect [ elemento, : ] = [ 1 , 2 , 3 , 4 , 5 , 6 , 7, 8 ]

            mcoord [ mconect [ elemento, : ], 0 ] = [ X [ 1 ], X [ 2 ], X [ 2 ], X [ 1 ], \
                                                      X [ 1 ], X [ 2 ], X [ 2 ], X [ 1 ] ]
            mcoord [ mconect [ elemento, : ], 1 ] = [ Y [ 1 ], Y [ 1 ], Y [ 1 ], Y [ 1 ], \
                                                      Y [ 2 ], Y [ 2 ], Y [ 2 ], Y [ 2 ] ]
            mcoord [ mconect [ elemento, : ], 2 ] = [ Z [ 1 ], Z [ 1 ], Z [ 2 ], Z [ 2 ], \
                                                      Z [ 1 ], Z [ 1 ], Z [ 2 ], Z [ 2 ] ]
            no_atual += 7

        elif elemento <= EX:
            #====================================================================================
            #FIRST ROW OF THE FIRST LAYER
            #====================================================================================
            mconect [ elemento ] [ : ] = [ mconect [ elemento - 1, 1 ], no_atual + 1, \
                                          no_atual + 2 , mconect [ elemento - 1, 2 ], \
                                          mconect [elemento - 1, 5 ], no_atual + 3, \
                                          no_atual + 4 , mconect [elemento - 1, 6 ] ]    

            mcoord [ mconect [ elemento, [1, 2, 5, 6] ], 0 ] = [ X [ elemento + 1 ], \
                                                                 X [ elemento + 1 ], \
                                                                 X [ elemento + 1 ], \
                                                                 X [elemento + 1 ] ]
            mcoord [ mconect [ elemento, [1, 2, 5, 6] ], 1 ] = [ Y [ 1 ], Y [ 1 ], \
                                                                 Y [ 2 ], Y [ 2 ] ]
            mcoord [ mconect [ elemento, [1, 2, 5, 6] ], 2 ] = [ Z [ 1 ], Z [ 2 ], \
                                                                 Z [ 1 ], Z [ 2 ] ]
            no_atual += 4

        elif elemento == ( ( linha_elementar - 1 ) * EX ) + 1 and profundidade_elementar == 1:
            #====================================================================================
            #FIRST COLUMN OF THE FIRST LAYER
            #====================================================================================
            mconect [ elemento ] [ : ] = [ mconect [ elemento - EX ] [ 4 ], \
                                           mconect [ elemento - EX ] [ 5 ], \
                                           mconect [ elemento - EX ] [ 6 ], \
                                           mconect [ elemento - EX ] [ 7 ],\
                                           no_atual + 1, no_atual + 2, \
                                           no_atual + 3, no_atual + 4]

            mcoord [ mconect [ elemento, 4:8 ], 0 ] = [ X [ 1 ], X [ 2 ], X [ 2 ], X [ 1 ] ]
            mcoord [ mconect [ elemento, 4:8 ], 1 ] = [ Y [ linha_elementar + 1 ], \
                                                        Y [ linha_elementar + 1 ], \
                                                        Y [ linha_elementar + 1 ], \
                                                        Y [ linha_elementar + 1 ] ]
            mcoord [ mconect [ elemento, 4:8 ], 2 ] = [ Z [ 1 ], Z [ 1 ], Z [ 2 ], Z [ 2 ] ]
            no_atual += 4

        elif profundidade_elementar == 1:
            #====================================================================================
            #REMAINDER OF THE FIRST LAYER (NOT IN THE FIRST COLUMN NOR IN THE FIRST ROW)
            #====================================================================================
            mconect [ elemento ] [ : ] = [ mconect [ elemento - EX ] [ 4 ], \
                                           mconect [ elemento - EX ] [ 5 ], \
                                           mconect [ elemento - EX ] [ 6 ], \
                                           mconect [ elemento - EX ] [ 7 ], \
                                           mconect [ elemento - 1 ] [ 5 ], no_atual + 1, \
                                           no_atual + 2 , mconect [ elemento - 1 ] [ 6 ] ]

            mcoord [ mconect [ elemento, [5, 6] ], 0 ] = [ mcoord [ mconect [ elemento - EX , 1 ], 0 ], \
                                                           mcoord [ mconect [ elemento - EX , 1 ], 0 ] ]
            mcoord [ mconect [ elemento, [5, 6] ], 1 ] = [ mcoord [ mconect [ elemento - 1 , 5 ], 1 ], \
                                                           mcoord [ mconect [ elemento - 1 , 5 ], 1 ] ]
            mcoord [ mconect [ elemento, [5, 6] ], 2 ] = [ Z [ 1 ], Z [ 2 ] ]
            no_atual += 2

        elif elemento == ( ( profundidade_elementar - 1) * NEP ) + 1:
            #====================================================================================
            #FIRST ELEMENT OF THE LAYERS EXCEPT THE FIRST
            #====================================================================================
            mconect [ elemento, : ] = [ mconect [ elemento - NEP ] [ 3 ], \
                                        mconect [ elemento - NEP ] [ 2 ], \
                                        no_atual + 2, no_atual + 1, \
                                        mconect [ elemento - NEP ] [ 7 ], \
                                        mconect [ elemento - NEP ] [ 6 ], \
                                        no_atual + 3, no_atual + 4 ]

            mcoord [ mconect [ elemento, [2, 3, 6, 7] ], 0 ] = [ mcoord [ mconect [ elemento , 1 ], 0 ], \
                                                                 mcoord [ mconect [ elemento , 0 ], 0 ],\
                                                                 mcoord [ mconect [ elemento , 1 ], 0 ],\
                                                                 mcoord [ mconect [ elemento , 0 ], 0 ] ]
            mcoord [ mconect [ elemento, [2, 3, 6, 7] ], 1 ] = [ mcoord [ mconect [ elemento , 1 ], 1 ], \
                                                                 mcoord [ mconect [ elemento , 0 ], 1 ],\
                                                                 mcoord [ mconect [ elemento , 5 ], 1 ],\
                                                                 mcoord [ mconect [ elemento , 4 ], 1 ] ]
            mcoord [ mconect [ elemento, [2, 3, 6, 7] ], 2 ] = [ Z [ profundidade_elementar + 1 ], \
                                                                 Z [ profundidade_elementar + 1 ],\
                                                                 Z [ profundidade_elementar + 1 ], \
                                                                 Z [ profundidade_elementar + 1 ]]
            no_atual += 4

        elif elemento <= ( ( profundidade_elementar -1 ) * NEP ) + EX:
            #====================================================================================
            #FIRST ROW OF THE LAYERS EXCEPT THE FIRST
            #====================================================================================
            mconect [ elemento, : ] = [ mconect [ elemento - 1 ] [ 1 ], \
                                        mconect [ elemento - NEP ] [ 2 ], \
                                        no_atual + 1, mconect [ elemento - 1 ] [ 2 ], \
                                        mconect [ elemento - 1 ] [ 5 ], \
                                        mconect [ elemento - NEP ] [ 6 ], \
                                        no_atual + 2, mconect [ elemento - 1 ] [ 6 ] ]

            mcoord [ mconect [ elemento, [2, 6 ] ], 0 ] = [ mcoord [ mconect [ elemento - NEP , 1 ], 0 ], \
                                                            mcoord [ mconect [ elemento - NEP , 1 ], 0 ] ]
            mcoord [ mconect [ elemento, [2, 6 ] ], 1 ] = [ mcoord [ mconect [ elemento - NEP , 1 ], 1 ], \
                                                            mcoord [ mconect [ elemento - NEP , 5 ], 1 ] ]
            mcoord [ mconect [ elemento, [2, 6 ] ], 2 ] = [ Z [ profundidade_elementar + 1 ], \
                                                           Z [ profundidade_elementar + 1 ] ]
            no_atual += 2

        elif elemento == ( ( linha_elementar - 1 ) * EX ) + 1:
            #====================================================================================
            #FIRST COLUMN OF THE LAYERS EXCEPT THE FIRST
            #====================================================================================
            mconect [ elemento, : ] = [ mconect [ elemento - EX ] [ 4 ], \
                                        mconect [ elemento - EX ] [ 5 ], \
                                        mconect [ elemento - EX ] [ 6 ], \
                                        mconect [ elemento - EX ] [ 7 ], \
                                        mconect [ elemento - NEP ] [ 7 ], \
                                        mconect [ elemento - NEP ] [ 6 ], \
                                        no_atual + 1, no_atual + 2 ]

            mcoord [ mconect [ elemento, 6:8 ], 0 ] = [ mcoord [ mconect [ elemento - NEP , 5 ], 0 ], \
                                                        mcoord [ mconect [ elemento - NEP , 4 ], 0 ] ]
            mcoord [ mconect [ elemento, 6:8 ], 1 ] = [ mcoord [ mconect [ elemento - NEP , 5 ], 1 ], \
                                                        mcoord [ mconect [ elemento - NEP , 4 ], 1 ] ]
            mcoord [ mconect [ elemento, 6:8 ], 2 ] = [ Z [ profundidade_elementar + 1 ], \
                                                       Z [ profundidade_elementar + 1 ] ] 
            no_atual += 2
        else:
            #====================================================================================
            #REMAINDER OF THE OTHER LAYERS EXCEPT THE FIRST (NOT IN THE FIRST COLUMN
            #NOR IN THE FIRST ROW NOR IN THE FIRST LAYER)
            #====================================================================================
            mconect [ elemento ] [ : ] = [ mconect [ elemento - EX, 4 ], \
                                           mconect [ elemento - EX, 5 ], \
                                           mconect [ elemento - EX, 6 ], \
                                           mconect [ elemento - EX, 7 ],\
                                           mconect [ elemento - 1, 5 ], \
                                           mconect [ elemento - NEP, 6 ],\
                                           no_atual + 1, mconect [ elemento - 1, 6 ] ]

            mcoord [ mconect [ elemento, 6 ], : ] = [ mcoord [ mconect [ elemento - NEP , 5 ], 0 ],\
                                                      mcoord [ mconect [ elemento - NEP , 5 ], 1 ],\
                                                      Z [ profundidade_elementar + 1 ] ]
            no_atual += 1
        if elemento == EX * linha_elementar:
            linha_elementar += 1
        if elemento == NEP * profundidade_elementar:
            profundidade_elementar += 1
        elemento += 1
    return mconect, mcoord

