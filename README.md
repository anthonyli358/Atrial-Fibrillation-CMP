# Atrial-Fibrillation-CMP

A computational MSci Physics project at Imperial College London using the Christensen-Manani-Peters (CMP) model to investigate atrial fibrillation (AF). 
 
## Authors 
Andrew Ford - andrewjford@hotmail.co.uk  
Anthony Li - anthonyli358@gmail.com   

## Getting Started
### Modules:
- config.py: A basic configuration module for changing the initialisation parameters of the model and viewer.
- model.py: A 3D implementation of the CMP model.
- QT.py: Animate the model in real time using the PyQt GUI.

For the purpose of simply running the 3D CMP model other modules may be disregarded for now.

### Running the Model:
- Open config.py and define the model initialisation parameters:
  - The *structure* dictionary is used to define the CMP model structure parameters. Change the seed from "None" to the seed for a known structure to reproduce the same behaviour.
  - The *sim* dictionary is used to set the activation period of the sinoatrial node. The runtime does not need to be set for real-time simulations.
  - The *QTviewer" dictionary sets the x, y, z positions at which cross-sections are taken and displayed.
  - The *viewer* dictionary is not needed for real-time simulations.
  
- Run QT.py 
  - Changes plotting design may be made in the *Animation* class.

- The z=0 and z=24 surfaces with cross sections indicated by cyan dotted lines are displayed alongside the current seed and timestep.
  - ![alt text](Icons/icons8-play-50.png) ![alt text](Icons/icons8-pause-50.png) Play/Pause animation.
  - ![alt text](Icons/icons8-heat-map-50.png) Plot phase spaces for AF risk (may be intensive & time-consuming).
  - ![alt text](Icons/icons8-settings.png) Settings - change structure parameters, animation style, and cross-section position.
  - ![alt text](Icons/icons8-reset.png) Reset the animation to time=0.
  - ![alt text](Icons/icons8-advance.png) Advance a timestep (time+=1) if animation is paused.

## Development 
### Other Modules:
**Runnable:**
- main.py: Run the 3D CMP model and use the model_recorder module to export the activation array at each time step (HDF5 format). A copy of config.py is also produced for reference.
- main_viewer.py: Import data (HDF5 format) and use method modules to view and analyse data.

**Methods:**
- analysis.py: Circuit tracing and quantification.
- direction.py: Get a random direction.
- ecg.py: An electrocardiogram (ECG) implementation as defined in the structure of the CMP model.
- model_recorder: Save model data (HDF5 format) for analysis.
- utility_methods.py: Generic methods.
- viewer.py: Plot saved model data (HDF5 format).

The data_analysis folder contains some basic initial data for the risk of AF occurring in the model, and the python modules used to plot this.

### Branch naming convention: 
- feat: Feature being added or expanded  
- bug: Bug fix   
- junk: Throwaway branch created for experimenting   
- *(any other commits; such as style changes, documentation, and minor text fixes, can be pushed straight onto the dev branch)* 
 
Once each branch is completed, merge it to the dev branch. Make sure the dev branch still works. Merge the dev branch to the master branch at meaningful checkpoints.
