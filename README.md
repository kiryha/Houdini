# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)


### Introduction
"Eve" is an **out of the box VFX pipeline** for Houdini application on Windows OS. It is a full CG oriented pipeline which can 
handle small tasks with just a few shots as well as huge projects like animation feature or TV series. Eve does not 
provide any particular solutions for any of CG techniques like modeling, rendering etc, its just allows to structure all 
necessary data storage and exchange. In other words, Eve is an **abstract data management tool** for your Houdini projects.

No matter how you would create your model, Eve will provide [tools](https://github.com/kiryha/Houdini/wiki/tools)
 to save the scene, share results for the next pipeline steps, version and publish working files.

### Learning database
Attempt to make first steps with Houdini, Programming or Math? In addition to `Eve` specific materials, we have plenty of Houdini tutorials! 

The best places to start with VEX and Python:
- [VEX for artists](https://github.com/kiryha/Houdini/wiki/vex-for-artists)  
- [Python for artists](https://github.com/kiryha/Houdini/wiki//python-for-artists)
- [USD for artists](https://github.com/kiryha/Houdini/wiki/pixar-usd-python-api)
- [AI for artists](https://github.com/kiryha/Houdini/wikiai-for-artists)

### How to use Eve
[Install necessary components](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials#installation). 
Clone this repository to a local drive and run **Project Manager** tool with `project_manager.bat`. 
Select directory to hold the new project under 
`Eve` control, enter project name and press "Create New Project" button to build a folder structure with necessary data.

Create assets and shots in database with **Project Manager** tool and you ar ready to produce the CGI magic with Houdini!

Project Manager is a system which controls your pipeline data. It serves to replicate basic Shotgun functionality. 

Check [Eve tutorials](https://github.com/kiryha/Houdini/wiki/pipeline-tutorials) for quick start.

#### Project Manager tool

Here you can create projects with assets and shots, launch Houdini in a project context.

[![](https://live.staticflickr.com/65535/50114534717_510ee4905c_o.png)](https://live.staticflickr.com/65535/50114534717_510ee4905c_o.png)
 

### History
"Eve" is an evolution of my VFX pipeline [Animation DNA](https://github.com/kiryha/AnimationDNA/wiki) used to 
create our [first Ukrainian 3D Animation film](https://www.imdb.com/title/tt5954304/). The core logic remains the same, 
I just switch from Maya to Houdini. The developing was done during personal project creation, [The Beauty](https://vimeo.com/343421950) music video:

[![](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)](https://live.staticflickr.com/65535/48093904051_82f1509e49_o.jpg)

After finishing "The Beauty" Eve were restructured so the Project manager tool now drives all projects and Eve settings.