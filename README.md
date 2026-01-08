The goal of this project is to transform a pre-processed 3D micro-CT image of a scaffold (.tif/.tiff) into mesh files that can be used to run FEM simulations of the scaffold combined with deposited cells under mechanical stimulation.

The pipeline takes a segmented 3D .tif volume as input and outputs mesh files (.msh and .ply) that can be imported into FEM software such as ANSYS, enabling simulations of the coupled ensemble under external stimulation.

The final mesh is composed of tetrahedral elements, as shown below.

<img width="1448" height="842" alt="image" src="https://github.com/user-attachments/assets/fb697333-a007-4821-bae5-c05246ef2a3d" />

To run the pipeline, refer to the example provided in main.ipynb. The workflow requires: pip install trimesh==3.22.5.

Note: newer versions of Trimesh may not support parts of the legacy Gmsh interface previously used in this project.
