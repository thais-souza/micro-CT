The goal of this project is to convert a pre-processed micro-CT image of scaffolds for cell deposition (from micro-CT in .tif/.tiff format) into mesh files compatible with Finite Element Method (FEM) simulations of the full system: scaffold + cells + mechanical stimulus.

The pipeline takes a segmented 3D .tif volume as input and outputs mesh files (.msh and .ply) that can be imported into FEM software such as ANSYS, enabling simulations of the coupled ensemble under external stimulation.

The final mesh is composed of tetrahedral elements, as shown below.

<img width="1448" height="985" alt="Mesh comparison after smoothing" src="https://github.com/user-attachments/assets/f81d2d9b-b0bb-4ec9-a0a2-cd0c6b7a3035" />

To run the pipeline, refer to the example provided in main.ipynb. The workflow requires:

pip install trimesh==3.22.5


⚠️ Note: newer versions of Trimesh may not support parts of the legacy Gmsh interface previously used in this project.
