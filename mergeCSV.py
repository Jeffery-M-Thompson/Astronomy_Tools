#!/usr/bin/env python3

""" This file is here to merge individual csv files into one file
The csv files in a directory are read.
This assumes they have the same column headers.
Due to these files being generated by the same script this is true,
but this program does no checking to verify this currently. """

import os
import csv
import sys

input_path = sys.argv[1]
output_file_name = sys.argv[2]



with open(output_file_name, 'w', newline='') as outfile:
	fieldnames = ['objID', 'ra', 'dec', 'l', 'b', 'dered_u', 'dered_g', 'dered_r', 'dered_i', 'dered_z']
	writer = csv.DictWriter(outfile, fieldnames=fieldnames)
	
	writer.writeheader()
	for root, dirs, files in os.walk(input_path):
		for file in files:
			if file.endswith(".csv"):
					with open(file) as csvfile:
						print (file)
						reader = csv.DictReader(csvfile)
						for row in reader:
							objID = row['objID']
							ra = row['ra']
							dec = row['dec']
							l = row['l']
							b = row['b']
							dered_u = row['dered_u']
							dered_g = row['dered_g']
							dered_r = row['dered_r']
							dered_i = row['dered_i']
							dered_z = row['dered_z']
							#print(objID)
							#print('{0}: ra={1}, dec={2}, dered_g={3}, dered_r={4}'.format(objID, ra, dec, dered_g, dered_r))
							writer.writerow({
								'objID' : objID, 
								'ra':ra, 
								'dec':dec, 
								'l':l,
								'b':b,
								'dered_u':dered_u,
								'dered_g':dered_g,
								'dered_r':dered_r,
								'dered_i':dered_i,
								'dered_z':dered_z})
					
						 

							
#objID,ra,dec,l,b,dered_u,dered_g,dered_r,dered_i,dered_z

