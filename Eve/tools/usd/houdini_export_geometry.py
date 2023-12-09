"""
Export geometry from Houdini geometry context.

Create Python node in Geometry context and connect your geometry to the first input.
Material export will work if you assign material to geometry in SOP context (use principledshader material)
"""

import random
from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf
import hou


def create_usd_material(stage, material_path, material_properties):
    """
    Create a USD material with diffuseColor from Houdini material properties.
    """

    # Get properties
    base_color = Gf.Vec3f(material_properties['basecolorr'],
                          material_properties['basecolorg'],
                          material_properties['basecolorb'])

    # Create a material
    usd_material = UsdShade.Material.Define(stage, material_path)

    # Create a UsdPreviewSurface Shader and set its parameters
    shader = UsdShade.Shader.Define(stage, f'{material_path}/usdPreviewSurface')
    shader.CreateIdAttr('UsdPreviewSurface')

    # Set diffuseColor
    shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(base_color)

    # Connect the shader's surface output to the material's surface output
    surface_output = shader.CreateOutput('surface', Sdf.ValueTypeNames.Token)
    usd_material_output = usd_material.CreateSurfaceOutput()
    usd_material_output.ConnectToSource(surface_output)

    return usd_material


def get_material_properties(material):
    """
    Extract properties from the Houdini material node.
    """

    properties = {}
    for parameter in material.parms():
        properties[parameter.name()] = parameter.eval()

    return properties


def get_material_path(geometry):
    """
    Get path to assigned material node from geometry object
    """

    if geometry.findPrimAttrib("shop_materialpath"):
        primitive = geometry.prims()[0]
        material_path = primitive.attribValue("shop_materialpath")

        return material_path


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


def export_materials(stage, geometry, mesh):

    # Get assigned material data and create USD material
    material_path = get_material_path(geometry)
    material = hou.node(material_path)
    material_properties = get_material_properties(material)
    usd_material_path = f'/Root/Looks/{material.name()}'
    create_usd_material(stage, usd_material_path, material_properties)

    # Bind material to mesh
    material_prim = stage.GetPrimAtPath(usd_material_path)
    material = UsdShade.Material(material_prim)
    UsdShade.MaterialBindingAPI(mesh).Bind(material)


def export_geometry(stage, geometry, input_node_name):

    # Get Geometry data
    points, normals, face_vertex_counts, face_vertex_indices = get_geometry_data(geometry)
    # print(f'{points}, {normals}, {face_vertex_counts}, {face_vertex_indices}')

    # Create a USD Mesh primitive and set properties
    mesh = UsdGeom.Mesh.Define(stage, f'/Root/Geometry/{input_node_name}')
    setup_mesh(mesh, points, normals, face_vertex_counts, face_vertex_indices)

    return mesh


def export_usd():
    """
    Create and save a USD file with geometry and normals from the first input.
    """

    # Create a new USD stage
    usd_file_path = f'E:/houdini_export_{random.randint(1, 100)}.usda'
    stage = Usd.Stage.CreateNew(usd_file_path)

    # Access the input geometry
    node = hou.pwd()
    geometry = node.geometry()
    input_node_name = node.inputs()[0].name()

    # Geometry
    mesh = export_geometry(stage, geometry, input_node_name)

    # Materials
    export_materials(stage, geometry, mesh)

    # Save the stage
    stage.GetRootLayer().Save()
    print(f'>> {usd_file_path}')


export_usd()
