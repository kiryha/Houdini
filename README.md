# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)

### Introduction
"Eve" is an **out of the box VFX pipeline** for Houdini application. It is a full CG oriented pipeline which can 
handle small tasks with just a few shots as well as huge projects like animation feature or TV series. Eve does not 
provide any particular solutions for any of CG techniques like modeling, rendering etc, its just allows to structure all 
necessary data storage and exchange. In other words, Eve is an abstract data management tool for your Houdini projects.

No matter how you would create your model, Eve will provide tools to save the scene, share results for the next 
pipeline steps, version and publish files.


The pipeline would be heavily rely on [Animation DNA](https://github.com/kiryha/AnimationDNA/wiki) structure and ideas.

### How to install and use
Clone this repository to a local drive and run **createProject.bat**. Select directory to hold the new project under 
`Eve` control, enter project name and press "CREATE PROJECT" to build a folder structure with necessary data.

Check [Eve tutorials](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials) for more details.

### Learning database
In addition to Eve specific materials there are plenty of Houdini tutorials. Check [Eve wiki](https://github.com/kiryha/Houdini/wiki)!

### Requirements
Windows, Python 2.7, PySide

### Current state
Supported OS: Windows  
Working [Tools](https://github.com/kiryha/Houdini/wiki/tools):  
- **Create project**: Build a folder structure for the new project with pipeline data and tools
- **Save next version**: Incremental save current scene
- **Project Manager**: "Shotgun" for free, assets and shots management tool.
- **Create flipbook**: Make a hardware render of shot camera and place it to a proper location with version control
- **Render Farm**: Render set of HIP files
