# Eve: 3D animation Houdini pipeline

## Introduction
"Eve" is an **out of the box VFX pipeline** for Houdini application. It is a full CG oriented pipeline which can 
handle small tasks with just a few shots as well as huge projects like animation feature or TV series. Eve does not 
provide any particular solutions for any of CG techniques like modeling, rendering etc, its just allows to structure all 
necessary data storage and exchange. In other words, Eve is an abstract data management tool for your Houdini projects.

No matter how you would create your model, Eve will provide tools to save the scene, share results for the next 
pipeline steps, version and publish files.

This repository is a clean version of early created [Houdini](https://github.com/kiryha/Houdini) pipeline. 

#### Documentation
Refer to [Eve wiki](https://github.com/kiryha/Houdini/wiki) for more info about pipeline usage and some fancy tutorials!

## Requirements and Installation
Currently, Eve designed to be run on Windows OS. 
Here is the list of things you need to have before Eve pipeline will works:

- Houdini 
- Python 2.7.5 x 64 (or later version) 
- PySide (may require `pip` to be installed) 
- GitHub Desktop 


## Usage
Clone Eve repository to your local drive with GitHub Desktop (alternatively you can just download repo as a zip file and 
extract to desired location). Go to Eve folder on your HDD and run Project Creator tool with `projectCreator.bat` file.

[![](https://live.staticflickr.com/65535/48019770601_10f9642217_o.gif)](https://live.staticflickr.com/65535/48019770601_10f9642217_o.gif)

Select location of your project on hard drive, enter project name and Houdini build number and press "Create Project" button.
Go to `<projectLocation>/PREP/PIPELINE/`, run Houdini with `runHoudini.bat` and do your CGI magic! 

You can create a shortcut for the bat file, place it in any convenient location (Desktop, for example) to access all your Eve projects easily. 

Once you have your project in place it`s time to create and manage assets and shots:
[![](https://live.staticflickr.com/65535/48056687948_124c55d2fe_o.gif)](https://live.staticflickr.com/65535/48056687948_124c55d2fe_o.gif)
