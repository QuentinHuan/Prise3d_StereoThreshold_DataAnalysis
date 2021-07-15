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

import process_data as pd
import Output as out

#path="data/p3d_arcsphere_results.log"
#path="data/p3d_contemporary-bathroom_results.log"
#path="data/p3d_caustic-view0_results.log"
#path="data/p3d_crown_results.log"
#path="data/p3d_indirect_results.log"

sceneList=["p3d_arcsphere","p3d_contemporary-bathroom","p3d_caustic-view0","p3d_crown","p3d_indirect"]
#sceneList=["p3d_indirect"]
for s in sceneList:
    print("")
    print(s)
    path="data/"+s+"_results.log"
    MP=True
    #out.showResult(path,MP)
    out.show_thresholdImage(path,"E:\image\Stereo",False,MP)

#MP=False
#out.showResult(path,MP)
#out.show_thresholdImage(path,"C:\Users\MMO\Desktop\expp3d\image",False,MP)

plt.show()