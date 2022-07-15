#import packages
import pandas as pd
import pymysql
import MySQLdb
import os
import logging
from importlib import reload
reload(logging)
import coloredlogs
import sqlalchemy
from sqlalchemy import create_engine, String, Integer
import datetime as dt
from dotenv import load_dotenv
load_dotenv()


# Get environment variables
user = os.getenv('db_user')
password = os.getenv('db_password')
localhost = '127.0.0.1' #os.getenv('db_localhost')
db_name = os.getenv('db_name')
table_name=os.getenv('channel_name')

################create folders

#create folder has the same name as the channel name
if not os.path.exists(table_name):
    os.makedirs(table_name)
    print(f'the folder {table_name} is created !')

    project_folders=[table_name+'_videosTs','iframe_live','jingles_found','iframes']
    for fol in project_folders:
        pat = os.path.join(table_name, fol)
        if not os.path.exists(pat):
            os.makedirs(pat)
            print(f'the {pat} is created')
else:
    print('all the folders are already exist !!!.')


#create a file where we will put the logs
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



db = MySQLdb.connect(localhost,user,password)

#create the database 
cursor = db.cursor()
sql="CREATE DATABASE IF NOT EXISTS "+db_name
cursor.execute(sql)

cursor.execute("""Use """+db_name+""";
create table IF NOT EXISTS {tab}
(
    id_diffussion INT PRIMARY KEY NOT NULL,
    id_chaine VARCHAR(100),
    Event_Name VARCHAR(100),
    Arabic_Event_Name VARCHAR(100),
    French_Event_Name VARCHAR(255),
    date_naissance VARCHAR(255),
    Start_Date VARCHAR(100),
    Start_Time VARCHAR(100),
    End_Date VARCHAR(100),
    End_Time VARCHAR(100),
    Genre VARCHAR(100)
);""".format(tab=table_name))
logger.info('Create table for %s .',table_name)


#read the program and do some processing
data_path='/home/fefo/Downloads/2m.xlsx'
data=pd.read_excel(data_path,engine='openpyxl')
l=['id_diffussion', 'id_chaine', 'Event Name',
       'Arabic Event Name', 'French Event Name', 'Start Date', 'Start Time',
       'End Date', 'End Time','Genre']

df=data[l]
df=df.fillna('')
result=[col.replace(' ','_') for col in l]
df.columns=result

# insert the program into a table 
connection = pymysql.connect(host=localhost,
                         user=user,
                         password=password,
                         db=db_name)


cursor=connection.cursor()


cols = "`,`".join([str(i) for i in df.columns.tolist()])

for i,row in df.iterrows():
    sql1 = "INSERT INTO "+table_name+" (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql1, tuple(row))
    connection.commit()
logger.info('Insert data from %s into %s table.',data_path.split('/')[-1],table_name)



# #connection = pymysql.connect(user=user, password=password,
#                               host=localhost,
#                               database=db_name,
#                               auth_plugin='mysql_native_password')

sql_select_Query = "select * from "+table_name
cursor = connection.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()


#get the name of shows so we can create a folder for each show
shows_name=[]
for row in records:
    shows_name.append(row[2]) if row[2] not in shows_name else shows_name

 #create a specific folder just for the jingles
Pa=os.path.join(table_name, 'iframes')
# if not os.path.exists(Pa):
#     os.makedirs(Pa)
#     print(f'the {Pa} folder is created !')

for show in shows_name:
    path = os.path.join(Pa, show)
    if not os.path.exists(path):
        os.makedirs(path)
logger.info('Create folders(i_frames) for %s .',table_name)



