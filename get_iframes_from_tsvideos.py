'''
iframe.py - ffmpeg i-frame extraction
'''

import sys, getopt, os
import subprocess
from pathlib import Path
import glob
import time
import os.path
from dotenv import load_dotenv
load_dotenv()

table_name=os.getenv('channel_name')

segment = str(sys.argv[1])

if os.path.isfile(table_name+'/'+table_name+'_videosTs/'+segment) and ".ts" in segment:


    duration = 6
    ts = time.time()
    ts = "."+str(ts).split('.')[0]
    now = str(segment).split('.')[0]

    home = os.path.expanduser("~")
    ffmpeg = 'ffmpeg'
    cwd = os.getcwd()



    cmd = "ffmpeg -y -i 2m_hls/"+segment+" -vf 'select=gt(scene\,0.10)' -vsync vfr -frame_pts true iframes_live/"+now+str(ts)+"_%d_"+str(duration)+".png"

    print(cmd)

    os.system(cmd)
