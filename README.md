# Houdini Pipeline Toolkit

### Introduction
This repository is a Houdini Pipeline Toolkit, currently at the early stages of developing. 
The goal is to create **out of the box VFX pipeline** for **Houdini** and **Nuke** applications under control of project management system (Ftrack or Shotgun)
for a single artist or animation studio. It is full CG oriented pipeline which can handle small tasks with just a few shots as well as huge projects like animation feature or TV series.

The pipeline would be heavily rely on [Animation DNA](https://github.com/kiryha/AnimationDNA/wiki) structure and ideas.

### How to use
Download repository as a zip file, extract to any temp location and run **setupProject.bat**. 
Select directory to hold the project, enter project name and press "CREATE PROJECT" to build a project folder structure with a pipeline.

Check [installation tutorial](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials#requirments-and-installation) for more details.

### Learning database
Despite the tools are not ready yet, Houdini learning database is full of useful materials, and it constantly updates.
Example Houdini scenes are located in the **hips** folder.
 
Go and check examples and tutorials in [Houdini pipeline wiki](https://github.com/kiryha/Houdini/wiki)!

### Requirements
Windows, Python 2.7, PySide

### Current state
Supported OS: Windows  
Functionality:  
- Create project folder structure with pipeline scripts and wrapper
