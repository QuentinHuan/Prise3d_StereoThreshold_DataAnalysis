"""
@author: Quentin Huan

collection of various function used to display results, compute thresholds, and reconstruct images
"""
import processData_lib as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from scipy.interpolate import NearestNDInterpolator
import os

# return a list of the perceptive thresholds (refers to the image ID)
# threshold_spp = 20*threshold[ID]
def compute_thresholds(resultFilePath,finalEstimation="",fullParam=False):
    T=[]
    dataX=[]
    dataY=[]
    result=pd.sortDataToXY(resultFilePath)
    sceneName=resultFilePath.replace("data/","").replace("_results.log","")
    print("compute_thresholds for : " + sceneName)
    print()
    print("number of observations per blocks :")
    print("[",end='')
    for i in range(16):
        print(str(len(result[i][0])),end=', ')
    print("]")
    print()
    for i in range(16):
        dataX = np.asarray(result[i][0],dtype=np.float32)
        dataY = np.asarray(result[i][1],dtype=np.float32)
        #logistic curve fitting
        params = pd.fit_logisticFunction_MLE(dataX,dataY)
        
        # compute maximum value perceived
        perceived=[]
        for r in range(len(dataX)):
            
            if(dataY[r]==1):
                perceived.append(dataX[r])
            if(len(perceived)>0):
                maxPerceived = int(max(perceived))
            else:
                maxPerceived = 1

        if(finalEstimation=="MP"):
            #MP reconstruction threshold finder
            params = [params[0],max(pd.reconstruct_MP(dataX,dataY),maxPerceived)]
        if(finalEstimation=="99perc"):
            tol=0.999
            spp_99perc=int(params[1]-(1/(params[0]+1e-5))*np.log((1-tol)/tol))
            #MP reconstruction threshold finder
            params = [params[0],max(spp_99perc,maxPerceived)]
        if (fullParam==True):
            T.append((params[0],max([int(params[1]),maxPerceived])))
        else:
            T.append(max([int(params[1]),1]))
    return T
    
# show the logistic plots and threshold values
def showResult(Threshold,resultFilePath,finalEstimation=False,method=""):
    T = Threshold

    result=pd.sortDataToXY(resultFilePath)
    fig, axes = plt.subplots(4,4, sharex=True, sharey=True)
    # fig.suptitle(resultFilePath.replace("data/","").replace("_results.log","")+" --MP="+str(int(finalEstimation)), fontsize=16)
    for i in range(4):
        for j in range(4):
            dataX = np.asarray(result[4*i + j][0],dtype=np.float32)
            dataY = np.asarray(result[4*i + j][1],dtype=np.float32)
            params = T[4*i + j]

            #logistic curve plot
            X = np.linspace(-1,501,503)
            tol=0.5
            if(method=="99perc"):
                tol=1-0.99
            else:
                tol=0.5
            
            #data points plot
            axes[i,j].set_ylim([0,1.05])
            axes[i,j].plot(dataX,dataY,"kx")
            
            thresLine = params[1]+(1/params[0])*np.log((1-tol)/tol)
            Y = pd.logistic(X,params[0],params[1])

            axes[i,j].plot(X,Y,"r",linewidth=1)
            axes[i,j].axvline(thresLine,ls="--",color="g",ymin=0,ymax=1,linewidth=0.5)
            axes[i,j].plot(thresLine,tol,"g.")
            axes[i,j].set_xlabel("seuil("+str(4*i+j)+")="+str(20*int(np.round(params[1])+1))) 


    plt.setp(axes[:, 0], ylabel='P_detection(spp)')


# generate an image made of all the threshold images
# bStereo = True to generate the stereo pair
def show_thresholdImage(resultFilePath,imgDataBasePath,bStereo,finalEstimation=False,side="right"):
    T = compute_thresholds(resultFilePath,finalEstimation)
    print("----------------------------")
    print("show_thresholdImage for "+resultFilePath)
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
    if(bStereo==True):
        imgOut=Image.new('RGB', (800*2, 800))
    else:
        imgOut=Image.new('RGB', (800, 800))
        
    for j in range(4):
        for i in range(4):
            im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i + 4*j]).zfill(5) +".png")
            region_l = im_l.crop((i*200, j*200, (i+1)*200, (j+1)*200))

            imgOut.paste(region_l,(i*200, j*200))
            
            if(bStereo==True):
                side="left"
                im_r = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i + 4*j]).zfill(5) +".png")
                region_r = im_r.crop((i*200, j*200, (i+1)*200, (j+1)*200))
    
                imgOut.paste(region_r,(i*200+800, j*200))

    saveDir = "./img/p3d_"+sceneName+"-"+side
    if(not os.path.isdir(saveDir)):
        os.mkdir(saveDir)
    output=saveDir+"/p3d_"+sceneName+"-"+side+"_00001.png"
    imgOut.save(output)
    print("image saved to: "+output)

