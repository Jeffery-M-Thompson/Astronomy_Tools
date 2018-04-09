#!/usr/bin/env python3

import astropy as astro
import numpy as np
from astropy.table import Table
from astroquery.sdss import SDSS

def countStars(b_low, b_high, delta, release, output):
	count = int((b_high-b_low)/delta)+1
	scans = np.linspace(b_low, b_high, num=count)
	counts = Table([[],[],[]],names=('b_low', 'b_high', 'stars'))

	for b in np.nditer(scans):
		bnext = b + delta
		low = str(b)
		high = str(bnext)
		query = 'Select Count(objID) from star where (b>={0}) and (b<{1})'\
		.format(low, high)
		if output:
			print (query)
		results = SDSS.query_sql(query, data_release=release, timeout = 300)
		if output:
			print (results)
		counts.add_row([b,bnext,results['Column1'][0]])
	return counts

def getTable(b_low, b_high, l_low, l_high, delta_b, delta_l, release, output):
	query = 'Select * from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	if output:
		print (query)
	results = SDSS.query_sql(query, data_release=release, timeout = 3600)
	if output:
		print (results)
	return results
	
b_low  = -80.0
b_high = -70.0
l_low	= 0.0
l_high	=360.0
delta_b = 0.1
delta_l = 360.0
release = 14
output = True

#results = countStars(b_low,b_high, delta_b, release, output)
#file_name = '../DR{0}{1}to{2}.csv'.format(str(release),str(b_low), str(b_high))
#results.write(file_name, format='ascii.csv')
count = int((b_high-b_low)/delta_b)+1
scans = np.linspace(b_low, b_high, num=count)
for b in np.nditer(scans):	
	bnext 	= b + delta_b
	blow 	= str("%.2f" % np.round_(b,2))
	bhigh 	= str("%.2f" % np.round_(bnext,2))
	llow	= str(l_low)
	lhigh	= str(l_high)
	results = getTable(blow, bhigh, llow, lhigh, delta_b, delta_l, release, output)
	if results is None:
		print ('No results in {0} to {0}'.format(str(llow), str(lhigh)))
	else:
		file_name = './AllStars_DR{0}_{1}_to{2}.csv'.format(str(release), str(blow), str(bhigh))
		results.write(file_name, format='ascii.csv')
