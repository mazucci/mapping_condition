#!/usr/bin/env python3

import grass.script as gscript


def main():



    years = [2000, 2006, 2012, 2018]



    name_green = 'green_IT_66'



    city_f = 'IT028L3_F'



    city_c = 'IT028L3_C'



    city_com = 'IT028L3_COM'

    

    # get commuting zone vector



    gscript.run_command('g.region', flags='pa', vector=city_f, res=100)

    

    gscript.run_command('v.overlay', ainput=city_f, binput=city_c, operator='not', output=city_com, overwrite=True)



    #rasterize FUA



    gscript.run_command('v.to.rast', input=city_f, output=city_f, use='cat')



    for year in years:



        gscript.run_command('g.region', raster='clc'+str(year), flags='ap')



        gscript.run_command('r.recode', input='clc'+str(year), output='clc'+str(year)+'L1', rules='\\\ies-ud01\\D3_Natcapes\\mapping_condition\\recodeCLC.txt')



        gscript.run_command('r.recode', input='clc'+str(year), output='clc'+str(year)+'L1arti', rules='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\recodeonlyartificial.txt')



    gscript.run_command('g.region', raster=name_green+'.2',flags='a')



    # mean 2000



    gscript.run_command('r.mapcalc', expression='NDVI_2000 = ('+name_green+'.4 + '+name_green+'.5 + '+name_green+'.6 + '+name_green+'.7 + '+name_green+'.8)/5')



    gscript.run_command('r.mapcalc', expression='NDVI_2006 = ('+name_green+'.10 + '+name_green+'.11 + '+name_green+'.12 + '+name_green+'.13 + '+name_green+'.14)/5')



    gscript.run_command('r.mapcalc', expression='NDVI_2012 = ('+name_green+'.16 + '+name_green+'.17 + '+name_green+'.18 + '+name_green+'.19 + '+name_green+'.20)/5')



    gscript.run_command('r.mapcalc', expression='NDVI_2018 = ('+name_green+'.20 + '+name_green+'.21 + '+name_green+'.22 + '+name_green+'.23 + '+name_green+'.24)/5')



    for year in years:



        # calc fua extent recoded



        gscript.run_command('g.region', flags='pa', vector=city_f, res=100)



        gscript.run_command('r.resample', input='NDVI_'+str(year), output='NDVI_'+str(year)+'_100')



        gscript.run_command('r.recode', input='NDVI_'+str(year)+'_100', output='NDVI_'+str(year)+'_100_r', rules='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\recodeNDVI.txt')



        # overlay recoded NDVI over CLC level 1 for the FUA



        gscript.run_command('r.mapcalc', expression='clc'+str(year)+'L1_plus = (if(clc'+str(year)+'L1 ==1, NDVI_'+str(year)+'_100_r, clc'+str(year)+'L1))*'+city_f, overwrite=True)


        # r.stats for the FUA



        gscript.run_command('r.stats', flags='c', input=city_f+',clc'+str(year)+'L1_plus', output='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\extent_'+str(year)+'.csv', separator='comma', overwrite=True)


        # core city



        gscript.run_command('g.region', flags='pa', vector=city_c, res=100)



        gscript.run_command('r.mask', vector=city_c, overwrite=True)



        gscript.run_command('r.stats', flags='c', input='clc'+str(year)+'L1_plus', output='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\extent_c_'+str(year)+'.csv', separator='comma', overwrite=True)



        # commuting zone



        gscript.run_command('g.region', flags='pa', vector=city_f, res=100)



        gscript.run_command('r.mask', vector=city_com, overwrite=True)



        gscript.run_command('g.region', flags='pa', vector=city_com, res=100)



        gscript.run_command('r.stats', flags='c', input='clc'+str(year)+'L1_plus', output='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\extent_com_'+str(year)+'.csv', separator='comma', overwrite=True)



        # remove mask



        gscript.run_command('r.mask', flags='r')

    

    #gscript.run_command('g.region', flags='pa', vector=city_c, res=100)



    #gscript.run_command('v.to.rast', input=city_c, output=city_c, use='cat')



    #gscript.run_command('r.mapcalc', expression='clc2000L1_plusc = (if(clc2000L1 ==1, NDVI_2000_100_r, clc2000L1))*'+city_c, overwrite=True)



    #gscript.run_command('r.stats', flags='c', input=city_c+',clc2000L1_plusc', output='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\extent_c_2000.csv', separator='comma', overwrite=True)



    #gscript.run_command('g.region', flags='pa', vector=city_f, res=100)



    #gscript.run_command('v.overlay', ainput=city_f, binput=city_c, operator='not', output=city_com, overwrite=True)



    #gscript.run_command('g.region', flags='pa', vector=city_com, res=100)



    #gscript.run_command('v.to.rast', input=city_com, output=city_com, use='cat')



    #gscript.run_command('r.mapcalc', expression='clc2000L1_pluscom = (if(clc2000L1 ==1, NDVI_2000_100_r, clc2000L1))*'+city_com, overwrite=True)



    #gscript.run_command('r.stats', flags='c', input=city_c+',clc2000L1_pluscom', output='\\\ies-ud01\\D3_NATCAPES\\mapping_condition\\extent_com_2000.csv', separator='comma', overwrite=True)




if __name__ == '__main__':
    main()
