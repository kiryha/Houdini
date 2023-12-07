import os
import random
from pxr import Usd, UsdGeom
import pymel.core as pm

# Create USD stage
usd_file_path = f'D:/maya_geometry_{random.randint(1, 1000)}.usda'

if os.path.exists(usd_file_path):
    os.remove(usd_file_path)

stage = Usd.Stage.CreateNew(usd_file_path)

# Create a root Xform to hold the USD Mesh objects
root_xform = UsdGeom.Xform.Define(stage, '/root')

# Process scene geometry
scene_geometry = pm.ls(type='mesh')

for mesh in scene_geometry:

    # Create a USD Mesh primitive for the object
    usd_mesh = UsdGeom.Mesh.Define(stage, root_xform.GetPath().AppendChild(mesh.getParent().name()))

    # Initialize lists to collect vertex positions, normals, and face information
    vertex_positions = []
    normals = []
    face_vertex_counts = []
    face_vertex_indices = []

    # Get mesh vertices and iterate over them
    for vtx in mesh.vtx:
        point = vtx.getPosition()
        vertex_positions.append((point[0], point[1], point[2]))

        # You can calculate or obtain normals as well and append them to the 'normals' list
        # For example, if your mesh has per-vertex normals:
        # normal = vtx.getNormal(space='world')  # Adjust the space as needed
        # normals.append((normal[0], normal[1], normal[2]))

    # Define face vertex counts and indices for a single triangle
    face_vertex_counts.append(3)  # For a triangle
    face_vertex_indices.extend([0, 1, 2])  # Vertex indices for the triangle

    # Set the collected attributes for the USD Mesh
    usd_mesh.GetPointsAttr().Set(vertex_positions)
    usd_mesh.GetNormalsAttr().Set(normals)  # Set normals if available
    usd_mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    usd_mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

# Save the USD stage to the file
stage.GetRootLayer().Save()
print(f'>> {usd_file_path}')