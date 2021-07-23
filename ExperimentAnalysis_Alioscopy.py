# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:24:37 2021

@author: Quentin

# analyse a single log file named "P3d_Expe1.log" in \WindowsNoEditor\P3d_Expe1\Saved\Logs
# results are saved in P3D/script/data/
"""
import main_lib
import sys
import os

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
wdir=get_script_path()
os.chdir(wdir)
print("WORKING DIR ="+wdir)
main_lib.process_one_log(wdir+"/../logs","p3d.log")
#main.process_one_log(wdir+"/../../Saved/Logs","P3d_Expe1.log") # path in UE4 project
print("SAVED")
