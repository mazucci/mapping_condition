# !/usr/bin/env python2.7
# extract univar per core cities / commuting zones / FUA

import os
import sys
import subprocess
import pandas as pd
import numpy as np
import time

start = time.time()
########### ########### ########### ########### ########### ########### ########### ########### ###########
########### ########### ########### ########### ########### ########### ########### ########### ###########
# path to the GRASS GIS launch script
# Linux
grass7bin_lin = 'grass'
# DATA
# define GRASS DATABASE # add your path to grassdata (GRASS GIS database) directory "~
gisdb = os.path.join(os.path.expanduser("/DATA/"), "grassdata")
# specify (existing) location and mapset
location = "newLocation"
mapset = "PERMANENT"

########### SOFTWARE
if sys.platform.startswith('linux'):
    # we assume that the GRASS GIS start script is available and in the PATH
    # query GRASS 7 itself for its GISBASE
    grass7bin = grass7bin_lin

# query GRASS 7 itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']

p = subprocess.Popen(startcmd, shell=False,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if p.returncode != 0:
    print >> sys.stderr, "ERROR: Cannot find GRASS GIS 7 start script (%s)" % startcmd
    sys.exit(-1)
gisbase = out.decode('utf8').strip('\n\r')

# Set GISBASE environment variable
os.environ['GISBASE'] = gisbase
# the following not needed with trunk
os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')
# define GRASS-Python environment
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)
########### ########### ########### ########### ########### ########### ########### ########### ###########

# Set GISDBASE environment variable
os.environ['GISDBASE'] = gisdb

# looking(script, '*command*')
# import GRASS Python bindings (see also pygrass)
import grass.script as gscript
import grass.script.setup as gsetup
import grass.script as grass

###########
# launch session
gsetup.init(gisbase,
            gisdb, location, mapset)

gscript.message('Current GRASS GIS 7 environment:')
# print gscript.gisenv()

gscript.message('Available raster maps:')
rasterL = []
rasterL2=[]
for rast in gscript.list_strings(type='rast'):
    rasterL.append(rast)
    rasterL2.append(rast)
rasterL2 = [rast.replace('@'+mapset, '') for rast in rasterL2]

vectlist = []
for vect in gscript.list_strings(type='vect'):
    vectlist.append(vect)

vectlist = [vect.replace('@'+mapset, '') for vect in vectlist]
#
#
# #########################################################
# # from the table get the FUA code #
sites_list = '/D3_NATCAPES/Users/zuliagr/FUA_2018/missed_core_cities.csv' # List_kernel.csv' #missed_core_cities.csv'#List_FUAs_F_with_cat.csv'  #List_FUAs_C_with_cat.csv' # list of sites List_FUAs_with_cat.csv
sites = pd.read_csv(sites_list)
print(sites)
# reporting_unit = 'FUA_'

results = pd.DataFrame([])
vect= 'URAU2018_EU28_C' #'URAU2018_EU28_F'#URAU2018_EU28_C@PERMANENT 'LAU_only_FUA'
field='cat'
indata = 'tc10m'#
for index, row in sites.iterrows():
    site = (row['cat'])
    urauid = (row['URAU_ID'])
    # fuaid = (row['urau_F'])
    # gisco_id = (row['GISCO_ID'])
    print(site)
    name_vect = "tempdcore_" + str(site)
    name_zone_ras = "temp_core_" + str(site)
    grass.run_command("v.extract", overwrite=True, input=vect, output=name_vect, where=field + "=" + str(site))
   #setta la region con flag a (allinea)
    grass.run_command('g.region', flags='a', vector=name_vect, res=10)
    grass.run_command("v.to.rast", input=name_vect, output=name_zone_ras, use='val', value='1', overwrite=True)

    grass.run_command('g.region', flags='a', raster=name_zone_ras, res=10)
# importante settare zones (altrimenti usa l'extent e il calcolo delle medie sbagliato)
    p = grass.pipe_command('r.univar', map=indata, zones=name_zone_ras, quiet=True, flags='et', separator='comma')
    rowL = []
    for line in p.stdout:
        line2 = line.split(',')
        rowL.append(line2)
    table_base_df = pd.DataFrame(rowL)

    f = table_base_df.replace('\n', ' ', regex=True)
    table_base_df = table_base_df.replace('%', ' ', regex=True)

    # # dropping null value columns to avoid errors
    table_base_df.dropna(inplace=True)

    ##field names if extended
    table_base_df.rename(columns={0: 'zone', 1: 'label', 2: 'non_null_cells', 3: 'null_cells', 4: 'min',
                                  5: 'max', 6: 'range', 7: 'mean', 8: 'mean_of_abs', 9: 'stddev',
                                  10: 'variance', 11: 'coeff_var', 12: 'sum', 13: 'sum_abs', 14: 'first_quart',
                                  15: 'median', 16: 'third_quart', 17: 'perc_90'}, inplace=True)
    pd.set_option('display.max_columns', None)


    table_base_df = table_base_df[1:]
    table_base_df1 = table_base_df.filter(['mean', 'sum', 'non_null_cells'],axis=1)

# #     #     #
    a1 = np.array(table_base_df1)
    a2 = a1.astype(np.float)

    headers = ['mean', 'sum', 'non_null_cells']
    table_base_df2 = pd.DataFrame(a2, columns=headers)

    table_base_df2['cat'] = str(site)  # add the cat code
    table_base_df2['city'] = str(urauid) #add the city code
    # table_base_df2['fua'] = str(fuaid)  # add the city code
    # table_base_df2['fua'] = str(urauid)  # add the city code
    # table_base_df2['GISCO_ID'] = str(gisco_id)  # add the LAU code

    results = results.append(table_base_df2)
    #delete temp ras

    # grass.run_command('g.remove', flags='f', type='vector', name=name_vect, quiet=True)
    # grass.run_command('g.remove', flags='f', type='raster', name=name_zone_ras, quiet=True)
#
#
results.fillna(0.0, inplace=True)
print results
results.to_csv('/D3_NATCAPES/Users/zuliagr/paper_green_balance/Tree_cover_Cuff2.csv')
# # results.to_csv('/D3_NATCAPES/Users/zuliagr/paper_green_balance/out_tables/ndvi2010_pd_districts.csv')
print ('end')
