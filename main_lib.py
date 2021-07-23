# -*- coding: utf-8 -*-
"""
@author: Quentin Huan



"""
import parseLog_lib as pl
import utility as u
import processData_lib as pd
import numpy as np

# process one log files located in logPath, whose name is logName
# ex: E:/logFolder/mylog.log
# logPath = E:/logFolder
# logName = mylog.log
#
# add the results to the dataset in ./data
def process_one_log(logPath,logName):
    
    print("##########################")
    print("  begin data processing   ")
    print("##########################")
    path=logPath

    # ------------------------------------
    # clean all logs file (remove all the irrelevant UE4 system logs)
    # ------------------------------------
    pl.prune_logFile(path,logName)
    
    print("cleaning file done")
    print("")
    path="data"
    
    # list all .log files in ./logs
    logs=u.listFiles(path,["prune_"])
    print(str(len(logs))+" clean .log files detected in "+ path)
    
    # ------------------------------------
    # split log files by scene
    # ------------------------------------
    for f in logs: 
        pl.split_logFile(path,f)
    
    print("split all files by scene done")
    
    # ------------------------------------
    # analyze each files
    # ------------------------------------
    logs=u.listFiles(path,[".log"])
    print(str(len(logs))+" files in "+ path)
    i=0
    for f in logs: 
        if("results" in f):
            print(f+"is result file, skip...")
        else:
            pl.analyze_logFile(path,f)
            i=i+1
            print("file annalysis : "+str(i)+"/"+str(len(logs)))
    
    print("-------------------------")
    print("file annalysis done   ")
    print("-------------------------")
    
    # ------------------------------------
    # get scenelist
    # ------------------------------------
    logs=u.listFiles(path,[".log","_20"])
    sceneList=[]
    for f in logs:
        name = f.split("_20")[0] 
        if name not in sceneList:
            sceneList.append(name)
    
    logs=u.listFiles(path,[".log","results"])
    sceneList=[]
    for f in logs:
        name = f.split("_results")[0] 
        if name not in sceneList:
            sceneList.append(name)
            
    print("detected scenes:")
    print("")
    print(sceneList)
    print("")
    # ------------------------------------
    # merge files by scene
    # ------------------------------------
    logs=u.listFiles(path,[".log","results"])
    pl.merge_logFile(path,sceneList,0)

    logs=u.listFiles(path,[".log","results"])
    for f in logs:
        print("generated: " + f)

# generate next stimulus given dataX and dataY
def next_stimulus_MLE(dataX,dataY):
    # experiment beginning: first stimulus is in sampling space center
    if len(dataX)==0:
        return 25
    else:
        # make sure it's a float32 array
        dataX=np.asarray(dataX,dtype=np.float32)
        dataY=np.asarray(dataY,dtype=np.float32)
        # fit new logistic curve to data
        params = pd.fit_logisticFunction_MLE(dataX,dataY)
        X0_estimated=int(params[1])

        return X0_estimated

