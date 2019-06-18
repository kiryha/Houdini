# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)

### Introduction
This repository is a Houdini Pipeline Toolkit named "EVE", currently at the early stages of developing. 
The goal is to create **out of the box VFX pipeline** for **Houdini** and **Nuke** applications under control of Shotgun project management system
for a single artist or animation studio. It is full CG oriented pipeline which can handle small tasks with just a few shots as well as huge projects like animation feature or TV series.

The pipeline would be heavily rely on [Animation DNA](https://github.com/kiryha/AnimationDNA/wiki) structure and ideas.

This repository is a draft pipeline version. If you want to use Eve for your projects, go to the [new Eve repo](https://github.com/kiryha/Eve) and follow instructions. 

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
Working [tools](https://github.com/kiryha/Houdini/wiki/tools):  
- **Create project**: Build a folder structure for the new project with pipeline data and tools
- **Save next version**: Incremental save current scene
- **Create scene**: Build a render scene with all necessary components (environment, caches, materials etc)
- **Create flipbook**: Make a hardware render of shot camera and place it to a proper location with version control
- **Reder Farm**: Render set of HIP files
