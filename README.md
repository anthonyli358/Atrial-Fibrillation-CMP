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
  - The *structure* dictionary is used to define the CMP model structure parameters. Change the seed from *None* to the seed for a known structure to reproduce the same behaviour. The dys_seed parameter can be used to reproduce dysfunctional cell firing behaviour.
  - The *sim* dictionary is used to set the activation period of the sinoatrial node. The runtime does not need to be set for real-time simulations.
  - The *QTviewer* dictionary sets the x, y, z positions at which cross-sections are taken and displayed.
  - The *viewer* dictionary is not needed for real-time simulations.
  
- Run QT.py 
  - Changes plotting design may be made in the *Animation* class.

- The endocardial (z=0) and epicardial (z=24) surfaces with cross sections indicated by cyan dotted lines are displayed alongside the current seed and timestep.
  - ![alt text](Icons/icons8-play-50.png) Play/Pause animation.
  - ![alt text](Icons/icons8-heat-map-50.png) Plot phase spaces for AF risk (may be intensive & time-consuming).
  - ![alt text](Icons/icons8-settings-50.png) Settings - change structure and ablation parameters, animation style, and cross-section position.
  - ![alt text](Icons/icons8-reset-50.png) Reset the animation to time=0.
  - ![alt text](Icons/icons8-advance-50.png) Advance a timestep (time+=1) if animation is paused.
  - ![alt text](Icons/icons8-end-32.png) Skip to first source of AF within 1000 timesteps (skip 1000 timesteps if no source found).
  - ![alt text](Icons/icons8-save-as-50.png) Save animation history to MP4.
  - ![alt text](Icons/icons8-laser-beam-50.png) Ablate from selected cell (radius=2mm by default), lesions are highlighted in red.
 
### Generating and Plotting Data:

Scroll to the bottom under the *if __name__ == '__main__':* statement for:

- risk_curve_data_generator.py: 
    - Loop over nu_x/nu_yz or the nu_av for the angle_vars variable e.g. using np.arange(start, stop, step).
    - The *func* variable must be set to one of the data generation functions in order to run. The options are *risk_curve_data* (risk of inducing AF), *af_time_data* (time in AF), *con_vel_data* (average conduction velocity), or *af_pos_data* (finding the possible AF positions for a given tissue structure).

- risk_curve_data_plotter.py:
    - Comment and uncomment each data specific function as required.
    - The *path* parameter is the folder path for data (*None* if same directory). 
    - Check for each function that the nu_x, nu_yz / nu_av ranges are the same as for data generation and that the *file* variable is of the correct name format for glob patterns using the wildcard character *.

### Initialising Ablated Tissue

The *ablated_tissue* parameter in config.py takes a list of positions (z, y, x) and ablates them upon tissue initialisation with a default radius of 2mm (this may be changed in the __init__() of model.py). It may be extended to ablate tissue of fixed structure where the positions of possible AF sources is known:

- risk_curve_data_generator.py and risk_curve_data_plotter.py: Generate and read af_pos_data().
    - The processed data will be saved in it's original folder in numpy format entitled *af_positions_parameters.npy*.
    - Data structure of [runs x [seed, (z, y, x),etc.]].

- config.py: Make changes outlined by comments in the file itself and in the pseudocode below.

    ```python
    import numpy as np  # required to load the data from file
    af_pos_runs = np.load("af_positions_parameters.npy")  # location of processed data
    for run in af_pos_runs:  # each sublist in the loaded data contains a run with a different tissue structure (seed)
        structure['seed'] = run[0]  # set seed parameter
        structure['ablated_tissue'] = run[1:]  # set ablated_tissue parameter
    ```

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
- risk_curve_data_variable_creator.py: Generate and save a numpy array of nu values bounding the rough region of known risk. Used to run high resolution risk curve data.
- viewer.py: Plot saved model data (HDF5 format).

The data_analysis folder contains some basic initial data for the risk of AF occurring in the model, and the python modules used to plot this.

### Branch naming convention: 
- feat: Feature being added or expanded  
- bug: Bug fix   
- junk: Throwaway branch created for experimenting   
- *(any other commits; such as style changes, documentation, and minor text fixes, can be pushed straight onto the dev branch)* 
 
Once each branch is completed, merge it to the dev branch. Make sure the dev branch still works. Merge the dev branch to the master branch at meaningful checkpoints.
