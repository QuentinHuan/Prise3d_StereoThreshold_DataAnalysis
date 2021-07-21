# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import process_log as pl
import utility as u
import os
import time
import shutil
import errno
import glob
import matplotlib.pyplot as plt
import numpy as np

import process_data as pd
import Output as out

Thresholds={"p3d_arcsphere" : [2733,1640,1560,2533,3693,2166,2506,2833,4866,3766,3273,3173,1766,2013,2913,3213],
"p3d_contemporary-bathroom" : [10000,10000,10000,10000,3086,10000,10000,10000,10000,10000,9013,9073,9666,9040,3060,3293],
"p3d_caustic-view0" : [2313,5306,3953,1760,2106,2166,2026,2820,3620,4906,5173,4426,3560,4033,5160,4966],
"p3d_crown" : [1286,6680,3760,1293,2153,6146,4953,2640,4420,2086,2286,3980,4486,3766,3553,3093],
"p3d_indirect" : [1020,1286,2166,6086,1286,1020,3093,5686,686,1086,2553,3020,420,1486,2086,2753]}

#imagePath="/home/stagiaire/Bureau/image/8pov"
#imagePath="/home/stagiaire/Bureau/image/stereo"
imagePath="E:/image/Stereo"

#path="data/p3d_arcsphere_results.log"
#path="data/p3d_contemporary-bathroom_results.log"
#path="data/p3d_caustic-view0_results.log"
#path="data/p3d_crown_results.log"
#path="data/p3d_indirect_results.log"

sceneList=["p3d_arcsphere","p3d_contemporary-bathroom","p3d_caustic-view0","p3d_crown","p3d_indirect"]
#sceneList=["p3d_kitchen-view0","p3d_kitchen-view1","p3d_landscape-view3","p3d_sanmiguel-view1","p3d_sanmiguel-view2"]
#sceneList=["p3d_caustic-view0"]
c=0
for s in sceneList:
    c=c+1
    print("-----------------------------------")
    print("("+str(c)+"/"+str(len(sceneList))+")")
    path="data/"+s+"_results.log"

    Threshold = out.compute_thresholds(path,finalEstimation=True)
    T=[]
    for i in range(16):
        T.append(Threshold[i][1])
    T=20*np.asarray(T)
    print(s+" threshold : ")
    print(str(T))

    #out.reconstruct_thresholdImage(Threshold,path,imagePath,800,800,"right",method="nearest",show=False)
    #out.reconstruct_thresholdImage(Threshold,path,imagePath,800,800,"left",method="nearest")
    #out.showResult(path,True)

    ## plot all thresholds
    X = np.linspace(0,15,16)
    Y1 = np.asarray(Thresholds.get(sceneList[0]))
    Y2 = np.asarray(T)
    #plt.plot(X,Y1,"r")
    #plt.plot(X,Y2,"b")
    E = np.prod(Y2/Y1)
    print(E)
    plt.plot(Y2,Y1,".")
    plt.xlim([0, 10000])
    plt.ylim([0, 10000])

plt.show()










