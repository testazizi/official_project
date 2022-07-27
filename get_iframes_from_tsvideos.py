'''
iframe.py - ffmpeg i-frame extraction
'''

import sys, getopt, os
import subprocess
from pathlib import Path
import glob
import time
import os.path
import logging
from importlib import reload
reload(logging)
import coloredlogs
import sqlalchemy
from dotenv import load_dotenv
load_dotenv()

table_name=os.getenv('channel_name')

segment = str(sys.argv[1])

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)
# Create a filehandler object
fh = logging.FileHandler(table_name+'/'+table_name+'.log')
fh.setLevel(logging.INFO)
# Create a ColoredFormatter to use as formatter for the FileHandler
formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
coloredlogs.install(level='INFO')

#def script_3(table_name,segment):
if os.path.isfile(table_name+'/'+table_name+'_videosTs/'+segment) and ".ts" in segment:
    print('daz1')
    duration = 6
    ts = time.time()
    ts = "."+str(ts).split('.')[0]
    now = str(segment).split('.')[0]
    home = os.path.expanduser("~")
    ffmpeg = 'ffmpeg'
    cwd = os.getcwd()
    
    cmd = "ffmpeg -y -i "+table_name+"/"+table_name+"_videosTs/"+segment+" -vf 'select=gt(scene\,0.10)' -vsync vfr -frame_pts true "+table_name+"/iframe_live/"+now+str(ts)+"_%d_"+str(duration)+".png"
    #print(cmd)
    os.system(cmd)
    print('daz2')
    

# script_3(table_name,segment)