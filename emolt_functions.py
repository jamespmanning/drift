# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 13:19:11 2022

@author: James.manning
"""
import time
import ftplib
import netCDF4
import numpy as np
import pandas as pd
import mysql.connector
import pymysql
import yaml

def get_mac(vessel):
    # given vessel returns MAC address of logger
    # by accessing database on remote machine
    # derived from George's "dbConnect.py" routine by JiM in June 2022
    # open the database connection config file
    vessel=vessel.upper().replace('_',' ')
    with open ("config.yml","r") as yamlfile:
      dbConfig=yaml.load(yamlfile, Loader=yaml.FullLoader)

    ## Connect to the development database  
    '''
    devconn = mysql.connector.connect(
      user = dbConfig['default']['db_remote']['username'],
      password = dbConfig['default']['db_remote']['password'],
      host = dbConfig['default']['db_remote']['host'],
      port = dbConfig['default']['db_remote']['port'],
      database = dbConfig['default']['db_remote']['dbname']
    )
    '''
    devconn = pymysql.connect(
      user = dbConfig['default']['db_remote']['username'],
      password = dbConfig['default']['db_remote']['password'],
      host = dbConfig['default']['db_remote']['host'],
      port = int(dbConfig['default']['db_remote']['port']),
      database = dbConfig['default']['db_remote']['dbname']
    )
    ## Query all MAC addresses associated with loggers
    cursor = devconn.cursor()

    query = "SELECT VESSEL_NAME,HARDWARE_ADDRESS FROM vessel_mac WHERE EQUIPMENT_TYPE = 'LOGGER'"

    cursor.execute(query)

    rows = cursor.fetchall()

    ## For each record returned by the query, print the sensor type, MAC address,
    ##  vessel name, and emolt vessel number from the telemetry_status Google doc
    for row in rows:
        #print(row)
        if row[0]==vessel:
            result=row[1]
            break
        else:
            result='none'
    return result
      
def eMOLT_cloud(ldata):
        # function to upload a list of files to SD machine
        for filename in ldata:
            # print u
            session = ftplib.FTP('66.114.154.52', 'huanxin', '123321')
            file = open(filename, 'rb')
            #session.cwd("/BDC")
            # session.retrlines('LIST')               # file to send
            session.storbinary("STOR " + filename.split('/')[-1], fp=file)  # send the file
            # session.close()
            session.quit()  # close file and FTP
            time.sleep(1)
            file.close()
            print(filename.split('/')[-1], 'uploaded in eMOLT endpoint')

def get_depth(loni,lati,mindist_allowed):
    # routine to get depth (meters) using vol1 from NGDC
    # mindist_allowed is the resolution in kms requested (I usually used .4)
  try:  
    if lati>=40.:
        url='https://www.ngdc.noaa.gov/thredds/dodsC/crm/crm_vol1.nc'
    else:
        url='https://www.ngdc.noaa.gov/thredds/dodsC/crm/crm_vol2.nc'
    nc = netCDF4.Dataset(url).variables 
    lon=nc['x'][:]
    lat=nc['y'][:]
    xi,yi,min_dist= nearlonlat_zl(lon,lat,loni,lati) 
    if min_dist>mindist_allowed:
      depth=np.nan
    else:
      depth=nc['z'][yi,xi]
  except:
    url='https://coastwatch.pfeg.noaa.gov/erddap/griddap/srtm30plus_LonPM180.csv?z%5B(33.):1:(47.)%5D%5B(-78.):1:(-62.)%5D'  
    df=pd.read_csv(url)
    lon=df['longitude'].values[1:].astype(np.float)
    lat=df['latitude'].values[1:].astype(np.float)
    i= nearlonlat(lon,lat,loni,lati)
    depth=df['z'].values[i]
  return depth#,min_dist

def nearlonlat_zl(lon,lat,lonp,latp): # needed for the next function get_FVCOM_bottom_temp 
    """ 
    used in "get_depth"
    """ 
    # approximation for small distance 
    cp=np.cos(latp*np.pi/180.) 
    dx=(lon-lonp)*cp
    dy=lat-latp 
    xi=np.argmin(abs(dx)) 
    yi=np.argmin(abs(dy))
    min_dist=111*np.sqrt(dx[xi]**2+dy[yi]**2)
    return xi,yi,min_dist

def nearlonlat(lon,lat,lonp,latp): # needed for the next function get_FVCOM_bottom_temp
    """
    i=nearlonlat(lon,lat,lonp,latp) change
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            For coordinates on a plane use function nearxy           
            Vitalii Sheremet, FATE Project  
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    i=np.argmin(dist2)
    return i
