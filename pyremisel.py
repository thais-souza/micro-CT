"""
Biblioteca para a determinação do ID do elemento dentro da matriz e para a 
eliminação dos elementos flutuantes utilizando o Union-Find.
"""
#==================================================================================
#IMPORTAÇÃO DAS BIBLIOTECAS
#==================================================================================
import numpy as np
import copy
#==================================================================================
#FUNÇÃO DE IDENTIFICAÇÃO DO ID
#==================================================================================
def id(position, size):
    """
    Função para a determinação da relação entre a posição na matriz 3D e o ID do 
    elemento. A entrada da função é a posição do elemento na matriz no formato
    (z, y, x) e o tamanho total da matriz, também no formato (Z, Y, X). A
    saída é o seu respectivo ID.
    """
    id = position[0] * size [1] * size [2] + position[1] * size [2] + position[2]
    return id
#==================================================================================
#FUNÇÃO DE ELIMINAÇÃO DOS ELEMENTOS FLUTUANTES
#==================================================================================
def elim_isel(im, MELT, CFP):
    """
    Função para a eliminação dos elementos flutuantes. Ela recebe como parâmetros
    a matriz em questão, o módulo de elasticidade do material constituinte e o 
    coeficiente de poisson também do material. A sua saída é uma matriz com os
    elementos flutuantes igualados a zero e um vetor contendo o (mód. elasticidade,
    coef. de poisson) de cada elemento. Aqueles elementos que são vazios estarão com
    (0,0).
    """
    size = im.shape
    area = size[0]*size[1]*size[2] 
    #==================================================================================
    #INICIALIZAÇÃO DOS VETORES NECESSÁRIOS PARA O UNION-FIND
    #==================================================================================
    #O vetor "parent" será utilizado para armazenar o ID do pai daquele elemento,
    #relacionado com o pai do conjunto que ele faz parte, e o vetor "qty" para 
    #armazenar a quantidade de elementos presentes em cada conjunto, possibilitando 
    #determinar qual o maior conjunto e eliminar todos os elementos que não são seus
    #constituintes
    parent = np.full((area), range(area))
    qty = np.full((area), 1)
    #==================================================================================
    #DEFINIÇÃO DAS FUNÇÕES NECESSÁRIAS PARA O UNION-FIND
    #==================================================================================
    #O "find" encontrará o pai daquele elemento enquanto o "join" juntará um elemento
    #ao conjunto que ele faz parte
    def find(x):
        nonlocal parent
        if(parent[x] == x):
            return x
        parent [x] = find(parent[x])
        return parent[x]
    def join (x, y):
        nonlocal parent
        nonlocal qty
        x = find(x)
        y = find(y)
        if (x == y):
            return
        if (qty[x] <= qty[y]):
            parent[x] = y
            qty [y] += qty [x]
        else:
            parent[y] = x
            qty [x] += qty [y]
    #==================================================================================
    #APLICAÇÃO DO UNION-FIND
    #==================================================================================
    #São agregados no mesmo conjunto os elementos adjacentes que possuem material, 
    #ou seja, que não estão vazios
    for z in range(size[0]):
        for y in range(size[1]):
            for x in range (size[2]):
                position = (z, y, x)
                if (im[position] == 255):
                    options = [-1, 0, 1]
                    for k in options:
                        for j in options:
                            for i in options:
                                if ((i,j,k) == (0,0,0)):
                                    continue
                                if ((x+i) >= 0 and (x+i) < size [2] and \
                                    (y+j) >= 0 and (y+j) < size[1]\
                                    and (z+k) >= 0 and (z+k) < size[0]):
                                    adj = (z+k, y+j, x+i)
                                    if (im[adj] == 255):
                                        join(id(position, size), id(adj, size))
    #==================================================================================
    #ELIMINAÇÃO DOS ELEMENTOS FLUTUANTES
    #==================================================================================
    #Cria-se uma matriz com os elementos flutuantes  
    #zerados. Os elementos flutuantes são todos aqueles que não fazem parte do
    #maior conjunto existente na estrutura (determinado pelo número de elementos)
    #conectados entre si. Também é gerado um vetor para armazenar o material
    #constituinte de cada elemento (arcabouço ou vazio)
    material_elementos = np.empty((area + 1), dtype = object)
    material_elementos.fill ((0,0))
    contador = 0
    parent_bgg = np.where(qty == np.amax(qty))
    elim_im = copy.deepcopy (im)
    for z in range(size[0]):
        for y in range(size[1]):
            for x in range (size[2]):
                position = (z, y, x)
                idty = id(position, size)
                if (find(idty) != parent_bgg and im[position] != 0):
                    elim_im [position] = 0
                if elim_im [position] != 0:
                    material_elementos [idty + 1] = (MELT, CFP)
    return elim_im, material_elementos        

