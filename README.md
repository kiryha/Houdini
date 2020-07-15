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
Clone this repository to a local drive and run **Project Manager** tool with `project_manager.bat`. 
Select directory to hold the new project under 
`Eve` control, enter project name and press "Create New Project" button to build a folder structure with necessary data.

Create assets and shots in database with **Project Manager** tool and you ar ready to produce the CGI magic with Houdini!

Project Manager is a system which controls your pipeline data. It serves to replicate basic Shotgun functionality. 

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


### Features:
#### Supported OS: 
Windows  

#### Project Manager tool

Here you can create projects with assets and shots, launch Houdini in a project context.

[![](https://live.staticflickr.com/65535/50114534717_510ee4905c_o.png)](https://live.staticflickr.com/65535/50114534717_510ee4905c_o.png)
 
#### File paths management system for all Eve files  
This module can create or read string file paths for any possible Eve file types.  
E.g. `D:/PROJECTS/Inception/PROD/3D/scenes/SHOTS/RENDER/cafe/destruction/destruction_001.hip` 

You need to have Python 2.7 with PySide2 in C:/Python27.  
[Get Python with PySide2](https://drive.google.com/open?id=1jC4x2-Dcf5saixe9Z5aBu-kIMMaGEmtJ)

### Learning database
Attempt to make first steps with Houdini, Programming or Math? In addition to `Eve` specific materials, we have plenty of Houdini tutorials! 

The best places to start with VEX and Python:
- [VEX for artists](https://github.com/kiryha/Houdini/wiki/vex-for-artists)  
- [Python for artists](https://github.com/kiryha/Houdini/wiki//python-for-artists)

Don't miss [Programming basics](https://github.com/kiryha/Houdini/wiki//programming-basics) if you don't have programming experience!

Applied Python in Houdini: [Python snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)  
Applied VEX: [VEX snippets](https://github.com/kiryha/Houdini/wiki//vex-snippets)   
Small solutions as a HIP files: [HIP Examples](https://github.com/kiryha/Houdini/wiki//examples)

### Release structure for Eve:  
  
 - Eve (root pipeline folder)  
    - project_manager.bat  
    - data (database file)  
    - tools (pipeline tools)  
        - core (common modules)  
        - houdini (houdini tools)  
        - nuke (nuke tools)  
        - pm (Project Manager)  
              
              
Download release, extract to the temp folder, copy Eve folder from Eve-0.0 to the network drive.

### History
"Eve" is an evolution of my VFX pipeline [Animation DNA](https://github.com/kiryha/AnimationDNA/wiki) used to 
create our [first Ukrainian 3D Animation film](https://www.imdb.com/title/tt5954304/). The core logic remains the same, 
I just switch from Maya to Houdini. The developing was done during personal project creation, [The Beauty](https://vimeo.com/343421950) music video:

[![](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)

After finishing "The Beauty" Eve were restructured so the Project manager tool now drives all projects and Eve settings.