# generate the reconstructed images (8pov)
def show_thresholdImage_8pov(resultFilePath,imgDataBasePath,bStereo,finalEstimation=False):
    T = compute_thresholds(resultFilePath,finalEstimation)
    suffix="MLE"
    if finalEstimation==True:
        suffix=suffix+"_MP"
    print("----------------------------")
    print("show_thresholdImage for "+resultFilePath)
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
   
    for r in range(1,9):
        side = str(r)
        imgOut=Image.new('RGB', (360, 360))
        saveDir = "./img/p3d_"+sceneName+"-0"+side

        if(not os.path.isdir(saveDir)):
            os.mkdir(saveDir)

        for j in range(4):
            for i in range(4):
                im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-0"+side+"/p3d_"+sceneName+"-0"+side+"_"+  str(T[i + 4*j]).zfill(5) +".png")
                region_l = im_l.crop((i*90, j*90, (i+1)*90, (j+1)*90))
                imgOut.paste(region_l,(i*90, j*90))
        
        imgOut.save(saveDir+"/p3d_"+sceneName+"-0"+side+"_"+  str(1).zfill(5) +".png")
        print(str(r) + "/8")
    print("image saved to: "+"./img/Thresh_"+sceneName+suffix+".png")
        
# generate the reconstructed images (8pov) : smooth transitions between blocks
# resX and resY resoltuition of the image in pixels
# side = "1"/"2"/.../"8" for 8pov or "left"/"right" for stereo 
def reconstruct_thresholdImage(Threshold,resultFilePath,imgDataBasePath,resX,resY,side,method="nearest",show=False,saveDir=""):
    # threshold computation
    T = Threshold
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
    SPP_Interp = np.zeros((resX,resY))

    SPP = []
    for j in range(4):
        for i in range(4):
            SPP.append(T[i + 4*j])
    SPP = np.asarray(SPP)
    SPP = np.reshape(SPP,(16,))

    # interpolate SPP level
    if(method=="nearest"):
        x=np.asarray([0,1,2,3])
        y=x
        g = np.meshgrid(x,y)
        g=np.append(g[0].reshape(-1,1),g[1].reshape(-1,1),axis=1)
        g=np.reshape(g,(16,2))
        f=NearestNDInterpolator(g, SPP)
        xx,yy=np.meshgrid(np.linspace(-0.5,3.5,resX),np.linspace(-0.5,3.5,resY))
        img=np.transpose(f(xx,yy))
    else:
        f=interp2d([0,1,2,3],[0,1,2,3],SPP,kind=method)
        img=f(np.linspace(-0.5,3.5,resX),np.linspace(-0.5,3.5,resY))

    SPP_Interp=np.asarray(img,dtype=np.uint32)
    SPP_Interp=np.clip(SPP_Interp,1,500)
    #Image.fromarray(SPP_Interp).show() # debug
    valueList=np.unique(SPP_Interp)
    imgOut=Image.new('RGB', (resX, resY))
    # for each spp values : load spp image and copy corresponding pixel on final image
    for i in valueList:
        if(side == "right" or side == "left"):#stereo threshold images
            im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(i).zfill(5) +".png")
        else:
            if(side==""): #2d threshold images
                im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"/p3d_"+sceneName+"_"+  str(i).zfill(5) +".png")
            else: #8pov threshold images
                im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-0"+side+"/p3d_"+sceneName+"-0"+side+"_"+  str(i).zfill(5) +".png")
        result = np.where(SPP_Interp == i)
        #print(result)
        for r in range(0,len(result[0])):
            coord = (int(result[0][r]),int(result[1][r]))
            pixel=im_l.getpixel(coord)
            imgOut.putpixel(coord,pixel)

    #imgOut=Image.fromarray(SPP_Interp)
    if(show):
        imgOut.show()
    else:
        savePathDir = "./img/"+saveDir+"/p3d_"+sceneName
        if(side == "right" or side == "left"):
            savePathDir = savePathDir+"-"+side
            output=savePathDir+"/p3d_"+sceneName+"-"+side+"_00001.png"
        else:
            if(side==""): #2d threshold images
                savePathDir = savePathDir
                output=savePathDir+"/p3d_"+sceneName+"_00001.png"
            else:
                savePathDir = savePathDir+"-0"+side
                output=savePathDir+"/p3d_"+sceneName+"-0"+side+"_00001.png"
        if(not os.path.isdir(savePathDir)):
            os.mkdir(savePathDir)
        imgOut.save(output)
        print("reconstructed -"+ side + "- image saved to: "+output)
