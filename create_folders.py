import mysql.connector
import os  
from dotenv import load_dotenv
load_dotenv()

# Get environment variables
user = os.getenv('db_user')
password = os.getenv('db_password')
localhost = os.getenv('db_localhost')
db_name = os.getenv('db_name')
table_name=os.getenv('channel_name')

#create folder has the same name as the channel name
if not os.path.exists(table_name):
    os.makedirs(table_name)
    print(f'the folder {table_name} is created !')

    project_folders=[table_name+'_videosTs','iframe_live','jingles_found']
    for fol in project_folders:
        pat = os.path.join(table_name, fol)
        if not os.path.exists(pat):
            os.makedirs(pat)
            print(f'the {pat} is created')

    

    #create a specific folder just for the jingles
    Pa=os.path.join(table_name, 'jingles')
    if not os.path.exists(Pa):
        os.makedirs(Pa)
        print(f'the {Pa} folder is created !')

    
    connection = mysql.connector.connect(user=user, password=password,
                              host=localhost,
                              database=db_name,
                              auth_plugin='mysql_native_password')

    sql_select_Query = "select * from "+table_name
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    records = cursor.fetchall()


    #get the name of shows so we can create a folder for each show
    shows_name=[]
    for row in records:
        shows_name.append(row[2]) if row[2] not in shows_name else shows_name
    
    for show in shows_name:
        path = os.path.join(Pa, show)
        if not os.path.exists(path):
            os.makedirs(path)
    print('create folders of the Event_name !')

else:
    print(f'{table_name} and all its folders are already created')

# project_folders=[table_name+'_videosTs','iframe_live','jingles_found']
# for fol in project_folders:
#     pat = os.path.join(table_name, fol)
#     if not os.path.exists(pat):
#         os.makedirs(pat)
#         print('create this !',pat)
    

# connection = mysql.connector.connect(user=user, password=password,
#                               host=localhost,
#                               database=db_name,
#                               auth_plugin='mysql_native_password')

# sql_select_Query = "select * from "+table_name
# cursor = connection.cursor()
# cursor.execute(sql_select_Query)
#     # get all records
# records = cursor.fetchall()

# create a specific folder just for the jingles
# Pa=os.path.join(table_name, 'jingles')
# if not os.path.exists(Pa):
#     os.makedirs(Pa)

# #get the name of shows so we can create a folder for each show
# shows_name=[]
# for row in records:
#     shows_name.append(row[2]) if row[2] not in shows_name else shows_name

# for show in shows_name:
#     path = os.path.join(Pa, show)
#     if not os.path.exists(path):
#         os.makedirs(path)



