"""
routine to reformat "gdp" drifter tracks to to xml
Running initially on JiMs primary desktop linux in Summer 2025 (not with rest of drifter system)

@author: JiM

Derived from drift2xml.py  but simplified
"""
import csv
import sys
import time
import ftplib
from utilities import lat2str, lon2str
from datetime import *
from matplotlib.dates import date2num,num2date
import numpy as np
import pandas as pd
#hardcode
ageactive=1
# open output and input file
filedirection='/home/user/drift/' # while testing on laptop
filename='drift_X_gdp'
#filedirection='/net/pubweb_html/drifter/'
#filedirection='/drifter/'

def eMOLT_cloud(ldata):# send file to SD machine
        # function to upload a list of files to SD machine
        for filename in ldata:
            # print u
            session = ftplib.FTP('66.114.154.52', 'huanxin', '123321')
            file = open(filename, 'rb')
            #session.cwd("/BDC")
            #session.cmd("/tracks")
            # session.retrlines('LIST')               # file to send
            session.storbinary("STOR " + filename.split('/')[-1], fp=file)  # send the file
            # session.close()
            session.quit()  # close file and FTP
            #time.sleep(1)
            file.close()
            print(filename.split('/')[-1], 'uploaded in SD endpoint')

fid=open(filedirection+'drift_X_gdp.xml','w')

#raw data loaded
#timestart=(date.today()-timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
timestart=(date.today()-timedelta(days=30)).strftime("%Y-%m-%dT00")
#url='https://erddap.aoml.noaa.gov/gdp/erddap/tabledap/OSMC_RealTime.csvp?platform_id%2Clatitude%2Clongitude&platform_type=%22DRIFTING%20BUOYS%20(GENERIC)%22&time%3E=2025-07-26T00%3A00%3A00Z&time%3C=2025-08-02T00%3A00%3A00Z&latitude%3E=25.1&latitude%3C=47&longitude%3E=-82&longitude%3C=-64'
url='https://erddap.aoml.noaa.gov/gdp/erddap/tabledap/OSMC_RealTime.csvp?platform_code%2Ctime%2Clatitude%2Clongitude&platform_type=%22DRIFTING%20BUOYS%20(GENERIC)%22&time%3E='+timestart+'%3A00%3A00Z&latitude%3E=25&latitude%3C=47&longitude%3E=-82&longitude%3C=-64'
print('reading realtime GDP erddap ...')
df=pd.read_csv(url)
ids=list(set(df['platform_code']))# list of distinct ids
print('got '+str(len(ids))+' tracks')
df['time (UTC)'] = pd.to_datetime(df['time (UTC)'])
df=df[df['time (UTC)'].dt.date>date.today()-timedelta(days=30)]# gets the last 30 days

#print ids
# write the first line of the xml output file
fid.write('<?xml version="1.0" encoding="UTF-8"?>\n<markers>\n')

# setup a set of line colors
#cc=['#FFFFFF','#33FFCC','#FF0000','#f5f5f5','#FF66FF','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC','#FFFF33',
cc=['#FFFFFF','#33FFCC','#FF0000','#9acd32','#800080','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC','#FFFF33',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57','#f5f5f5',
    '#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57','#f5f5f5',
    '#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#99CC66','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57',
    '#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff',
    '#FF0000','#f5f5f5','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57','#f5f5f5',
    '#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57','#f5f5f5',
    '#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff',
    '#FF0000','#99CC66','#3333CC','#FF66FF','#660033','#FFFF33','#33FFCC','#990066','#9900FF','#FFCC33','#9966CC','#33FFFF','#FF00CC',
    '#2e8b57','#99CC66','#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff','#2e8b57',
    '#f5f5f5','#fa8072','#008080','#9acd32','#800080','#dda0dd','#ffa500','#000080','#48d1cc','#ff00ff']
cc=cc+cc# doubles the size

    
# for each drifter write out line and marker         
for k in range(len(ids)): # loop through all the distinct deployment ids
    df1=df[df['platform_code']==ids[k]] # finds the index of all rows with this id
    year=2025
    time=list(df1['time (UTC)'].values)
    lat=list(df1['latitude (degrees_north)'].values)
    lon=list(df1['longitude (degrees_east)'].values)
    last_drifter_time=time[-1]
    active=1  
    fid.write('<line width="3" color="'+cc[k]+'">\n')
    for i in range(len(lat)):
        if np.isnan(lat[i])==False:
            fid.write('<point lat="'+str(lat[i])+'" lng="'+str(lon[i])+'"/>\n')
    fid.write('<point lat="'+str(lat[i])+'" lng="'+str(lon[i])+'"/>\n')
    fid.write('</line>\n')
    la=lat2str(round(lat[-1],2))
    lo=lon2str(round(lon[-1],2))
    if (ids[k]>=7810165) & (ids[k]<=7810167):
        boatName='Oregon II'
        schoolName='Falmouth MA High School Adopt a Drifter'
    else:
        boatname='Unknown'
        schoolName='Global Drifter Program'
        
    depth=15.      #print float(depth)
    fid.write('<marker lat="'+str(lat[-1])+'" lng="'+str(lon[-1])+'" label="'+str(ids[k])+'" active="'+str(active)+
              '" html="Drogued Drifter&lt;br&gt; School Name: '+schoolName+'&lt;br&gt; WMO_ID = '+str(ids[k])+'&lt;br&gt; Position:'+str(la)+' '+str(lo)
              +'&lt;br&gt;'+'StartTime='+str(time[0])[0:16]+'  &lt;br&gt; EndTime='
              +str(time[-1])[0:16]+' \n"/>')
#if sys.argv[1]=='drift_fa_2014_1':
#     fid.write('<marker lat="41.945" lng="-70.578333" label="Plymouth Nuclear"  html="Plymouth Nuclear Power Plant" />\n') 
fid.write('</markers>')
fid.close()
# send these output files to the StudentDrifter FTP drop
eMOLT_cloud([filedirection+filename+'.xml'])
