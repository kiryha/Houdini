"""
Export geometry from Maya scene to USD file
"""

import random
from pxr import Usd, UsdGeom
import pymel.core as pm


def get_geometry_data(mesh):
    """
    Get mesh geometry data
    """

    points = []  # World position coordinates (tuples) for each geometry point (point3f[] points)
    face_vertex_counts = []  # Number of vertices in each geometry face (int[] faceVertexCounts)
    face_vertex_indices = []  # List of geometry vertex indexes (int[] faceVertexIndices)

    # Get vertex data for each face
    vertex_index = 0
    for face in mesh.faces:
        vertex_indexes = []
        for vertex in face.getVertices():
            position = tuple(mesh.vtx[vertex].getPosition(space='world'))
            points.append(position)
            vertex_indexes.append(vertex_index)
            vertex_index += 1

        face_vertex_counts.append(len(vertex_indexes))
        face_vertex_indices.extend(vertex_indexes)

    return points, face_vertex_counts, face_vertex_indices


def process_geometry(stage, root_xform):
    """
    Iterate over all scene meshes and record them to the USD stage
    """

    for mesh in pm.ls(type='mesh'):

        # Get geometry data
        points, face_vertex_counts, face_vertex_indices = get_geometry_data(mesh)

        # Create USD Mesh and record mesh data
        usd_mesh = UsdGeom.Mesh.Define(stage, root_xform.GetPath().AppendChild(mesh.getParent().name()))
        usd_mesh.GetPointsAttr().Set(points)
        usd_mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
        usd_mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)


def export_geometry():
    """
    Create USD file and record geometry data
    """

    # Create USD stage
    usd_file_path = f'D:/maya_geometry_{random.randint(1, 1000)}.usda'

    # Create USD stage and root object
    stage = Usd.Stage.CreateNew(usd_file_path)
    root_xform = UsdGeom.Xform.Define(stage, '/')

    process_geometry(stage, root_xform)

    # Save the USD stage to the file
    stage.GetRootLayer().Save()
    print(f'>> {usd_file_path}')


export_geometry()
