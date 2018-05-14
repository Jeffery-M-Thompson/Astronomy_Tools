#!/usr/bin/env python3

import astropy as astro
import numpy as np
from astropy.table import Table
from astroquery.sdss import SDSS

# This script executes selected common SDSS queries and stores
# the reults in an hdf5 file to preserve table information

# The script will need an hdf5 file name
# The script will need a data path to store the results in.
# If the file name and the path exist it will append the existing data.



def write_table(query_results):
	
	return file_HDF5

# This generates a hdf5 file of all the stars in SDSS given the data release

def query_star(release):	
	query = 'Select * from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	if output:
		print (query)
		results = SDSS.query_sql(query, data_release=release, timeout = 3600)
	if output:
		print (results)
	return results

# This generates a hdf table of all MSTO stars given the 

def query_MSTO(release, b_low, b_high):

	queryString = ('Select objID, ra, dec, l, b, dered_u, dered_g, dered_r, dered_i, '
	'dered_z from star WHERE b>={0} and b<{1} AND '
	'dered_g BETWEEN 16.0 AND 23.0 AND '
	'(dered_g - dered_r) BETWEEN 0.1 AND 0.3 AND '
	'(dered_u - dered_g) > 0.4 AND '
	'(flags & dbo.fPhotoFlags(\'SATURATED\')) = 0 AND '
	'(flags & dbo.fPhotoFlags(\'EDGE\')) = 0').format(b_low, b_high)	
	print (queryString)
	
	MSTO_Table = SDSS.query_sql(queryString, data_release = release, timeout = 3600)

	return MSTO_Table
	
b_low  = 0.0
b_high = 90.0
delta_b = 1.0
release = 14

count = int((b_high-b_low)/delta_b)+1
scans = np.linspace(b_low, b_high, num=count)
for b in np.nditer(scans):	
	bnext 	= b + delta_b
	blow 	= str("%.2f" % np.round_(b,2))
	bhigh 	= str("%.2f" % np.round_(bnext,2))
	qtable = query_MSTO(release, blow, bhigh)
	print(qtable)
	if qtable is None:
		noneR ='No results in {0} to {1}'.format(blow, bhigh)
		print(noneR)
	else:
		file_name = './MSTO_stars_DR_{0}_{1}_to{2}.csv'.format(str(release), str(blow), str(bhigh))
		qtable.write(file_name, format='ascii.csv')



