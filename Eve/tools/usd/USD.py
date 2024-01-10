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

# mesh_path = Sdf.Path(root_xform.GetPath()).AppendChild('super_plane')
# mesh = UsdGeom.Mesh.Define(stage, mesh_path)
"""

from pxr import Usd, UsdGeom, Sdf, UsdShade
import procedurals


def crate_geometry():
    """
    Procedurally create geometry and save it to the USDA file
    """

    shape = 'super_extrude'
    root_for_export = 'C:/Users/kko8/OneDrive/projects/houdini_snippets/PROD/3D/caches/ASSETS'
    stage = Usd.Stage.CreateNew(f'{root_for_export}/{shape}.usda')

    # Build mesh object
    UsdGeom.Xform.Define(stage, '/Root')
    mesh = UsdGeom.Mesh.Define(stage, f'/Root/{shape}')

    # Build mesh geometry
    # mesh_data = procedurals.plane(6, 6)
    # mesh_data = procedurals.sphere(8, 6)
    # mesh_data = procedurals.torus(8, 12, 1, 0.5)
    # mesh_data = procedurals.cone(12)

    # lot = [(1, 0, -1), (1, 0, 1), (0.6, 0, 1), (0.6, 0, 1.2),
    #        (0.2, 0, 1.2), (0.2, 0, 0.8), (0, 0, 0.8), (0, 0, -0.2), (0.4, 0, -0.2), (0.4, 0, -1)]
    # mesh_data = procedurals.polygon(lot)

    # Extrude Face
    # mesh_data = procedurals.EditMesh(procedurals.polygon()).extrude_face(0, 4)
    mesh_data = procedurals.EditMesh(procedurals.torus(8, 12, 1, 0.5)).extrude_face(5, 0.3)

    mesh.GetPointsAttr().Set(mesh_data.points)
    mesh.GetFaceVertexCountsAttr().Set(mesh_data.face_vertex_counts)
    mesh.GetFaceVertexIndicesAttr().Set(mesh_data.face_vertex_indices)

    # Set orientation and subdivisionScheme
    mesh.CreateOrientationAttr().Set(UsdGeom.Tokens.leftHanded)
    mesh.CreateSubdivisionSchemeAttr().Set("none")

    stage.GetRootLayer().Save()


def build_references():
    """
    Create USD hierarchy:
    "shot.usd" references "asset_a.usd" and "asset_b.usd"
    """

    root_for_export = 'C:/Users/kko8/OneDrive/projects/houdini_snippets/PROD/3D/caches/ASSETS'

    # Asset A
    stage_a = Usd.Stage.CreateNew(f'{root_for_export}/asset_a.usda')
    UsdGeom.Xform.Define(stage_a, '/Root_A')
    UsdGeom.Xform.Define(stage_a, '/Root_A/object_A')
    stage_a.SetDefaultPrim(stage_a.GetPrimAtPath('/Root_A'))  # Set name of the root prim that will be referenced
    stage_a.GetRootLayer().Save()

    # Asset B
    stage_b = Usd.Stage.CreateNew(f'{root_for_export}/asset_b.usda')
    UsdGeom.Xform.Define(stage_b, '/Root_B')
    UsdGeom.Xform.Define(stage_b, '/Root_B/object_B')
    stage_b.SetDefaultPrim(stage_b.GetPrimAtPath('/Root_B'))
    stage_b.GetRootLayer().Save()

    # Shot
    stage = Usd.Stage.CreateNew(f'{root_for_export}/shot.usda')
    UsdGeom.Xform.Define(stage, '/Root_Shot')
    reference_a = stage.OverridePrim('/Root_Shot/reference_a')  # Define "over" prim that will be replaced
    reference_b = stage.OverridePrim('/Root_Shot/reference_b')
    reference_a.GetReferences().AddReference('./asset_a.usda')
    reference_b.GetReferences().AddReference('./asset_b.usda')
    stage.GetRootLayer().Save()


crate_geometry()
# build_references()

