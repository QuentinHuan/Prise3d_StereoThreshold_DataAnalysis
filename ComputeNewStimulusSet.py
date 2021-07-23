# -*- coding: utf-8 -*-
"""
@author: Quentin Huan

# arguments:
# in terminal: "python3 ComputeNewStimulusSet.py sceneName"

# description
# print next stimuli values (in [1,500]^16) for scene sceneName
# values are coma separated
# use the results files in ./data to compute the new value 
"""

import main_lib
import processData_lib as pd
import sys
import numpy as np
import os

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
wdir=get_script_path()

sceneName = sys.argv[1]
# results contains dataX and dataY for each block
results = pd.sortDataToXY(wdir+"/data/"+sceneName+"_results.log") # ==> [(dataX_0,dataY_0);...;(dataX_15,dataY_15)]
stimulus=""
# for each image block, compute a new stimulus value
for i in range(16):
    dataX = np.asarray(results[i][0],np.float32)
    dataY = np.asarray(results[i][1],np.float32)
    stimulus=stimulus+str(main_lib.next_stimulus_MLE(dataX,dataY))
    if i!=15: stimulus=stimulus+"," # add coma, exept for last one
print(stimulus)
