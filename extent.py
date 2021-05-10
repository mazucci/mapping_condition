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

    for year in years:

        gscript.run_command('g.region', raster='clc'+str(year), flags='ap')

        gscript.run_command('r.recode', input='clc'+str(year), output='clc'+str(year)+'L1', rules='\\\ies-ud01\\D3_Natcapes\\mapping_condition\\recodeCLC.txt')

        # FUA

        gscript.run_command('g.region', vector=city_f, flags='ap', res=100)

        gscript.run_command('r.mask', vector=city_f)

        gscript.run_command('r.stats', flags='c', input='clc'+str(year)+'L1', separator='comma', output="E:\zurbmay\Documents\\urban_accounts\IT028L3_F_CLC"+str(year)+".csv", overwrite=True)

        # CORE CITY

        gscript.run_command('g.region', vector=city_c, flags='ap', res=100)

        gscript.run_command('r.mask', vector=city_c, overwrite=True)

        gscript.run_command('r.stats', flags='c', input='clc'+str(year)+'L1', separator='comma', output="E:\zurbmay\Documents\\urban_accounts\IT028L3_C_CLC"+str(year)+".csv", overwrite=True)

        # COM
        
        gscript.run_command('g.region', vector=city_com, flags='ap', res=100)
   
        gscript.run_command('r.mask', vector=city_com, overwrite=True)

        gscript.run_command('r.stats', flags='c', input='clc'+str(year)+'L1', separator='comma', output="E:\zurbmay\Documents\\urban_accounts\IT028L3_COM_CLC"+str(year)+".csv", overwrite=True)

        gscript.run_command('r.mask', flags='r')

if __name__ == '__main__':
    main()
