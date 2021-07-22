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

from scipy.ndimage.filters import gaussian_filter

import process_data as pd
import Output as out

Thresholds={"p3d_arcsphere-view0" : [2733,1640,1560,2533,3693,2166,2506,2833,4866,3766,3273,3173,1766,2013,2913,3213],
"p3d_contemporary-bathroom-view0" : [10000,10000,10000,10000,3086,10000,10000,10000,10000,10000,9013,9073,9666,9040,3060,3293],
"p3d_caustic-view0" : [2313,5306,3953,1760,2106,2166,2026,2820,3620,4906,5173,4426,3560,4033,5160,4966],
"p3d_crown-view0" : [1286,6680,3760,1293,2153,6146,4953,2640,4420,2086,2286,3980,4486,3766,3553,3093],
"p3d_indirect-view0" : [1020,1286,2166,6086,1286,1020,3093,5686,686,1086,2553,3020,420,1486,2086,2753]}

#imagePath="/home/stagiaire/Bureau/image/8pov"
#imagePath="/home/stagiaire/Bureau/image/stereo"
#imagePath="E:/image/Stereo"

#path="data/p3d_arcsphere_results.log"
#path="data/p3d_contemporary-bathroom_results.log"
#path="data/p3d_caustic-view0_results.log"
#path="data/p3d_crown_results.log"
#path="data/p3d_indirect_results.log"

sceneList=["p3d_arcsphere","p3d_contemporary-bathroom","p3d_caustic-view0","p3d_crown","p3d_indirect"]
#sceneList=["p3d_kitchen-view0","p3d_kitchen-view1","p3d_landscape-view3","p3d_sanmiguel-view1","p3d_sanmiguel-view2"]
#sceneList=["p3d_indirect"]

# rebuild Stereo
def rebuild_Stereo():
    c=0
    for s in sceneList:
        c=c+1
        print("-----------------------------------")
        print("("+str(c)+"/"+str(len(sceneList))+")")
        path="data/"+s+"_results.log"

        imagePath="E:/image/stereo"
        for method in ["99perc",""]:#,"MP","99perc"]:
            print("Method = " + method)
            Threshold = out.compute_thresholds(path,finalEstimation=method,fullParam=True)
            T=[]
            Sig=[]
            for i in range(16):
                T.append(Threshold[i][1])
                Sig.append(Threshold[i][0])
            T=np.asarray(T)
            print(s+" threshold : ")
            print(str(20*T))
            print(Sig)
            #out.reconstruct_thresholdImage(T,path,imagePath,800,800,str("right"),method="nearest",show=False,saveDir=method)
            out.showResult(Threshold,path,True,method=method)
            for i in ["right","left"]:
                out.reconstruct_thresholdImage(T,path,imagePath,800,800,str(i),method="nearest",show=False,saveDir=method)
        
        

def rebuild_8pov():
    c=0
    for s in sceneList:
        c=c+1
        print("-----------------------------------")
        print("("+str(c)+"/"+str(len(sceneList))+")")
        path="data/"+s+"_results.log"

        imagePath="/home/stagiaire/Bureau/image/8pov"
        Threshold = out.compute_thresholds(path,finalEstimation=True)
        T=[]
        for i in range(16):
            T.append(Threshold[i])
        T=np.asarray(T)
        print(s+" threshold : ")
        print(str(20*T))

        for i in range(1,9):
            out.reconstruct_thresholdImage(T,path,imagePath,360,360,str(i),method="nearest",show=False)

        # gauss filter SPP to even out
        """ T_gauss = np.reshape(T,(4,4))
        T_gauss=gaussian_filter(T_gauss, sigma=0.5,mode='wrap')
        print(s+" threshold : ")
        T_gauss=T_gauss.reshape((16,))
        print(str(20*T_gauss))

        out.reconstruct_thresholdImage(T,path,imagePath,800,800,"right",method="linear",show=True) """
        #out.reconstruct_thresholdImage(Threshold,path,imagePath,800,800,"left",method="nearest")

def rebuild_2d():
    sceneList=["p3d_arcsphere-view0","p3d_contemporary-bathroom-view0","p3d_caustic-view0","p3d_crown-view0","p3d_indirect-view0"]
    c=0
    for s in sceneList:
        c=c+1
        print("-----------------------------------")
        print("("+str(c)+"/"+str(len(sceneList))+")")
        path="data/"+s+"_results.log"

        imagePath="/home/stagiaire/Bureau/img 2d"
        T=Thresholds.get(s)
        T=np.asarray(T)
        print(s+" threshold : ")
        print(str(T))
        Threshold=[]
        for i in range(16):
            Threshold.append((1,T[i]-(T[i]%20)))

        out.reconstruct_thresholdImage(Threshold,path,imagePath,800,800,"",method="nearest",show=False) 

    """    ## plot all thresholds
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

plt.show() """



#rebuild_8pov()
rebuild_Stereo()
#plt.show()

"""
print("-----------------------------------")
path="data/"+"p3d_indirect"+"_results.log"

def next_stimulus_MLE(dataX,dataY):
    # experiment beginning: first stimulus is in sampling space center
    if len(dataX)==0:
        return 250
    else:
        # make sure it's a float32 array
        dataX=np.asarray(dataX,dtype=np.float32)
        dataY=np.asarray(dataY,dtype=np.float32)
        # fit new logistic curve to data
        params = pd.fit_logisticFunction_MLE(dataX,dataY)
        X0_estimated=int(params[1])

        return X0_estimated

data = pd.sortDataToXY(path)
dataX = np.asarray(data[3][0],dtype=np.float32)
dataY = np.asarray(data[3][1],dtype=np.float32)

i=17
dataX = np.resize(dataX,dataX.size - i)
dataY = np.resize(dataY,dataY.size - i)

print(dataX)
for i in range(40):
    spp = next_stimulus_MLE(dataX,dataY)
    dataX=np.append(dataX,spp)
    if(spp>300):
        dataY=np.append(dataY,0)
    else:
        dataY=np.append(dataY,1)

print(dataX)"""








