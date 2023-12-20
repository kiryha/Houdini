"""
Pixar USD Python API

Requirements: get compiled Python API: pip install usd-core

Hello World:
# xformPrim = UsdGeom.Xform.Define(stage, '/hello')
# sphere = UsdGeom.Sphere.Define(stage, '/hello/world')
# sphere.GetRadiusAttr().Set(2.0)
# material = UsdShade.Material.Define(stage, '/myMaterial')
# shader = UsdShade.Shader.Define(stage, '/myMaterial/myShader')

# mesh = UsdGeom.Mesh.Define(stage, '/Root/super_plane')
"""

from pxr import Usd, UsdGeom, Sdf, UsdShade
import procedurals


def crate_geometry():
    """
    Procedurally create geometry and save it to the USDA file
    """

    root_for_export = 'C:/Users/kko8/OneDrive/projects/houdini_snippets/PROD/3D/caches/ASSETS'
    stage = Usd.Stage.CreateNew(f'{root_for_export}/super_cone.usda')

    # Build mesh object
    root_xform = UsdGeom.Xform.Define(stage, '/Root')
    mesh_path = Sdf.Path(root_xform.GetPath()).AppendChild('super_plane')
    mesh = UsdGeom.Mesh.Define(stage, mesh_path)

    # Build mesh geometry
    # geometry_data = procedurals.plane(6, 6)
    # geometry_data = procedurals.sphere(8, 6)
    # geometry_data = procedurals.torus(8, 12, 1, 0.5)
    geometry_data = procedurals.cone(12)

    mesh.GetPointsAttr().Set(geometry_data['points'])
    mesh.GetFaceVertexCountsAttr().Set(geometry_data['face_vertex_counts'])
    mesh.GetFaceVertexIndicesAttr().Set(geometry_data['face_vertex_indices'])

    # Set orientation and subdivisionScheme
    mesh.CreateOrientationAttr().Set(UsdGeom.Tokens.leftHanded)
    mesh.CreateSubdivisionSchemeAttr().Set("none")

    stage.GetRootLayer().Save()


crate_geometry()
