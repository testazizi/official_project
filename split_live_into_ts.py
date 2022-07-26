import os
from dotenv import load_dotenv
load_dotenv()

live_url= os.getenv('live_url')
table_name=os.getenv('channel_name')

def script_2(live_url,table_name):
    
    comm="while true; do rm *.ts; ffmpeg -i "+live_url+ "-hls_list_size 100 -hls_flags delete_segments -hls_time 6 -c copy "+table_name+"/"+table_name+"_videosTs/index.m3u8; done"
    os.system(comm)