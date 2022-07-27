import pandas as pd
import mysql.connector
import time
import os
import cv2
import sys
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime
from pathlib import Path
from importlib import reload
import logging
reload(logging)
import coloredlogs
import sqlalchemy

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

def get_date_of_jingle(channel_name,jingle,user,password,localhost,db_name):
    
    current_date=time.strftime("%d:%m:%Y").replace(':','/')
    current_time=datetime.strptime(time.strftime("%H:%M:%S"),"%H:%M:%S")
    result=''
    
    connection = mysql.connector.connect(host=localhost,
                         user=user,
                         password=password,
                         db=db_name,
                        auth_plugin='mysql_native_password')
    
    cursor=connection.cursor()

    sql='select Start_Time from ' +channel_name+ ' where Start_Date='+'"'+current_date+'"'+' and Event_name='+'"'+jingle+'"'
    cursor.execute(sql)
    records = cursor.fetchall()
    
    if len(records)==1:
        return records[0]
    else:
    
        for record in records:
            #print(record)
            interval=[]
            interval.append(datetime.strptime(':'.join(record[0].split(':')[:3]),"%H:%M:%S")- timedelta(minutes=150))
            interval.append(datetime.strptime(':'.join(record[0].split(':')[:3]),"%H:%M:%S")+ timedelta(minutes=150))
        
        
            if current_time>interval[0] and current_time<interval[1]:
                result=record
                break
        
            
        return result


def update_jingle_time(channel_name,jingle,user,password,localhost,db_name):
    
    current_date=time.strftime("%d:%m:%Y").replace(':','/')
    current_time=(time.strftime("%H:%M:%S")+":00",)
    result=get_date_of_jingle(channel_name,jingle,user,password,localhost,db_name)
    
    connection = mysql.connector.connect(host=localhost,
                         user=user,
                         password=password,
                         db=db_name,
                        auth_plugin='mysql_native_password')
    
    cursor=connection.cursor()
    #sql='UPDATE '+channel_name+' SET Start_Time ="'+current_time[0]+'" where Start_Date="'+current_date+'" and Event_name="'+jingle+'" and Start_Time=""'
    
    sql='UPDATE '+channel_name+' SET Start_Time ='+'"'+current_time[0]+'"'+' where Start_Date='+'"'+current_date+'"'+' and Event_name='+'"'+jingle+'"'+' and Start_Time='+'"'+result[0]+'"'
    #print(sql)
    #ple=(current_time[0],result[0])
    
    cursor.execute(sql)
    
    connection.commit()
    logger.info('Update the time %s of the %s by %s',result[0],jingle,current_time[0])


def compare_images(i_frame,jingle):
    img1=cv2.imread(i_frame)
    img2=cv2.imread(jingle)
    #print(img1)
    #print(img2)
    
    orb= cv2.ORB_create()
    
    kb_a, desc_a= orb.detectAndCompute(img1,None)
    kb_b, desc_b= orb.detectAndCompute(img2,None)
     
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches=bf.match(desc_a, desc_b)
    similar_regions=[i for i in matches if i.distance < 50]
    
    if len(matches) ==0:
        return 0
    return len(similar_regions)/len(matches)


############## there is a case to handle when we handle the beginning of a show
def get_folders_to_handle(table_name,user,password,localhost,db_name):
    
    current_date=time.strftime("%d:%m:%Y").replace(':','/')
    connection = mysql.connector.connect(host=localhost,
                         user=user,
                         password=password,
                         db=db_name,
                        auth_plugin='mysql_native_password')
    
    sql='select Start_Time, id_diffussion, Event_Name from '+table_name+' where Start_Date='+'"'+current_date+'"'
    cursor=connection.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    idd=[]
    times=[]
    event=[]
    
    for rec in records:
        times.append(datetime.strptime(':'.join(rec[0].split(':')[:-1]), "%H:%M:%S"))
        idd.append(rec[1])
        event.append(rec[2])
        
    data={'id_diffussion':idd,'Start_Time':times,'Event_Name':event}
    df=pd.DataFrame(data)
        
    curent_time_minus=datetime.strptime(time.strftime("%H:%M:%S"),"%H:%M:%S")- timedelta(hours=1.5)
    curent_time_plus=datetime.strptime(time.strftime("%H:%M:%S"),"%H:%M:%S")+ timedelta(hours=1.5)
        
    get_idd_frame=df[(df.Start_Time<curent_time_plus) & (df.Start_Time>curent_time_minus)]
        
    return list(get_idd_frame.Event_Name)