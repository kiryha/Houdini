"""
Export geometry from Houdini geometry context.

Create Python node in Geometry context and connect your geometry to the first input.
"""

import random
from pxr import Usd, UsdGeom, Gf
import hou


def setup_mesh(mesh, points, normals, face_vertex_counts, face_vertex_indices):
    """
    Setup mesh attributes in USD file
    """

    mesh.GetPointsAttr().Set(points)
    mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
    mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

    if normals:
        mesh.CreateNormalsAttr().Set(normals)
        mesh.SetNormalsInterpolation(UsdGeom.Tokens.faceVarying)

    # Set orientation and subdivisionScheme
    mesh.CreateOrientationAttr().Set(UsdGeom.Tokens.leftHanded)
    mesh.CreateSubdivisionSchemeAttr().Set("none")


def get_geometry_data(geometry):
    """
    Get mesh geometry data including normals
    """

    points = []  # List of point positions (point3f[] points)
    normals = []  # List of normals (normal3f[] normals)
    face_vertex_counts = []  # List of vertex count per face (int[] faceVertexCounts)
    face_vertex_indices = []  # List of vertex indices (int[] faceVertexIndices)

    # Collect points and normals
    for point in geometry.points():
        position = point.position()
        points.append(Gf.Vec3f(position[0], position[1], position[2]))

    # Collect face data
    for primitive in geometry.prims():
        vertices = primitive.vertices()
        face_vertex_counts.append(len(vertices))

        for vertex in vertices:
            face_vertex_indices.append(vertex.point().number())

            # Get Normals data
            if geometry.findVertexAttrib("N") is not None:
                normal = vertex.attribValue("N")
                normals.append(Gf.Vec3f(normal[0], normal[1], normal[2]))

    return points, normals, face_vertex_counts, face_vertex_indices


def export_geometry():
    """
    Create and save a USD file with geometry and normals from the first input.
    """

    # Create a new USD stage
    usd_file_path = f'E:/houdini_export_{random.randint(1, 100)}.usda'
    stage = Usd.Stage.CreateNew(usd_file_path)

    # Access the input geometry
    node = hou.pwd()
    geometry = node.geometry()
    input_node = node.inputs()[0]
    input_node_name = input_node.name()

    # Get Geometry data
    points, normals, face_vertex_counts, face_vertex_indices = get_geometry_data(geometry)

    # Create a USD Mesh primitive and set properties
    mesh = UsdGeom.Mesh.Define(stage, f'/Root/{input_node_name}')
    setup_mesh(mesh, points, normals, face_vertex_counts, face_vertex_indices )

    # Save the stage
    stage.GetRootLayer().Save()
    print(f'>> {usd_file_path}')


export_geometry()
