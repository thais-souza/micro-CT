"""
Library for generating tetrahedral elements from a triangular surface (before 
generating these elements, the faces are subdivided if necessary and smoothing 
is performed). The library also generates a figure for comparing the structure 
before and after smoothing (the figure appears inside the JUPYTER NOTEBOOK).
"""
#==================================================================================
#IMPORTING THE LIBRARIES
#==================================================================================
import pyvista as pv
import trimesh
#==================================================================================
#FUNCTION FOR GENERATING THE TETRAHEDRA
#==================================================================================
def smooth_tmsh (mcoord, mconect_faces_triangle, TAM_VOX, nm_export, n_subd, it_smooth):
    """
    Function for generating the tetrahedra. It receives as parameters the coordinate
    matrix, the connectivity matrix of the triangular faces, the leg length
    (in this case assumed to be equal), the name of the file to be generated
    (nm_export.ply), the desired number of subdivisions (each increase of one unit
    corresponds to dividing each face into 3 parts), and the number of iterations for
    mesh smoothing. Thus, before generating the tetrahedra the function removes
    isolated vertices, duplicate faces, subdivides the mesh, and performs smoothing.
    There is no return, but rather the generation of two .ply files named
    "<nm_export>.ply" and "<nm_export_smooth>.ply", which correspond to the result
    after subdivision and after smoothing, respectively. At the end there is also
    the generation of a "<nm_export.msh" file, related to the file with the
    tetrahedral elements.
    """
    #==================================================================================
    #TRIMESH IMPORT
    #==================================================================================
    mesh_trimesh = trimesh.Trimesh(vertices = mcoord[1:], faces = mconect_faces_triangle, \
                                             process = False)
    #==================================================================================
    #REMOVAL OF VERTICES NOT CONNECTED TO ANY FACE
    #==================================================================================
    mesh_trimesh.remove_unreferenced_vertices()
    #==================================================================================
    #REMOVAL OF DUPLICATE FACES
    #==================================================================================
    trimesh.tol.merge = TAM_VOX/10
    mesh_trimesh.process(validate=True, merge_tex=None, merge_norm=None)
    #==================================================================================
    #SUBDIVISION (EACH SUBDIVISION CORRESPONDS TO 4× THE ORIGINAL NUMBER OF FACES)
    #==================================================================================
    for i in range (n_subd):
        mesh_trimesh = mesh_trimesh.subdivide()
    mesh_trimesh.export(nm_export + ".ply")
    #==================================================================================
    #SMOOTHING OF THE SUBDIVIDED STRUCTURE
    #==================================================================================
    trimesh.smoothing.filter_laplacian(mesh_trimesh, iterations=it_smooth)
    mesh_trimesh.export(nm_export + "_smooth.ply")
    #==================================================================================
    #TETRAHEDRA GENERATION
    #==================================================================================
    trimesh.interfaces.gmsh.to_volume(mesh_trimesh, file_name=nm_export + "_smooth.msh", \
                                      max_element=None, mesher_id=1)
#==================================================================================
#FUNCTION FOR PLOTTING THE STRUCTURE BEFORE AND AFTER SMOOTHING
#==================================================================================
def smooth_plot (nm_bf_smooth, nm_aft_smooth):
    """
    Function for plotting the structure before and after smoothing. It receives as
    parameters the file name (in .ply format) before smoothing and the file name
    (also .ply) after smoothing. The generated image consists only of the
    wireframe of the structure before smoothing and the complete structure after
    smoothing
    """
    #==================================================================================
    #LOADING THE TWO FILES
    #==================================================================================
    mesh_polydata = pv.PolyData(nm_bf_smooth)
    mesh_polydata_smooth = pv.PolyData(nm_aft_smooth)
    #==================================================================================
    #EXTRACTION OF ONLY THE WIREFRAME OF THE STRUCTURE BEFORE SMOOTHING
    #==================================================================================
    orig_edges = mesh_polydata.extract_feature_edges()
    #==================================================================================
    #DETERMINATION OF THE VISUALIZATION SETTINGS IN THE JUPYTER NOTEBOOK
    #==================================================================================
    pv.set_plot_theme('document')
    pv.global_theme.jupyter_backend = 'panel'
    #==================================================================================
    #IMAGE GENERATION
    #==================================================================================
    pl = pv.Plotter()
    pl.add_mesh(mesh_polydata_smooth, show_edges=True, show_scalar_bar=True)
    pl.add_mesh(orig_edges, show_scalar_bar=True, color='k', line_width=2)
    pl.show()