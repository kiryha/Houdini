"""
Export geometry from Maya scene to USD file
"""

import os
import random
from pxr import Usd, UsdGeom
import pymel.core as pm

# Create USD stage
usd_file_path = f'D:/maya_geometry_{random.randint(1, 1000)}.usda'

if os.path.exists(usd_file_path):
    os.remove(usd_file_path)

# Create USD stage and root object
stage = Usd.Stage.CreateNew(usd_file_path)
root_xform = UsdGeom.Xform.Define(stage, '/')

for mesh in pm.ls(type='mesh'):

    # Initialize geometry data
    vertex_positions = []
    face_vertex_counts = []
    face_vertex_indices = []

    # Create a USD Mesh primitive for the mesh object
    usd_mesh = UsdGeom.Mesh.Define(stage, root_xform.GetPath().AppendChild(mesh.getParent().name()))

    # Iterate over the faces/vertices and collect geometry data
    for face in mesh.faces:
        vertex_indexes = face.getVertices()
        face_vertex_counts.append(len(vertex_indexes))
        for vertex_index in vertex_indexes:
            vertex = mesh.vtx[vertex_index]
            vertex_position = vertex.getPosition()
            vertex_positions.append((vertex_position[0], vertex_position[1], vertex_position[2]))
            face_vertex_indices.append(vertex_index)

    # Set the collected attributes for the USD Mesh
    usd_mesh.GetPointsAttr().Set(vertex_positions)
    usd_mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    usd_mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

# Save the USD stage to the file
stage.GetRootLayer().Save()
print(f'>> {usd_file_path}')
