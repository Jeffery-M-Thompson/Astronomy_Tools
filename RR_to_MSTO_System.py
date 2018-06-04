#!/usr/bin/env python3

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import Distance
from astropy.table import Table
from astropy.cosmology import WMAP5, WMAP7

import numpy as np
import os
import csv
import sys

input_path = sys.argv[1]
output_file_name = sys.argv[2]

rr_lyrae = Table(
	names=(
		'RAdeg','DEdeg','S3ab','S3c','DM','Per','phi0',
		'gAmp','rAmp','iAmp','zAmp',
		'gmag','rmag','imag','zmag',
		'Tg','Tr','Ti','Tz',
		'<gmag>','<rmag>','<imag>','<zmag>',
		'E(B-V)',
		'Ldeg', 'Bdeg',
		'Rdist'
	),
	dtype=(
		'f8','f8','f8','f8','f8','f8','f8',
		'f8','f8','f8','f8',
		'f8','f8','f8','f8',
		'i4','i4','i4','i4',
		'f8','f8','f8','f8',
		'f8',
		'f8','f8',
		'f8'
	)
)

rr_lyrae['RAdeg'].u =	'deg'
rr_lyrae['DEdeg'].u =	'deg'
rr_lyrae['DM'].u	=	'mag'
rr_lyrae['Per'].u	=	'd'
rr_lyrae['gAmp'].u	=	'mag'
rr_lyrae['rAmp'].u	=	'mag'
rr_lyrae['iAmp'].u	=	'mag'
rr_lyrae['zAmp'].u	=	'mag'
rr_lyrae['gmag'].u	=	'mag'
rr_lyrae['rmag'].u	=	'mag'
rr_lyrae['imag'].u	=	'mag'
rr_lyrae['zmag'].u	=	'mag'
rr_lyrae['<gmag>'].u=	'mag'
rr_lyrae['<rmag>'].u=	'mag'
rr_lyrae['<imag>'].u=	'mag'
rr_lyrae['<zmag>'].u=	'mag'
rr_lyrae['E(B-V)'].u=	'mag'
rr_lyrae['Ldeg'].u	=	'deg'
rr_lyrae['Bdeg'].u	=	'deg'
rr_lyrae['Rdist'].u	=	'kpc'
index=0
with open(input_path) as csvfile:
	rr_dat = csv.reader(csvfile, delimiter=' ',skipinitialspace=True)
	for row in rr_dat:
		#print(row)
		index = index+1
		RA		=	float(row[0])
		DEC		=	float(row[1])
		S3ab	=	float(row[2])
		S3c		=	float(row[3])
		DM		=	float(row[4])
		Per		=	float(row[5])
		Phi0	=	float(row[6])
		gamp	=	float(row[7])
		ramp	=	float(row[8])
		iamp	=	float(row[9])
		zamp	=	float(row[10])
		gmag	=	float(row[11])
		rmag	=	float(row[12])
		imag	=	float(row[13])
		zmag	=	float(row[14])
		Tg		=	int(row[15])
		Tr		=	int(row[16])
		Ti		=	int(row[17])
		Tz		=	int(row[18])
		Agmag	=	float(row[19])
		Armag	=	float(row[20])
		Aimag	=	float(row[21])
		Azmag	=	float(row[22])
		EBV		=	float(row[23])
		Sky		=	SkyCoord(ra=RA*u.degree, dec=DEC*u.degree)
		L		=	Sky.galactic.l.degree
		B		=	Sky.galactic.b.degree
		R		=	Distance(distmod=DM, unit=u.kpc)
		rr_lyrae.add_row([
			RA,DEC,S3ab,S3c,DM,Per,Phi0,
			gamp,ramp,iamp,zamp,
			gmag,rmag,imag,zmag,
			Tg,Tr,Ti,Tz,
			Agmag,Armag,Aimag,Azmag,
			EBV,
			L,B,
			R])
		if (index%5000==0):
			print('x', end="", flush=True)
		elif (index%250==0):
			print('.', end="", flush=True)
		

rr_lyrae.write(output_file_name, format='ascii.csv')
