#import packages
import pandas as pd
import mysql.connector
import time
import cv2
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import glob
load_dotenv()

# Get environment variables
user = os.getenv('db_user')
password = os.getenv('db_password')
localhost = os.getenv('db_localhost')
db_name = os.getenv('db_name')
table_name=os.getenv('channel_name')



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

    sql='select Start_Time from ' +channel_name+ 'where Start_Date='+'"'+current_date+'"'+' and Event_name='+'"'+jingle+'"'
    cursor.execute(sql)
    records = cursor.fetchall()
    
    if len(records)==1:
        return records[0]
    else:
    
        for record in records:
            #print(record)
            interval=[]
            interval.append(datetime.strptime(':'.join(record[0].split(':')[:3]),"%H:%M:%S")- timedelta(minutes=10))
            interval.append(datetime.strptime(':'.join(record[0].split(':')[:3]),"%H:%M:%S")+ timedelta(minutes=10))
        
        
            if current_time>interval[0] and current_time<interval[1]:
                result=record
        
            
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
    
    sql='UPDATE '+channel_name+ 'SET Start_Time =%s where Start_Date='+'"'+current_date+'"'+' and Event_name='+'"'+jingle+'"'+'and Start_Time=%s'
    ple=(current_time[0],result[0])
    
    cursor.execute(sql,ple)
    
    
    connection.commit()

def compare_images(i_frame,jingle):
    pass



############## there is a case to handle when we handle the beginning of a show
def get_folders_to_handle(channel_name,jingle,user,password,localhost,db_name):
    
    current_date=time.strftime("%d:%m:%Y").replace(':','/')
    connection = mysql.connector.connect(host=localhost,
                         user=user,
                         password=password,
                         db=db_name,
                        auth_plugin='mysql_native_password')
    
    cursor=connection.cursor()
    result=get_date_of_jingle(channel_name,jingle,user,password,localhost,db_name)[0]
    sql='select id_diffussion from '+channel_name+ 'where Start_Date='+'"'+current_date+'"'+' and Event_name='+'"'+jingle+'"'+'and'+' Start_Time='+'"'+result+'"'
    #sql='second select id_diffussion from rotana where Start_Date="01/07/2022" and Event_name="Al Wa3D"and Start_Time="00:40:00:00"'
    #print('second',sql)
    cursor.execute(sql)
    records = cursor.fetchall()
    
    #print(records[0][0])
    
    idd=int(records[0][0])
    prev,next=idd-1,idd+1
    
    sql1='SELECT 1 FROM '+channel_name+' WHERE id_diffussion='+'"'+str(prev)+'"'
    cursor.execute(sql1)
    
    records1 = cursor.fetchall()
    if records1==[]:
        #for recor in records:
        #event_name_1=get_records(prev,channel_name,user,password,localhost,db_name)
        event_name_2=get_records(records[0][0],channel_name,user,password,localhost,db_name)
        event_name_3=get_records(next,channel_name,user,password,localhost,db_name)
        return event_name_2,event_name_3
        
    else:
        event_name_1=get_records(prev,channel_name,user,password,localhost,db_name)
        event_name_2=get_records(records[0][0],channel_name,user,password,localhost,db_name)
        event_name_3=get_records(next,channel_name,user,password,localhost,db_name)
        
        return event_name_1,event_name_2,event_name_3





filename = str(sys.argv[1])

#read the i_frame
i_frame_detected= cv2.imread(filename)

#get the current time which the time of the i_frame
i_frame_time= time.strftime("%H:%M:00")

#get all the jingles inside 2m folder as an example

jingles = []
for folder in list(get_folders_to_handle(table_name,jingle.split('/')[-2],user,password,localhost,db_name)):
    for file in glob.glob("test_epg_server/jingles_iframes/"+folder+"/*.png"):
        jingles.append(file)

for jingle in jingles:
    #check the similarity between the two images
    result= compare_images(i_frame,jingle)
    
    # if they're not similar do nothing
    if result<0.5:
        pass
    
    else:  #they are similar
        
        logger.info('There is a similarity between this i_frame %s and this i_frame %s at %s',jingle,i_frame,i_frame_time)
        dif_time = i_frame_time - get_date_of_jingle(table_name,jingle.split('/')[-2],user,password,localhost,db_name)
        
        if dif_time==0:
            pass
        else:
            update_jingle_time(table_name,jingle.split('/')[-2],user,password,localhost,db_name)


