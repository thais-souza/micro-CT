"""
Biblioteca para criação das matrizes de conectividade e de coordenadas para uma 
estrutura formada por elementos cúbicos.
"""
#==================================================================================
#IMPORTAÇÃO DAS BIBLIOTECAS
#==================================================================================
import numpy as np
#==================================================================================
#FUNÇÃO PARA A CRIAÇÃO DAS MATRIZES DE CONECTIVIDADE E DE COORDENADAS 
#==================================================================================
def create_mcs (EZ, EY, EX, W, H, L):
    """
    Função para a criação das matrizes de conectifidade e de coordenadas. Recebe
    como parâmetros o número de elementos da direção Z, na direção Y e na direção
    X, além do tamanho da estrutura nas mesmas direções Z, Y, X. Retorna duas 
    matrizes. A primeira de conectividade, com cada linha sendo uma lista dos
    índices dos vértices que compõem cada elemento cúbico, e a segunda de 
    coordenadas com cada linha correspondente às coordenadas do vértice com 
    aquele índice. 
    """
    #==================================================================================
    # DETERMINAÇÃO DOS PARÂMETROS BASEADOS NA ESTRUTURA
    #==================================================================================
    NX = EX + 1              #Número de pontos no eixo X
    NY = EY + 1              #Número de pontos no eixo Y
    NZ = EZ + 1              #Número de pontos no eixo Z
    NPP = NX * NY            #Número de pontos por camada
    NEP = EX * EY            #Número de elementos por camada
    NP = NPP * NZ            #Número de pontos no total
    NE = NEP * EZ            #Númeto de elementos no total
    #==================================================================================
    # DETERMINAÇÃO DAS COORDENADAS DOS PONTOS EXISTENTES
    #==================================================================================
    X = np.concatenate (([0.0] , np.linspace ( 0 , L , NX )))
    Y = np.concatenate (([0.0] , np.linspace ( 0 , H , NY )))
    Z = np.concatenate (([0.0] , np.linspace ( 0 , W , NZ )))
    #==================================================================================
    # INICIALIZAÇÃO DAS MATRIZES DE CONECTIVIDADE E DE COORDENADAS
    #==================================================================================
    mconect = np.full ( ( NE + 1, 8 ),0)
    mcoord = np.zeros ( ( NP + 1, 3 ))
    #==================================================================================
    # DETERMINAÇÃO DAS MATRIZES DE CONECTIVIDADE E DE COORDENADAS
    #==================================================================================
    elemento = 1
    linha_elementar = 1
    profundidade_elementar = 1
    no_atual = 1
    while elemento <= NE:
        if elemento == 1:
            #==================================================================================
            #PRIMEIRO ELEMENTO DA PRIMEIRA CAMADA
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
            #PRIMEIRA LINHA DA PRIMEIRA CAMADA
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
            #PRIMEIRA COLUNA DA PRIMEIRA CAMADA
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
            #RESTANTE DA PRIMEIRA CAMADA (NÃO ESTÁ NEM NA PRIMEIRA COLUNA NEM NA PRIMEIRA LINHA)
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
            #PRIMEIRO ELEMENTO DAS CAMADAS EXCETO A PRIMEIRA
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
            #PRIMEIRA LINHA DAS CAMADAS EXCETO A PRIMEIRA
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
            #PRIMEIRA COLUNA DAS CAMADAS EXCETO A PRIMEIRA
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
            #RESTANTE DAS OUTRAS CAMADAS EXCETO A PRIMEIRA (NÃO ESTÁ NEM NA PRIMEIRA COLUNA 
            #NEM NA PRIMEIRA LINHA NEM NA PRIMEIRA CAMADA)
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

