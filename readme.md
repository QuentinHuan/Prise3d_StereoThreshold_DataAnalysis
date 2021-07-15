Python scripts for data processing:

# description:

main scripts:
* ```main.py```: interface to extract the data from .log Ue4 files and compute the perceptive thresholds
* ```process_log.py```: module that extracts data form .log Ue4 files
* ```process_data.py```: module that computes thresholds
* ```MLE_stimulus.py```: module for MLE procedure (interface and performance tests)
* ```Output.py```: module for plots and visualisation of the results

unreal bindings:
* ```ExperimentAnalysis.py```: analyse .log files and save the results (used by UE4 project)
* ```ComputeNewStimulusSet.py```: use saved results to compute new stimulus values (used by UE4 project)

install scripts:
* ```get-pip.py```: install pip on computer
* ```install.sh```: bash script to install all the dependencies

# How to add to the unreal project:

* package the project
* add the ```script``` folder into ```packProjectFolder\WindowsNoEditor\P3d_Expe1\Content\script\```

# Check if everything is working as expected:

* run ```python /pathToScript/ComputeNewStimulusSet.py p3d_contemporary-bathroom``` (or some other scene present in ```/pathToScript/data```).
script should print something of the sort: ```177,267,216,77,77,254,77,206,259,293,245,77,234,247,77,77```

if the script run into an error, it's probably because some dependencies are not met:
* open a terminal window
* check if python 3 is installed: ```python --version``` (if not, please install and add to PATH)
* check if pip is installed: ```python``` (if not, run ```python /pathToScript/get-pip.py```)
* run ```bash /pathToScript/install.sh``` to install all  the dependencies (numpy, scipy, matplotlib,pillow)
