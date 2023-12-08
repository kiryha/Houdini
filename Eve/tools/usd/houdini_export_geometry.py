"""
Export geometry from Houdini geometry context.

Create Python node in Geometry context and connect your geometry to the first input.
"""

import random
from pxr import Usd, UsdGeom, Gf
import hou


def get_geometry_data(geometry):
    """
    Get mesh geometry data
    """

    points = []  # List of point positions (point3f[] points)
    face_vertex_counts = []  # List of vertex count per face (int[] faceVertexCounts)
    face_vertex_indices = []  # List of vertex indices (int[] faceVertexIndices)

    # Collect points
    for point in geometry.points():
        position = point.position()
        points.append(Gf.Vec3f(position[0], position[1], position[2]))

    # Collect face data
    for primitive in geometry.prims():
        vertices = primitive.vertices()
        face_vertex_counts.append(len(vertices))
        face_vertex_indices.extend([vertex.point().number() for vertex in vertices])

    return points, face_vertex_counts, face_vertex_indices


def export_geometry():
    """
    Create and save a USD file with geometry from the first input.
    """

    # Create a new USD stage
    usd_file_path = f'E:/houdini_export_{random.randint(1, 100)}.usda'
    stage = Usd.Stage.CreateNew(usd_file_path)

    # Access the input geometry
    node = hou.pwd()
    geometry = node.geometry()
    input_node = node.inputs()[0]
    input_node_name = input_node.name()

    points, face_vertex_counts, face_vertex_indices = get_geometry_data(geometry)

    # Create a USD Mesh primitive
    mesh = UsdGeom.Mesh.Define(stage, f'/Root/{input_node_name}')
    mesh.GetPointsAttr().Set(points)
    mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

    # Save the stage
    stage.GetRootLayer().Save()
    print(f'>> {usd_file_path}')


export_geometry()
