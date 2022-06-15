# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:30:46 2022

@author: Ranveer kumar
        IIT BHU, varanasi

Title: IMDSWAT 2.1

Description:
    the program provide easy one stop solution to download the 2D gridded weather data from 
    IMD and reformat it for SWAT Inputs. 
    
    Change the parameters in the bottom  section. The SWAT inputs will be created 
    the /IMDSWAT folder.
    
    Please clean the IMDSWAT folder before Rerun of the program.
    
"""

# import the libraries
import pip
def install(package):
    pip.main(['install', package])

try:
    import imdlib
    print("module 'imdlib' is installed")
except ModuleNotFoundError:
    print("module 'imdlib' is not installed")
    # or
    install("imdlib") 
    
try:
    import requests
    print("module 'requests' is installed")
except ModuleNotFoundError:
    print("module 'requests' is not installed")
    # or
    install("requests") 
    
    
import imdlib as imd
import pandas as pd
import os
import shutil
import numpy as np
import requests

########################################

def swat_wgnIMD(locs,start_year,end_year):
    '''
    

    Parameters
    ----------
    locs : 2D list 
        list of Lattitude and longitude of all the stations in a list. 
        example:
            locations = [[lat1,long1],[lat2,long2]]
    start_year : Integer
        start year for data generation, the data will be generated from 1st of
        january to the 31st of december.
    end_year : Integer
        End year for data generation, the data will be generated from 1st of
        january to the 31st of december.

    Returns
    -------
    None.

    '''
    loc = locs
    start_yr = start_year
    end_yr = end_year
# Working Directory
    c_dir = os.getcwd()

# Creating working directories for file handling
    try:
        os.mkdir('Database')
        os.mkdir('IMDSWAT')
        os.mkdir('Scraps')
    except FileExistsError:
        print('Directories already exists !!!')

#downloading the working directory to download the data
    os.chdir(c_dir+'/Database')

### Check for existing Binary data and downloading the data

    years = list(np.arange(start_yr,end_yr+1,1))

    for y in years:
        if os.path.exists(os.getcwd()+'/rain/'+str(y)+'.grd'):
            print('Rain data for year %i already exists'%y)
            # data_rain = imd.open_data('rain', y, y,'yearwise', os.getcwd()+'/rain/')
            # print('Data read sucessfull')
        else:
            print('downloading the gridded data from server')
            data_rain =imd.get_data('rain', y, y, fn_format='yearwise')
        
    for y in years:
        if os.path.exists(os.getcwd()+'/tmin/'+str(y)+'.GRD'):
            print('Tmin data for year %i already exists'%y)
            # data_tmin = imd.open_data('tmin', y, y,'yearwise', os.getcwd()+'/tmin/')
            # print('Data read sucessfull')
        else:
            print('downloading the gridded data from server')
            data_tmin =imd.get_data('tmin', y, y, fn_format='yearwise')
        
    for y in years:
        if os.path.exists(os.getcwd()+'/tmax/'+str(y)+'.GRD'):
            print('Tmax data for year %i already exists'%y)
            # data_tmax = imd.open_data('tmax', y, y,'yearwise', os.getcwd()+'/tmax/')
            # print('Data read sucessfull')
        else:
            print('downloading the gridded data from server')
            data_tmax =imd.get_data('tmax', y, y, fn_format='yearwise')
            
    data_rain = imd.open_data('rain', start_yr, end_yr,'yearwise', os.getcwd()+'/rain/')
    data_tmin = imd.open_data('tmin', start_yr, end_yr,'yearwise', os.getcwd()+'/tmin/')
    data_tmax = imd.open_data('tmax', start_yr, end_yr,'yearwise', os.getcwd()+'/tmax/')
    print('Data read sucessfull')
#### binary to csv. 
    os.chdir(c_dir+'/Scraps')    
    for pos in loc:
        data_rain.to_csv('r.csv', pos[0],pos[1])
        data_tmax.to_csv('tmx.csv',pos[0],pos[1])
        data_tmin.to_csv('tmn.csv',pos[0],pos[1])
        
#### reading the csv
    swat_dir = c_dir+'/IMDSWAT'
    swat_files=[]
    
    ### Station file
    f_s = open(swat_dir+'/'+'pcp.txt','w')
    f_st = open(swat_dir+'/'+'temp.txt','w')
    f_s.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')
    f_st.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')
    
    a = 1
    for pos in loc:
  #file names
      [lt,ln] = pos
      fnr = "r_"+'%0.2f'%lt+'_'+'%0.2f'%ln+'.csv'
      fntx = "tmx_"+'%0.2f'%lt+'_'+'%0.2f'%ln+'.csv'
      fntn = "tmn_"+'%0.2f'%lt+'_'+'%0.2f'%ln+'.csv'

      print('files for Lattitude {0} and Longitude {1} is created.'.format(lt,ln))

  # Reading the data
      data_r = pd.read_csv(fnr)
      data_tx = pd.read_csv(fntx)
      data_tn = pd.read_csv(fntn)
      print('data reading is complete')   
      
      # file creation and writing
      f_r = open(swat_dir+'/'+fnr[0:-4]+'.txt', 'w') #format of the swat file = r_lat_long.txt
      f_t = open(swat_dir+'/'+'t_'+fntx[4:-4]+'.txt', 'w')  #format of the swat file = t_lat_long.txt
      
      ### List of swat files
      swat_files.append(fnr[0:-4]+'.txt')
      swat_files.append('t_'+fntx[4:-4]+'.txt')
      ##
      
      f_r.write(str(data_r.iloc[0,0]).replace('-','')+'\n')
      for d in data_r.iloc[:,1].values:
          f_r.write(str(d)+'\n')

      f_t.write(str(data_tx.iloc[0,0]).replace('-','')+'\n')
      for i in range(len(data_tx)):
          f_t.write(str(data_tx.iloc[i,1])+','+str(data_tn.iloc[i,1])+'\n')
          
      [lt,ln] = pos
      f_s.write(str(a)+','+fnr[0:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
      f_st.write(str(a)+','+'t_'+fntx[4:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
      a+=1
    
      print('Swat files created')
      f_r.close()
      f_t.close()

### Station file
    # f_s = open(swat_dir+'/'+'pcp.txt','w')
    # f_st = open(swat_dir+'/'+'temp.txt','w')
    # f_s.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')
    # f_st.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')

    # i =1
    # for pos in loc:
    #     [lt,ln] = pos
    #     f_s.write(str(i)+','+fnr[0:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
    #     f_st.write(str(i)+','+'t_'+fntx[4:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
    #     i+=1

    f_s.close()
    f_st.close()

    os.chdir(c_dir)
    # shutil.rmtree(c_dir+'/Scraps')
    return swat_files

def swat_nasap(locs,start_year,end_year):
    """
    Download data from nasa power and process in form of SWAT Input. from 2021
    to further due to unavailability of IMD gridded data.
    
    Parameters
    ----------
    locs : 2D list 
        list of Lattitude and longitude of all the stations in a list. 
        example:
            locations = [[lat1,long1],[lat2,long2]]
    start_year : Integer
        start year for data generation, the data will be generated from 1st of
        january to the 31st of december.
    end_year : Integer
        End year for data generation, the data will be generated from 1st of
        january to the 31st of december.

    Returns
    -------
    None.

    """
    y1 = start_year
    y2 = end_year
    loc = locs
    # first step to 2020
    list_files = swat_wgnIMD(loc,y1,2020)
    
    #step 2 after 2020
    
    for xy in loc:
        [lt,ln] =xy
        api_link_r = 'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=RE&longitude='+str(ln)+'00&latitude='+str(lt)+'&start='+str(2021)+'0101&end='+str(y2)+'0430&format=CSV'
        api_link_tmin = 'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MIN&community=RE&longitude='+str(ln)+'00&latitude='+str(lt)+'&start='+str(2021)+'0101&end='+str(y2)+'0430&format=CSV'
        api_link_tmx = 'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX&community=RE&longitude='+str(ln)+'00&latitude='+str(lt)+'&start='+str(2021)+'0101&end='+str(y2)+'0430&format=CSV'
        
        res_r = requests.get(api_link_r)
        res_tmin = requests.get(api_link_tmin)
        res_tmx = requests.get(api_link_tmx)
        
        print('Responce codes: %i'%res_r.status_code)
        print('Responce codes: %i'%res_tmin.status_code)
        print('Responce codes: %i'%res_tmx.status_code)
        
        d_rain =res_r.text
        r1 = d_rain.split('\n')
        r1 = r1[10:]
        r2 = [l.split(',')[-1] for l in r1]
        
        d_tmin =res_tmin.text
        t1 = d_tmin.split('\n')
        t1 = t1[10:]
        t2 = [l.split(',')[-1] for l in t1]
        
        d_tmx =res_tmx.text
        tm1 = d_tmx.split('\n')
        tm1 = tm1[10:]
        tm2 = [l.split(',')[-1] for l in tm1]
        
        swat_dir = os.getcwd()+'/IMDSWAT'
        
        print('appending the data from nasa power to IMD data')
        f_r = open(swat_dir+'/'+'r_'+'%0.2f'%lt+'_'+'%0.2f'%ln+'.txt', 'a') #format of the swat file = r_lat_long.txt
        f_t = open(swat_dir+'/'+'t_'+'%0.2f'%lt+'_'+'%0.2f'%ln+'.txt', 'a')  #format of the swat file = t_lat_long.txt
        
        # f_r.seek(-1)
        # f_t.seek(-1)
        
        for d in r2:
            f_r.write(d+'\n')
        for t in range(len(t2)):
            f_t.write(str(tm2[t])+','+str(t2[t])+'\n')
            
        f_r.close()
        f_t.close()
        
        print('Sucess')
        
        # response = requests.get("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=RE&longitude=82.2500&latitude=25.0000&start=20210101&end=20210331&format=CSV")
    # response = requests.get("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=RE&longitude=82.2500&latitude=25.0000&start=20210101&end=20210331&format=CSV")
# 
    # print(response.status_code)
    
    # rint(response.text.split('\n'))
    
    # d1 =response.text
    # l1 = d1.split('\n')
    # l1 = l1[10:]
    # l2 = [l.split(',')[-1] for l in l1]
    
    #with open()
    
    
    return None


############### Change the parameters here #############
# Change parameters here as per requirenment
start_yr = 1990
end_yr = 2020

grid_locations = [[25,82.25],[25,82.5]]

###########################################################
if end_yr <= 2020:
    swat_wgnIMD(grid_locations,start_yr,end_yr)
else:
    swat_nasap(grid_locations,start_yr,end_yr)
