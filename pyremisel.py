"""
Library for identifying the element ID inside the matrix and eliminating 
floating elements using the Union-Find (Disjoint Set) data structure.
"""
#==================================================================================
#LIBRARIES IMPORT
#==================================================================================
import numpy as np
import copy
#==================================================================================
#ID IDENTIFICATION FUNCTION
#==================================================================================
def id(position, size):
    """
    Function for determining the relationship between the position in the 3D matrix 
    and the element ID. The function input is the element position in the matrix in
    the format (z, y, x) and the total matrix size, also in the format (Z, Y, X). The
    output is the corresponding ID.
    """
    id = position[0] * size [1] * size [2] + position[1] * size [2] + position[2]
    return id
#==================================================================================
#FUNCTION FOR ELIMINATING FLOATING ELEMENTS
#==================================================================================
def elim_isel(im, MELT, CFP):
    """
    Function for the elimination of floating elements. It receives as parameters
    the matrix in question, the Young’s modulus of the constituent material, and 
    the Poisson’s ratio of the material. The output is a matrix with the floating
    elements set to zero and a vector containing the (Young’s modulus, Poisson’s
    ratio) of each element. Empty elements will contain (0, 0).
    """
    size = im.shape
    area = size[0]*size[1]*size[2] 
    #==================================================================================
    #INITIALIZATION OF THE VECTORS REQUIRED FOR UNION-FIND
    #==================================================================================
    #The "parent" vector will be used to store the parent ID of that element, 
    #related to the representative (root) of the set it belongs to, and the "qty" 
    #vector to store the number of elements present in each set, making it
    #possible to determine the largest set and eliminate all elements that are
    #not its constituents.
    parent = np.full((area), range(area))
    qty = np.full((area), 1)
    #==================================================================================
    #DEFINITION OF THE FUNCTIONS REQUIRED FOR UNION-FIND
    #==================================================================================
    #The "find" function will locate the parent of a given element, while the 
    #"join" function will merge an element into the set it belongs to.
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
    #APPLICATION OF UNION-FIND
    #==================================================================================
    #Adjacent elements that contain material are grouped into the same set,
    #meaning elements that are not empty.
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
    #ELIMINATION OF FLOATING ELEMENTS
    #==================================================================================
    #A new matrix is created with the floating elements set to zero. Floating 
    #elements are all those that are not part of the largest connected set in
    #the structure (determined by the number of elements connected to each other). 
    #A vector is also generated to store the constituent material of each element 
    #(solid framework or empty).
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

