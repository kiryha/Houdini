"""
Pixar USD Python API

Requirements: get compiled Python API: pip install usd-core
"""

from pxr import Usd, UsdGeom, UsdShade

stage = Usd.Stage.CreateNew('E:/output.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
sphere = UsdGeom.Sphere.Define(stage, '/hello/mySphere')
sphere.GetRadiusAttr().Set(2.0)
# material = UsdShade.Material.Define(stage, '/myMaterial')
# shader = UsdShade.Shader.Define(stage, '/myMaterial/myShader')

stage.GetRootLayer().Save()