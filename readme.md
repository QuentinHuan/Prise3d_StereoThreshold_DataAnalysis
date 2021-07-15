Python scripts for processing captured by [P3D_StereoThreshold](https://github.com/QuentinHuan/Prise3D_StereoThreshold) and [P3D_StereoThreshold_Alioscopy](https://github.com/QuentinHuan/Prise3d_StereoThreshold_Alioscopy) experiments.

# description:

main scripts:
* ```main.py```: interface to extract the data from .log Ue4 files and compute the perceptive thresholds
* ```process_log.py```: module that extracts data form .log Ue4 files
* ```process_data.py```: module that computes thresholds
* ```MLE_stimulus.py```: module for MLE procedure (interface and performance tests)
* ```Output.py```: module for plots, visualisation of the results, and image reconstruction

unreal bindings:
* ```ExperimentAnalysis.py```: analyse .log files and save the results (used by UE4 project)
* ```ComputeNewStimulusSet.py```: use saved results to compute new stimulus values (used by UE4 project)

alioscopy binding:
* ```ExperimentAnalysis_Alioscopy.py```: analyse .log files and save the results (used by Alioscopy project)

install scripts:
* ```get-pip.py```: install pip on computer
* ```install.sh```: bash script to install all the dependencies

# How to add to the P3D_StereoThreshold Unreal project:

* package the project from the editor
* add the ```script``` folder into ```packProjectFolder\WindowsNoEditor\P3d_Expe1\Content\script\```
* copy the result files you want to use

# Check if everything is working as expected:

* run ```python /pathToScript/ComputeNewStimulusSet.py p3d_contemporary-bathroom``` (or some other scene present in ```/pathToScript/data```).
script should print something of the sort: ```177,267,216,77,77,254,77,206,259,293,245,77,234,247,77,77```

if the script run into an error, it's probably because some dependencies are not met:
* open a terminal window
* check if python 3 is installed: ```python --version``` (if not, please install and add to PATH)
* check if pip is installed: ```python``` (if not, run ```python /pathToScript/get-pip.py```)
* run ```bash /pathToScript/install.sh``` to install all  the dependencies (numpy, scipy, matplotlib,pillow)

# How to add to the P3D_StereoThreshold_Alioscopy project:
Prise3d_StereoThreshold_DataAnalysis* is already packaged in the repo as a submodule. Everything is working out of the box.
* just replace the result files (backups in ```./data/backups/``` ) if you want to use an existing set ```./data```
