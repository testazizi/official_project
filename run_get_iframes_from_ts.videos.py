import os
from dotenv import load_dotenv
load_dotenv()

table_name=os.getenv('channel_name')

def script_4(table_name):
    
    
    com='inotifywait -m '+table_name+'/'+table_name+'_videosTs -e close_write |     while read directory action file; do         if [[ "$file" =~ .*ts$ ]]; then              python3 get_iframes_from_tsvideos.py $file ;         fi;     done'
    #print(com)
    os.system('inotifywait -m '+table_name+'/'+table_name+'_videosTs -e close_write |     while read directory action file; do         if [[ "$file" =~ .*ts$ ]]; then              python3 get_iframes_from_tsvideos.py $file ;         fi;     done')
    

script_4(table_name)