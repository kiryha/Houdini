# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)

### Introduction
"Eve" is an **out of the box VFX pipeline** for Houdini application on Windows OS. It is a full CG oriented pipeline which can 
handle small tasks with just a few shots as well as huge projects like animation feature or TV series. Eve does not 
provide any particular solutions for any of CG techniques like modeling, rendering etc, its just allows to structure all 
necessary data storage and exchange. In other words, Eve is an **abstract data management tool** for your Houdini projects.

No matter how you would create your model, Eve will provide [tools](https://github.com/kiryha/Houdini/wiki/tools)
 to save the scene, share results for the next pipeline steps, version and publish working files.

### How to use Eve
[Install necessary components](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials#installation). 
Clone this repository to a local drive and run **Project Creator** tool with `createProject.bat`. Select directory to hold the new project under 
`Eve` control, enter project name and press "Create New Project" button to build a folder structure with necessary data.

Create assets and shots in database with **Project Manager** tool and you ar ready to produce the CGI magic with Houdini!
[![](https://live.staticflickr.com/65535/48056687948_124c55d2fe_o.gif)](https://live.staticflickr.com/65535/48056687948_124c55d2fe_o.gif)

Check [Eve tutorials](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials) for quick start.

### Learning database
Attempt to make first steps with Houdini, Programming or Math? In addition to `Eve` specific materials, we have plenty of Houdini tutorials! 

The best places to start with VEX and Python:
- [VEX for artists](https://github.com/kiryha/Houdini/wiki/vex-for-artists) 
- [Python for artists](https://github.com/kiryha/Houdini/wiki//python-for-artists)

Don't miss [Programming basics](https://github.com/kiryha/Houdini/wiki//programming-basics) if you don't have programming experience!

Applied Python in Houdini: [Python snippets](https://github.com/kiryha/Houdini/wiki/python-snippets) 
Applied VEX: [VEX snippets](https://github.com/kiryha/Houdini/wiki//vex-snippets)  
Small solutions as a HIP files: [HIP Examples](https://github.com/kiryha/Houdini/wiki//examples)

### Current state
Supported OS: Windows  

Working [Tools](https://github.com/kiryha/Houdini/wiki/tools):  
- **Create project**: Build a folder structure for the new project with pipeline data and tools
- **Save next version**: Incremental save current scene
- **Project Manager**: "Shotgun" for free, assets and shots management tool.
- **Create flipbook**: Make a hardware render of shot camera and place it to a proper location with version control
- **Render Farm**: Render list of HIP files

[![](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)
