#import packages
import pandas as pd
import mysql.connector
import time
import os
import cv2
import sys
import logging
from importlib import reload
reload(logging)
import coloredlogs
import sqlalchemy
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime
from pathlib import Path
from functions import *
from dotenv import load_dotenv
import concurrent.futures
import shutil
import glob
load_dotenv()

# Get environment variables
user = os.getenv('db_user')
password = os.getenv('db_password')
localhost = os.getenv('db_localhost')
db_name = os.getenv('db_name')
table_name=os.getenv('channel_name')
channel_name=table_name

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

filename = str(sys.argv[1])


#filename ="2m/iframe_live/index4.1658835213_144_6.png" #str(sys.argv[1])
    
    #get the current time which the time of the i_frame
i_frame_time= time.strftime("%H:%M:00")
    #get all the jingles inside 2m folder as an example
logger.info('Handling this i_frame %s at %s',filename,i_frame_time)

jingles = []
for folder in get_folders_to_handle(table_name,user,password,localhost,db_name):
    for file in glob.glob(table_name+"/iframes/"+folder+"/*.png"):
        logger.info('getting %s show', folder)
    #for file in glob.glob(table_name+"/iframes/"+folder+"/*.png"):
        jingles.append(file)


#time_of_chow=''
for jingle in jingles:
#def main(jingle):
    time_of_chow=''
    print(jingle.split('/')[-2])  
    #check the similarity between the two images
    logger.info('Measure the similarity between %s and %s',filename,jingle)
    result= compare_images(filename,jingle)
    logger.info('The result of the similarity between %s and %s is %s',filename,jingle,result)
    
    
    if result!=0:
        logger.info('The %s and %s are NOT similar',filename,jingle)

    else:  
        #they are similar
        logger.info('The %s and the %s are SIMILAR',filename,jingle)
        time_of_chow=get_date_of_jingle(channel_name,jingle.split('/')[-2],user,password,localhost,db_name)[0]
        dif_time = datetime.strptime(i_frame_time,"%H:%M:%S") - datetime.strptime(':'.join(time_of_chow.split(':')[:-1]),"%H:%M:%S")
        
        if dif_time==0:
            logger.info('The %s and the %s have the same time',filename,jingle)
                
        else:
            logger.info('The %s and the %s DONT NOT have the same time',filename,jingle)
            update_jingle_time(table_name,jingle.split('/')[-2],user,password,localhost,db_name)
            logger.info('Treatement is done for this %s',filename)
            


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(main, jingles)




