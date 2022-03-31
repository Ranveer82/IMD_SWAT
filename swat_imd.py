# -*- coding: utf-8 -*-
"""SWAT_IMD

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T1CI6KHpfAiejZaBoGYb1c-BpSMPWkkc

Author: Ranveer Kumar (iitbhu.ac.in)

**Install the library**
"""

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

#importing the library
import imdlib as imd
import pandas as pd
import os
import shutil

"""**DOWNLOADING THE DATA**"""

############### Change the parameters here #############
# parameters

grid_locations = [[25.75,82.00],[25.75,82.25],[25.75,82.5],[25.5,82.00],[25.5,82.25],
                  [25.5,82.5],[25.5,82.75],[25.25,82.5],[25.25,82.75],[25.25,82.3]]

start_yr = 2000
end_yr = 2021

########################################################

loc = grid_locations
# Working Directory
c_dir = os.getcwd()

# Creating working directories for file handling
try:
  os.mkdir('Database')
  os.mkdir('IMDSWAT')
except FileExistsError:
  print('Directories already exists !!!')

#downloading the working directory to download the data
os.chdir(c_dir+'/Database')

#variable = 'rain' # other options are ('tmin'/ 'tmax')
# downloading the data in current directories
print('downloading the gridded data from server')

data_rain =imd.get_data('rain', start_yr, end_yr, fn_format='yearwise') 
data_tmin = imd.get_data('tmin', start_yr, end_yr, fn_format='yearwise')
data_tmax = imd.get_data('tmax', start_yr, end_yr, fn_format='yearwise')

#os.chdir(c_dir)
# to save the data in other directories
#file_dir = (r'C:\Users\imdlib\Desktop\\') #Path to save the files
#imd.get_data(variable, start_yr, end_yr, fn_format='yearwise', file_dir=file_dir)

"""Plotting 

"""

# ds = data_rain.get_xarray()
# ds = ds.where(ds['rain'] != -999.) #Remove NaN values
# ds['rain'].mean('time').plot(figsize = (9,8))

# Bonus : all the grid points to find the required locations
# import numpy as np

# grid = []
# for lt in np.array(ds['lat']):
#   for ln in np.array(ds['lon']):
#     grid.append([lt,ln])

# grid = np.array(grid)
# df = pd.DataFrame(data = grid,columns = ['Lat','Long'])
# df.to_csv('xy.csv')

"""Get data for a given location, convert, and save into csv file:"""

#data.to_csv('test.csv', lat, lon, file_dir)
for pos in loc:
  data_rain.to_csv('r.csv', pos[0],pos[1])
  data_tmax.to_csv('tmx.csv',pos[0],pos[1])
  data_tmin.to_csv('tmn.csv',pos[0],pos[1])


#for lt in Latt:
#  for ln in Long:
 #    data_rain.to_csv('r.csv', lt,ln)
  #   data_tmax.to_csv('tmx.csv',lt,ln)
   #  data_tmin.to_csv('tmn.csv',lt,ln)

#os.chdir(c_dir) # back to parent directory

# station wise data for swat (tempearture and rainfall)

swat_dir = c_dir+'/IMDSWAT'

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

  f_r.write(str(data_r.iloc[0,0]).replace('-','')+'\n')
  for d in data_r.iloc[:,1].values:
      f_r.write(str(d)+'\n')

  f_t.write(str(data_tx.iloc[0,0]).replace('-','')+'\n')
  for i in range(len(data_tx)):
      f_t.write(str(data_tx.iloc[i,1])+','+str(data_tn.iloc[i,1])+'\n')
    
  print('Swat files created')
  f_r.close()
  f_t.close()

### Station file
f_s = open(swat_dir+'/'+'pcp.txt','w')
f_st = open(swat_dir+'/'+'temp.txt','w')
f_s.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')
f_st.write('ID'+','+'NAME'+','+'LAT'+','+'LONG'+','+'ELEVATION'+'\n')

i =1
for pos in loc:
  [lt,ln] = pos
  f_s.write(str(i)+','+fnr[0:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
  f_st.write(str(i)+','+'t_'+fntx[4:-4]+','+str(lt)+','+str(ln)+','+'%0.2f'%0.00+'\n')
  i+=1

f_s.close()
f_st.close()

os.chdir(c_dir)

# Cleanup
print('Cleaning Up')
shutil.rmtree(c_dir+'/Database')
#shutil.rmtree(c_dir+'/IMDSWAT')