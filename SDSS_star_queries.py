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

def query_MSTO(release, dered, b_low, b_high):
	if dered:
		queryString = 'Select objId, ra, dec, l, b, dered_u, dered_g, dered_r, dered_i, dered_z from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	else:
		queryString = 'Select objId, ra, dec, l, b, psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	return MSTO_Table
	
	
declare @correction_u real,
		@correction_g real,
		@correction_r real,
		@correction_i real,
		@correction_z real
set @correction_u = 4.239 / 5.155
set @correction_g = 3.303 / 3.793
set @correction_r = 2.285 / 2.751
set @correction_i = 1.698 / 2.086
set @correction_z = 1.263 / 1.479

Select ra, dec, l ,b, psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z, 
  extinction_u, extinction_g, extinction_r, extinction_i, extinction_z
  into mydb.MSTSouth_Neg_25_To_Neg_30 from star
WHERE ((psfmag_g -(@correction_g * extinction_g)) between 16.0 and 23.0) and
  (b <= -25.0) and (b > -30.0) and
  (((psfmag_g -(@correction_g * extinction_g) - 
  		(psfmag_r -(@correction_r * extinction_r)) between 0.1 and 0.3) and
  (((psfmag_u -(@correction_u * extinction_u) - 
  (psfmag_g -(@correction_g * extinction_g)) > 0.4) and
  (flags & dbo.fPhotoFlags('SATURATED')) = 0 and
  (flags & dbo.fPhotoFlags('EDGE')) = 0
  
	
query = 'Select * from star where (b>={0}) and (b<{1})'.format(b_low, b_high)
	if output:
		print (query)
	results = SDSS.query_sql(query, data_release=release, timeout = 3600)
	if output:
		print (results)
	return results
	
