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

stage = Usd.Stage.CreateNew('C:/Users/kko8/OneDrive/projects/houdini_snippets/PROD/3D/caches/ASSETS/python.usda')

# Build mesh object
root_xform = UsdGeom.Xform.Define(stage, '/Root')
mesh_path = Sdf.Path(root_xform.GetPath()).AppendChild('super_plane')
mesh = UsdGeom.Mesh.Define(stage, mesh_path)

# Build mesh geometry
plane_data = procedurals.plane(1, 1)
mesh.GetPointsAttr().Set(plane_data['points'])
mesh.GetFaceVertexCountsAttr().Set(plane_data['face_vertex_counts'])
mesh.GetFaceVertexIndicesAttr().Set(plane_data['face_vertex_indices'])


# Set orientation and subdivisionScheme
mesh.CreateOrientationAttr().Set(UsdGeom.Tokens.leftHanded)
mesh.CreateSubdivisionSchemeAttr().Set("none")

stage.GetRootLayer().Save()
