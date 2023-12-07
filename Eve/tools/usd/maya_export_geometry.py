"""
Export geometry from Maya scene to USD file
"""

import random
from pxr import Usd, UsdGeom
import pymel.core as pm

# Create USD stage
usd_file_path = f'D:/maya_geometry_{random.randint(1, 1000)}.usda'

# Create USD stage and root object
stage = Usd.Stage.CreateNew(usd_file_path)
root_xform = UsdGeom.Xform.Define(stage, '/')

for mesh in pm.ls(type='mesh'):

    # Initialize geometry data
    vertex_positions = []  # point3f[] points
    face_vertex_counts = []  # int[] faceVertexCounts
    face_vertex_indices = []  # int[] faceVertexIndices

    # Create a USD Mesh primitive for the mesh object
    usd_mesh = UsdGeom.Mesh.Define(stage, root_xform.GetPath().AppendChild(mesh.getParent().name()))

    # Iterate over the faces and collect vertices and indices
    vertex_index = 0
    for face in mesh.faces:
        vertex_indexes = []
        for vertex in face.getVertices():
            position = tuple(mesh.vtx[vertex].getPosition(space='world'))

            # Add the vertex position to the list and its index to the face's vertex indexes
            vertex_positions.append(position)
            vertex_indexes.append(vertex_index)
            vertex_index += 1

        face_vertex_counts.append(len(vertex_indexes))
        face_vertex_indices.extend(vertex_indexes)

    # Set the collected attributes for the USD Mesh
    usd_mesh.GetPointsAttr().Set(vertex_positions)
    usd_mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    usd_mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

# Save the USD stage to the file
stage.GetRootLayer().Save()
print(f'>> {usd_file_path}')
