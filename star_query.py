#!/usr/bin/env python3

import astropy as astro
import numpy as np
from astropy.table import Table
from astroquery.sdss import SDSS

b_low  = -90.0
b_high = 90.0

delta  = 1.0
count = int((b_high-b_low)/delta)+1
scans = np.linspace(b_low, b_high, num=count)
counts = Table([[],[],[]],names=('b_low', 'b_high', 'stars'))

for b in np.nditer(scans):
	bnext = b + delta
	low = str(b)
	high = str(bnext)
	query = 'Select Count(objID) from star where (b>={0}) and (b<{1})'.format(low, high)
	print (query)
	results = SDSS.query_sql(query, data_release=14, timeout = 300)
	print (results)
	counts.add_row([b,bnext,results['Column1'][0]])

file_name = '/media/pi/Research_Data/Star_Counts_SDSS_DR14/DR14_{0}_to_{1}.csv'\
.format(str(b_low), str(bnext))
counts.write(file_name, format='ascii.csv', overwrite=True)
