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
	
	return ALL_Table

# This generates a hdf table of all MSTO stars given the 

def query_MSTO(release, b_low, b_high):
	
	queryString = ('Select objId, ra, dec, l, b, dered_u, dered_g, dered_r,'
	'dered_i, dered_z from star where (b>={0}) and (b<{1}) and ' 
	'((dered_g) betweeen 16.0 and 23.0) and '
	'((dered_g - dered_r) between 0.1 and 0.3) and '
	'((dered_u - dered_g) > 0.4)'.format(b_low, b_high))
	
	print (queryString)
	
	MSTO_Table = SDSS.query_sql(queryString, data_release = release, timeout = 3600)
	
	return MSTO_Table

def query_All(release, b_low, b_high):	
	query = 'Select * from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	if output:
		print (query)
		results = SDSS.query_sql(query, data_release=release, timeout = 3600)
	if output:
		print (results)
	return results
	
table = query_MSTO(14, -90, -85)
print (table)
