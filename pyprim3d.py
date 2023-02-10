"""
Biblioteca para a formação de elementos tetraédricos a partir de uma superfície
triangular (antes da formação desses elementos é feito ainda a subdivisão das
faces caso necessário e o smooth). A biblioteca também gera uma figura para a 
comparação da estrutura antes e depois do smooth (a figura aparece dentro do 
JUPYTER NOTEBOOK).
"""
#==================================================================================
#IMPORTAÇÃO DAS BIBLIOTECAS
#==================================================================================
import pyvista as pv
import trimesh
#==================================================================================
#FUNÇÃO PARA A FORMAÇÃO DOS TETRAEDROS
#==================================================================================
def smooth_tmsh (mcoord, mconect_faces_triangle, TAM_VOX, nm_export, n_subd, it_smooth):
    """
    Função para a formação dos tetraedros. Recebe como parâmetros a matriz de 
    coordenadas, a matriz de conectividade das faces triangulares, o tamanho dos
    catetos (nesse caso assumidos como iguais), o nome do arquivo a ser gerado 
    (nm_export.ply), o número de subdivisões desejado (cada aumento de uma unidade
    corresponde a divisão de cada face em 3 dezes) e o número de iterações para
    o smooth da malha. Assim, antes de formar os tetraedros a função remove os 
    vértices isolados, as faces repetidas, subdivide a malha e realiza o smooth. 
    Não há retorno, mas sim a geração de dois arquivos .ply de nomes 
    "<nm_export>.ply" e "<nm_export_smooth>.ply" que correspondem ao resultado 
    depois da subdivisão e depois do smooth, respectivamente. No final ainda há
    a geração de um arquivo "<nm_export.msh", relativo ao arquivo com os elementos
    tetraédricos. 
    """
    #==================================================================================
    #IMPORTAÇÃO PARA O TRIMESH
    #==================================================================================
    mesh_trimesh = trimesh.Trimesh(vertices = mcoord[1:], faces = mconect_faces_triangle, \
                                             process = False)
    #==================================================================================
    #REMOÇÃO DOS VÉRTICES NÃO CONECTADOS A NENHUMA FACE
    #==================================================================================
    mesh_trimesh.remove_unreferenced_vertices()
    #==================================================================================
    #REMOÇÃO DAS FACES REPETIDAS
    #==================================================================================
    trimesh.tol.merge = TAM_VOX/10
    mesh_trimesh.process(validate=True, merge_tex=None, merge_norm=None)
    #==================================================================================
    #SUBDIVISÃO (CADA SUBDIVISÃO CORRESPONDE A X4 A QUANTIDADE DE FACES ORIGINAL)
    #==================================================================================
    for i in range (n_subd):
        mesh_trimesh = mesh_trimesh.subdivide()
    mesh_trimesh.export(nm_export + ".ply")
    #==================================================================================
    #SMOOTH DA ESTRUTURA SUBDIVIDIDA
    #==================================================================================
    trimesh.smoothing.filter_laplacian(mesh_trimesh, iterations=it_smooth)
    mesh_trimesh.export(nm_export + "_smooth.ply")
    #==================================================================================
    #FORMAÇÃO DOS TETRAEDROS
    #==================================================================================
    trimesh.interfaces.gmsh.to_volume(mesh_trimesh, file_name=nm_export + "_smooth.msh", \
                                      max_element=None, mesher_id=1)
#==================================================================================
#FUNÇÃO PARA O PLOT DA ESTRUTURA ANTES E DEPOIS DO SMOOTH
#==================================================================================
def smooth_plot (nm_bf_smooth, nm_aft_smooth):
    """
    Função para a plotagem da estrutura antes e depois do smooth. Recebe como 
    parâmetros o nome do arquivo (do formato .ply) antes do smooth e o nome
    do arquivo (também .ply) depois do smooth. A imagem formada consiste apenas
    no traçado da estrutura antes do smooth e a estrutura completa depois do
    smooth.
    """
    #==================================================================================
    #CARREGAMENTO DOS DOIS ARQUIVOS
    #==================================================================================
    mesh_polydata = pv.PolyData(nm_bf_smooth)
    mesh_polydata_smooth = pv.PolyData(nm_aft_smooth)
    #==================================================================================
    #EXTRAÇÃO APENAS DO TRAÇADO DA ESTRUTURA ANTES DO SMOOTH
    #==================================================================================
    orig_edges = mesh_polydata.extract_feature_edges()
    #==================================================================================
    #DETERMINAÇÃO DAS CARACTERÍSTICAS DE VISUALIZAÇÃO NO JUPYTER NOTEBOOK
    #==================================================================================
    pv.set_plot_theme('document')
    pv.global_theme.jupyter_backend = 'panel'
    #==================================================================================
    #FORMAÇÃO DA IMAGEM
    #==================================================================================
    pl = pv.Plotter()
    pl.add_mesh(mesh_polydata_smooth, show_edges=True, show_scalar_bar=True)
    pl.add_mesh(orig_edges, show_scalar_bar=True, color='k', line_width=2)
    pl.show()