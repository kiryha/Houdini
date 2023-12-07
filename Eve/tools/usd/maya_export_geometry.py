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
    unique_vertex_positions = {}

    # Create a USD Mesh primitive for the mesh object
    usd_mesh = UsdGeom.Mesh.Define(stage, root_xform.GetPath().AppendChild(mesh.getParent().name()))

    # Iterate over the vertices and collect unique positions
    for vertex in mesh.vtx:
        position = tuple(vertex.getPosition(space='world'))
        if position not in unique_vertex_positions:
            unique_vertex_positions[position] = len(unique_vertex_positions)
            vertex_positions.append(position)

    # Iterate over the faces and collect indices
    # Alternative: face_vertex_counts, face_vertex_indices = mesh.getVertices()
    for face in mesh.faces:
        vertex_indexes = [unique_vertex_positions[tuple(mesh.vtx[i].getPosition(space='world'))] for i in
                          face.getVertices()]
        face_vertex_counts.append(len(vertex_indexes))
        face_vertex_indices.extend(vertex_indexes)

    # Set the collected attributes for the USD Mesh
    usd_mesh.GetPointsAttr().Set(vertex_positions)
    usd_mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    usd_mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

# Save the USD stage to the file
stage.GetRootLayer().Save()
print(f'>> {usd_file_path}')