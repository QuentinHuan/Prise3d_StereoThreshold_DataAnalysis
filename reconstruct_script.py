"""
@author: Quentin Huan

script for computing thresholds and reconstruction the corresponding images
Will process all the scenes in "sceneList"
"""
import matplotlib.pyplot as plt
import numpy as np
import output_lib as out

# 2d thresholds
Thresholds = {"p3d_arcsphere-view0": [2733, 1640, 1560, 2533, 3693, 2166, 2506, 2833, 4866, 3766, 3273, 3173, 1766, 2013, 2913, 3213],
              "p3d_contemporary-bathroom-view0": [10000, 10000, 10000, 10000, 3086, 10000, 10000, 10000, 10000, 10000, 9013, 9073, 9666, 9040, 3060, 3293],
              "p3d_caustic-view0": [2313, 5306, 3953, 1760, 2106, 2166, 2026, 2820, 3620, 4906, 5173, 4426, 3560, 4033, 5160, 4966],
              "p3d_crown-view0": [1286, 6680, 3760, 1293, 2153, 6146, 4953, 2640, 4420, 2086, 2286, 3980, 4486, 3766, 3553, 3093],
              "p3d_indirect-view0": [1020, 1286, 2166, 6086, 1286, 1020, 3093, 5686, 686, 1086, 2553, 3020, 420, 1486, 2086, 2753]}

sceneList = ["p3d_arcsphere", "p3d_contemporary-bathroom",
             "p3d_caustic-view0", "p3d_crown", "p3d_indirect"]  # list 1
#sceneList = ["p3d_kitchen-view0", "p3d_kitchen-view1", "p3d_landscape-view3", "p3d_sanmiguel-view1", "p3d_sanmiguel-view2"]  # list 2
#sceneList = ["p3d_kitchen-view0"]  # for quick testing

# compute a final threshold estimation and reconstruct the composite image
# result files should be located in ./data/
# args:
#    showData = true to display a plot of all the data point and the logistic curves
#    type = "stereo" or "8pov"


def rebuild_Images(type="stereo", showData=False):
    c = 0
    for s in sceneList:
        c = c+1
        print("-----------------------------------")
        print("("+str(c)+"/"+str(len(sceneList))+")")
        path = "data/"+s+"_results.log"

        Threshold = out.compute_thresholds(
            path, finalEstimation="99perc", fullParam=True)
        T = []
        Sig = []
        for i in range(16):
            T.append(Threshold[i][1])
            Sig.append(Threshold[i][0])
        T = np.asarray(T)
        print(s+" threshold : ")
        for i in range(16):
            print(str(20*T[i])+" & ", end="")
        print("")
        # data plot
        if showData:
            out.showResult(Threshold, path, True, method="99perc")

        # stereo parameters
        if type == "stereo":
            resolution = 800
            imagePath = "/home/stagiaire/Bureau/image/stereo"
            ListOfPov = ["right", "left"]
        # 8pov parameters
        if type == "8pov":
            imagePath = "/home/stagiaire/Bureau/image/8pov"
            resolution = 360
            ListOfPov = range(1, 9)
        # reconstruction
        for i in ListOfPov:
            out.reconstruct_thresholdImage(
                T, path, imagePath, resolution, resolution, str(i), method="nearest", show=False)


# plot threshold 2d against threshold stereo
"""    ## plot all thresholds
        X = np.linspace(0,15,16)
        Y1 = np.asarray(Thresholds.get(sceneList[0]))
        Y2 = np.asarray(T)
        # plt.plot(X,Y1,"r")
        # plt.plot(X,Y2,"b")
        E = np.prod(Y2/Y1)
        print(E)
        plt.plot(Y2,Y1,".")
        plt.xlim([0, 10000])
        plt.ylim([0, 10000])

plt.show() """

rebuild_Images(type="stereo", showData=False)
plt.show()
