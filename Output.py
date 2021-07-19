# output the results of the analysis
# 
#
import process_data as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.interpolate import interp2d
from scipy.interpolate import griddata
import os
import systemd

# return a list of the perceptive thresholds (refers to the image ID)
# threshold_spp = 20*threshold[ID]
def compute_thresholds(resultFilePath,finalEstimation=False):
    T=[]
    dataX=[]
    dataY=[]
    result=pd.sortDataToXY(resultFilePath)
    print("number of observations per blocks :"+str(len(result[1][0])))
    print("compute_thresholds for :" + resultFilePath)
    for i in range(16):
        dataX = np.asarray(result[i][0],dtype=np.float32)
        dataY = np.asarray(result[i][1],dtype=np.float32)
        #logistic curve fitting
        params = pd.fit_logisticFunction_MLE(dataX,dataY)
        
        if(finalEstimation==True):
            #MP reconstruction threshold finder
            params = [1,max(pd.reconstruct_MP(dataX,dataY),params[1])]


        #print("cell "+str(i)+":")
        #print("parameters = ")
        
        T.append((params[0],max([int(params[1]),1])))
    print(T)
    return T
    
# show the logistic plots and threshold values
def showResult(resultFilePath,finalEstimation=False):
    print("----------------------------")
    print("showResult :"+resultFilePath)
    T = compute_thresholds(resultFilePath,finalEstimation)

    result=pd.sortDataToXY(resultFilePath)
    fig, axes = plt.subplots(4,4, sharex=True, sharey=True)
    fig.suptitle(resultFilePath.replace("data/","").replace("_results.log","")+" --MP="+str(int(finalEstimation)), fontsize=16)
    for i in range(4):
        for j in range(4):
            dataX = np.asarray(result[4*i + j][0],dtype=np.float32)
            dataY = np.asarray(result[4*i + j][1],dtype=np.float32)
            params = T[4*i + j]

            #logistic curve plot
            X = np.linspace(1,501,501)
            Y = pd.logistic(X,params[0],params[1])
            axes[i,j].plot(X,Y,"k",linewidth=1)
            axes[i,j].plot(params[1],0.5,"rx")
            axes[i,j].axvline(params[1],ls="--",color="r",ymin=0,ymax=0.5,linewidth=0.5)
            axes[i,j].set_xlabel("seuil("+str(4*i+j)+")="+str(20*int(np.round(params[1])+1))) 

            #data points plot
            axes[i,j].set_ylim([0,1.05])
            axes[i,j].plot(dataX,dataY,"bx")

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
            im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i + 4*j][1]).zfill(5) +".png")
            region_l = im_l.crop((i*200, j*200, (i+1)*200, (j+1)*200))

            imgOut.paste(region_l,(i*200, j*200))
            
            if(bStereo==True):
                side="left"
                im_r = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i + 4*j][1]).zfill(5) +".png")
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
                im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-0"+side+"/p3d_"+sceneName+"-0"+side+"_"+  str(T[i + 4*j][1]).zfill(5) +".png")
                region_l = im_l.crop((i*90, j*90, (i+1)*90, (j+1)*90))
                imgOut.paste(region_l,(i*90, j*90))
        
        imgOut.save(saveDir+"/p3d_"+sceneName+"-0"+side+"_"+  str(1).zfill(5) +".png")
        print(str(r) + "/8")
    print("image saved to: "+"./img/Thresh_"+sceneName+suffix+".png")

def getSPP(SPP,i,j):
    return SPP[int(np.clip(i,0,3)),int(np.clip(j,0,3))]
        

# generate the reconstructed images (8pov)
def show_thresholdImage_8pov_smooth(resultFilePath,imgDataBasePath,bStereo,finalEstimation=False):
    resX=360
    resY=360


    T = compute_thresholds(resultFilePath,finalEstimation)
    suffix="MLE"
    if finalEstimation==True:
        suffix=suffix+"_MP"
    print("----------------------------")
    print("show_thresholdImage for "+resultFilePath)
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
   
    imgOut=Image.new('RGB', (360, 360))
    SPP_Interp = np.zeros((resX,resY))

    SPP = []
    for j in range(4):
        for i in range(4):
            SPP.append(T[i + 4*j][1])
    SPP = np.asarray(SPP)
    #SPP=np.reshape(SPP,(4,4))
    print("SPP")
    print(SPP)
    print(SPP.shape)


    eval = lambda x,y : SPP[x][y]

    N=360
    values = []
    f=interp2d([0,1,2,3],[0,1,2,3],SPP,kind='linear')
    img=f(np.linspace(-0.5,3.5,N),np.linspace(-0.5,3.5,N))

    #img=(f)
    SPP_Interp=np.asarray(img,dtype=np.uint32)
    SPP_Interp=np.clip(SPP_Interp,1,500)

    """ side = "1"
    for i in range(0,resX):
        print(str(i)+ "/"+str(resX))
        for j in range(0,resX):
                im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-0"+side+"/p3d_"+sceneName+"-0"+side+"_"+  str(SPP_Interp[i,j]).zfill(5) +".png")
                #region_l = im_l.crop((i, j, i+1, j+1))
                #imgOut.paste(region_l,(i, j))
                pixel=im_l.getpixel((i,j))
                imgOut.putpixel((i,j),pixel) """

    valueList=np.unique(SPP_Interp)
    side = "1"
    c=0
    for i in valueList:
        c=c+1
        print(str(c)+ "/" + str(len(valueList)))
        im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-0"+side+"/p3d_"+sceneName+"-0"+side+"_"+  str(i).zfill(5) +".png")

        result = np.where(SPP_Interp == i)
        for r in range(0,len(result[0])):
            coord = (int(result[0][r]),int(result[1][r]))
            pixel=im_l.getpixel(coord)
            imgOut.putpixel(coord,pixel)

    #imgOut=Image.fromarray(SPP_Interp)
    imgOut.show()
