#!/usr/bin/env python3

import astropy as astro
import math as ma
import numpy as np
from numpy import linalg as LA
import scipy as sc
import matplotlib
#matplotlib.use('PS')
import matplotlib.pyplot as plt
import os
import sys
import csv

""" Code from Matt Newby's astro_coordinates updated by Jeff Thompson to
with python3 and astropy """

""" This is a translation of stCoords.c and atSurveyGeometry.c from the
Milkyway@home code.  
-Matthew Newby, RPI, Jun 15, 2011"""

deg = 180.0 / ma.pi 
rad = ma.pi / 180.0 
surveyCenterRa = 185.0
surveyCenterDec = 32.5
raGP = 192.8594813 * rad
decGP = 27.1282511 * rad
lCP = 122.932 * rad #123.932
arr = sc.array([0.0])
dsun = 8.5

""" All systems should be accurate to within 1 arcsecond, 1/3600 degree = 0.000278 """

""" !!!  There may be lingering 'type' issues... !!! """

def EqToGC (ra_deg, dec_deg, wedge):  #produces lists...  anglebounds2!!!
    """ Converts equatorial ra,dec into Great Circle mu, nu; 'atSurveyGeometry.c' in
    m31.phys.rpi.edu:/p/prd/astrotools/v5_18/Linux-2-4-2-3-2/src"""
    node = (surveyCenterRa - 90.0)*rad
    eta = get_eta(wedge)
    inc = (surveyCenterDec + eta)*rad
    ra, dec = (ra_deg*rad), (dec_deg*rad)
    # Rotation
    x1 = sc.cos(ra-node)*sc.cos(dec)
    y1 = sc.sin(ra-node)*sc.cos(dec)
    z1 = sc.sin(dec)
    x2 = x1
    y2 = y1*sc.cos(inc) + z1*sc.sin(inc)
    z2 = -y1*sc.sin(inc) + z1*sc.cos(inc)
    mu = sc.arctan2(y2,x2) + node
    nu = sc.arcsin(z2)
    nu, mu = angle_bounds2((nu*deg), (mu*deg))
    return mu,nu
    
def GCToEq (mu_deg, nu_deg, wedge):  # produces lists....
    """ Converts Stripe mu, nu into equatorial ra, dec.  Called 'atGCToEq' in at SurveyGeometry.c"""
    node = (surveyCenterRa - 90.0)*rad
    eta = get_eta(wedge)
    inc = (surveyCenterDec + eta)*rad
    mu, nu = (mu_deg*rad), (nu_deg*rad)
    # Rotation
    x2 = sc.cos(mu - node)*sc.cos(nu)
    y2 = sc.sin(mu - node)*sc.cos(nu)
    z2 = sc.sin(nu)
    x1 = x2
    y1 = y2*sc.cos(inc) - z2*sc.sin(inc)
    z1 = y2*sc.sin(inc) + z2*sc.cos(inc)
    ra = sc.arctan2(y1,x1) + node
    dec = sc.arcsin(z1)
    dec, ra = angle_bounds2((dec*deg),(ra*deg))
    return ra, dec

def EqTolb (ra_deg, dec_deg):
    """ Converts equatorial ra, dec, into galactic l,b;  from Binney and Merrifield, p. 31
    following the method of http://star-www.st-and.ac.uk/~spd3/Teaching/AS3013/programs/radec2lb.f90
    NOT QUITE - I use arctan2 method instead"""
    ra, dec = (ra_deg*rad), (dec_deg*rad)
    # Conversion Code
    r = (ra - raGP)
    b = sc.arcsin( sc.sin(decGP)*sc.sin(dec) + sc.cos(decGP)*sc.cos(dec)*sc.cos(r) )
    t = sc.arctan2((sc.cos(dec)*sc.sin(r)),
                   (sc.cos(decGP)*sc.sin(dec) - sc.sin(decGP)*sc.cos(dec)*sc.cos(r)) )
    l = (lCP - t)
    b, l = angle_bounds2((b*deg), (l*deg))
    return l, b
    
def lbToEq (l_deg, b_deg):   
    """ Converts galactic l,b in to Equatorial ra, dec; from Binney and Merrifield, p. 31;  
    l, b must be arrays of same shape"""
    l, b = (l_deg*rad), (b_deg*rad)
    # Conversion Code
    t = lCP - l
    dec = sc.arcsin(sc.sin(decGP)*sc.sin(b) + sc.cos(decGP)*sc.cos(b)*sc.cos(t) )
    r = sc.arctan2( (sc.cos(b)*sc.sin(t)),
                    ( (sc.cos(decGP)*sc.sin(b)) - (sc.sin(decGP)*sc.cos(b)*sc.cos(t)))  )
    if type(r) != type(arr):  r = sc.array([r])
    for i in range(len(r)):
        r[i] = angle_bounds((r[i] + raGP)*deg)
    return r, (dec*deg)

def lbr2xyz (l, b, r, d0=dsun):
    """ convert sun-centered l,b,r into galactic x,y,z coordinates; derived from stCoords.c"""
    bsin = sc.sin(b * rad)
    lsin = sc.sin(l * rad)
    bcos = sc.cos(b * rad)
    lcos = sc.cos(l * rad)
    z = r*bsin
    zp = r*bcos
    d = sc.sqrt((d0*d0) + (zp*zp) - (2*d0*zp*lcos))  #law of cosines
    x = ((zp*zp) - (d0*d0) - (d*d)) / (2.0*d0)  #law of cosines combined with x= -d*cos(theta)
    y = zp*lsin
    return x,y,z

def xyz2lbr (x, y, z, d0=dsun):
    """ convert galactic xyz into sun-centered lbr coordinates; derived from stCoords.c"""
    #if len(xyz.shape) > 1:  x, y, z = xyz[:,0], xyz[:,1], xyz[:,2]
    #else:                   x, y, z = xyz[0], xyz[1], xyz[2]
    xsun = x + d0
    temp = (xsun*xsun) + (y*y)
    l = sc.arctan2(y, xsun) * deg
    b = sc.arctan2(z, sc.sqrt(temp)) * deg
    r = sc.sqrt(temp + (z*z))
    if type(l) == type(arr):
        for i in range(len(l)):
            if l[i] < 0.0:  l[i] = l[i] + 360.0
    else:
        if l < 0.0:  l = l + 360.0
    return l,b,r
    
def stream2xyz (u, v, w, mu, r, theta, phi, wedge, nu=0.0):
    """ Converts to galactic x,y,z from custom stream coordinates u,v,w;
    ACCEPTS ONLY 1 POINT AT A TIME - don't know what will happen if arrays are passed in
    stream is aligned along w-axis;  rotation is theta about y-axis, then phi about z-axis
    (See Nathan Cole's thesis, page 17)"""
    theta, phi = (theta*rad), (phi*rad)
    # Get uvw origin in xyz
    ra, dec = GCToEq(mu, nu, wedge)
    l, b = EqTolb(ra, dec)
    xyz0 = lbr2xyz(l,b,r)
    # Rotate uvw into xyz
    R_M = sc.matrix([
        [(sc.cos(phi)*sc.cos(theta)), (-1.0*sc.sin(phi)), (sc.cos(phi)*sc.sin(theta))],
        [(sc.sin(phi)*sc.cos(theta)),  (sc.cos(phi)),     (sc.sin(phi)*sc.sin(theta))],
        [(-1.0*sc.sin(theta)),         (0.0),             (sc.cos(theta))]
        ])
    """R_inv = sc.matrix([
        [(sc.sin(theta)*sc.cos(phi)), (-1.0*sc.sin(theta)*sc.sin(phi)), (-1.0*sc.cos(theta))],
        [(sc.sin(phi)),               (sc.cos(phi)),                    (0.0)],
        [(sc.cos(theta)*sc.cos(phi)), (-1.0*sc.cos(theta)*sc.sin(phi)), (sc.sin(theta))]
        ])  OLD CRAP"""
    uvw_M = sc.matrix([u,v,w])
    xyz_M = R_M*uvw_M.T
    xyzR = sc.array(xyz_M)
    # Translate rotated values
    x = xyzR[0] + xyz0[0]
    y = xyzR[1] + xyz0[1]
    z = xyzR[2] + xyz0[2]
    return x[0],y[0],z[0]

def xyz2longlat(x,y,z):
    """ converts cartesian x,y,z coordinates into spherical longitude and latitude """
    r = sc.sqrt(x*x + y*y + z*z)
    long = sc.arctan2(y,x)
    d = sc.sqrt(x*x + y*y)
    lat = sc.arcsin(z/r)
    return long*deg, lat*deg, r
    
def longlat2xyz(long,lat,r=1.0):
    """ converts spherical longitude and latitude into cartesian x,y,z """
    x = r*sc.cos(long*rad)*sc.cos(lat*rad)
    y = r*sc.sin(long*rad)*sc.cos(lat*rad)
    z = r*sc.sin(lat*rad)
    return x,y,z

def xyz2plane(x,y,z, new_x=[], plane=[], origin=None):
    """ Converts galactic x,y,z into orbital plane x,y,z
        new_x is the x,y,z coordinates of new x-axis
        plane is a,b,c,d plane parameters: ax + by + cz + d = 0
        origin is x offset, use d_sun for sun-centered inputs"""
    # preliminary stuff
    if origin != None:  x = x - origin
    a,b,c,d = plane
    bottom = np.sqrt(a*a + b*b + c*c)  # normalize
    a,b,c,d = a/bottom, b/bottom, c/bottom, d/bottom
    px, py, pz = new_x
    bot = np.sqrt(px*px + py*py + pz*pz)  #normalize
    px, py, pz = px/bot, py/bot, pz/bot
    p0 = [px,py,pz]
    # do rotation
    z_hat = [a,b,c]
    y_hat = cross(z_hat, p0)
    x_hat = cross(y_hat, z_hat)
    if type(x)==type(arr) or type(x)==type([]):
        xp, yp, zp = [], [], []
        for i in range(len(x)):
            xp.append(dot([x[i],y[i],z[i]], x_hat))
            yp.append(dot([x[i],y[i],z[i]], y_hat))
            zp.append(dot([x[i],y[i],z[i]], z_hat))
    else:
        xp = dot([x,y,z], x_hat)
        yp = dot([x,y,z], y_hat)
        zp = dot([x,y,z], z_hat)
    return xp, yp, zp

def rot_3D(x,y,z, rot="z", angles=[ma.pi]):
    """ Rotates a set of vectors by any number of Euler angles.
        rot is a string of x's, y's and z's describing the order of rotations, left-to-right,
        while angles is the corresponding angle (in radians) for each rotation"""
    # Build rotation matrix
    R = sc.identity(3)
    for i in range(len(angles)):
        t = angles[i]
        if rot[i] == "x":   Rx = Rot_x(t);  R = Rx*R;  continue
        elif rot[i] == "y": Ry = Rot_y(t);  R = Ry*R;  continue
        elif rot[i] == "z": Rz = Rot_z(t);  R = Rz*R;  continue
        else:  print ("!!! - Invalid rotation axis, {0}").format(rot(i))
    # Now do the rotations
    if type(x) != type(sc.zeros(1)):
        out = R*sc.matrix([ [x],[y],[z] ])
        x, y, z = float(out[0]), float(out[1]), float(out[2])
    else:
        for i in range(len(x)):
            out = R*sc.matrix([ [x[i]],[y[i]],[z[i]] ])
            x[i], y[i], z[i] = float(out[0]), float(out[1]), float(out[2])
    return x, y, z


def inv_rot_3D(x,y,z, rot="z", angles=[ma.pi]):
    """ Rotates a set of vectors by any number of Euler angles, in the reverse direction.
        input is as rot_3D, using the inverse order for rotations and angles, but leaving
        the angles un-flipped - the matrix inverses will take care of that.
        rot is a string of x's, y's and z's describing the order of rotations, left-to-right,
        while angles is the corresponding angle (in radians) for each rotation"""
    # Build rotation matrix
    R = sc.identity(3)
    for i in range(len(angles)):
        t = angles[i]
        if rot[i] == "x":   Rx = LA.inv(Rot_x(t));  R = Rx*R;  continue
        elif rot[i] == "y": Ry = LA.inv(Rot_y(t));  R = Ry*R;  continue
        elif rot[i] == "z": Rz = LA.inv(Rot_z(t));  R = Rz*R;  continue
        else:  print ("!!! - Invalid rotation axis, {0}").format(rot(i))
    # Now do the rotations
    if type(x) != type(sc.zeros(1)):
        out = R*sc.matrix([ [x],[y],[z] ])
        x, y, z = float(out[0]), float(out[1]), float(out[2])
    else:
        for i in range(len(x)):
            out = R*sc.matrix([ [x[i]],[y[i]],[z[i]] ])
            x[i], y[i], z[i] = float(out[0]), float(out[1]), float(out[2])
    return x, y, z
    """ MAYBE MAKE THIS ONE TAKE SAME INPUTS AS rot_3D TO MAKE THINGS EASIER """


""" ------------------ Higher-order transforms ------------------ """

def GC2xyz(mu, nu, r, wedge):
    ra, dec = GCToEq(mu, nu, wedge)
    l, b = EqTolb(ra, dec)
    return lbr2xyz(l,b,r)

def GC2lbr(mu, nu, r, wedge):
    ra, dec = GCToEq(mu, nu, wedge)
    l, b = EqTolb(ra, dec)
    return l,b,r

def lb2GC(l, b, wedge):
    ra, dec = lbToEq(l, b)
    return EqToGC(ra, dec, wedge)
    
def lb2sgr(l,b,r):
    x,y,z = lbr2xyz(l,b,r)
    return law_xyz2sgr(x,y,z)
    
def streamToGC(u,v,w, mu,r,theta,phi,wedge):
    x,y,z = stream2xyz(u,v,w, mu,r,theta,phi,wedge)
    l,b,r1 = xyz2lbr(x,y,z)
    ra, dec = lbToEq(l,b)
    mu, nu = EqToGC(ra, dec, wedge)
    return mu, nu, r1

def xyz2lambeta(x,y,z, new_x=[], plane=[], origin=None, verbose=1):
    x,y,z = xyz2plane(x,y,z, new_x, plane, origin, verbose)
    lam, beta, r = xyz2longlat(x,y,z)
    if type(lam)==type(arr):
        for i in range(len(lam)):
            if lam[i] < 0.0:  lam[i] = lam[i] + 360.0
    else:  
        if lam < 0.0:  lam = lam + 360.0
    return lam, beta, r

def lambeta2xyz(lam, beta, r, center=[], plane=[], origin=None):
    x1, y1, z1 = longlat2xyz(lam, beta, r)
    return plane2xyz(x1, y1, z1, center, plane, origin)
    
def lambeta2lbr(lam, beta, r, center=[], plane=[], origin=None):
    x1, y1, z1 = longlat2xyz(lam, beta, r)
    x, y, z = plane2xyz(x1, y1, z1, center, plane, origin)
    return xyz2lbr(x,y,z)


""" ------------------ Utilities ------------------ """

def cross(a, b):
    """ returns the cross-product of two 3-vectors"""
    c1 = a[1]*b[2] - a[2]*b[1]
    c2 = a[2]*b[0] - a[0]*b[2]
    c3 = a[0]*b[1] - a[1]*b[0]
    return sc.array([c1,c2,c3])

def dot(a, b):
    """ returns the dot product of two 3-vectors"""
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def get_eta (wedge):
    """ Get the eta value that corresponds to the given stripe value """  #wedge_eta?
    ss = 2.5
    if wedge <= 46:  eta = wedge * ss - 57.5
    else:  eta = wedge * ss - 57.5 - 180.0
    return eta
    
def angle_bounds (angle, min=0.0, max=360.0):
    """ Keeps an angle, in degrees, in a 360 degree region"""
    while angle < min:  angle = angle + 360.0
    while angle > max:  angle = angle - 360.0
    return angle

def angle_bounds2 (theta, phi):
    """ Sets two spherical angles in bounds, -90<theta<90; 0<phi<360"""
    if type(theta) != type(arr):  theta = sc.array([theta])
    if type(phi) != type(arr):  phi = sc.array([phi])
    for i in range(len(theta)):
        theta[i] = angle_bounds(theta[i], -180.0, 180.0)
    for i in range(len(theta)):
        if sc.fabs(theta[i]) > 90.0:
            theta[i] = 180.0 - theta[i]
            phi[i] = phi[i] + 180.0
    for i in range(len(theta)):
        theta[i] = angle_bounds(theta[i], -180.0, 180.0)
        phi[i] = angle_bounds(phi[i], 0.0, 360.0)
    for i in range(len(theta)):
        if (sc.fabs(theta[i]) == 90.0):  phi[i] = 0.0
    if len(theta)==1:
        theta, phi = theta[0], phi[0]
    return theta, phi

def angle_bounds3 (theta, phi, phi_max=360.0):
    """ Sets two spherical angles in bounds, 0<theta<180; (phi_max-360.0)<phi<phi_max"""
    phi_min = phi_max-360.0
    if type(theta) != type(arr):  theta = sc.array([theta])
    if type(phi) != type(arr):  phi = sc.array([phi])
    for i in range(len(theta)):
        theta[i] = angle_bounds(theta[i], -180.0, 180.0)
    for i in range(len(theta)):
        if theta[i] < 0.0:
            theta[i] = -1.0*theta[i]
            phi[i] = phi[i] + 180.0
    for i in range(len(theta)):
        theta[i] = angle_bounds(theta[i], -180.0, 180.0)
        phi[i] = angle_bounds(phi[i], phi_min, phi_max)
    for i in range(len(theta)):
        if (sc.fabs(theta[i]) == 180.0):  phi[i] = 0.0
    if len(theta)==1:
        theta, phi = theta[0], phi[0]
    return theta, phi

def get_angle (sin_in, cos_in):
    """ Just use arctan2 - much more efficient"""
    if (sin_in >= 0.0 and cos_in >= 0.0):     out = sc.arcsin(sin_in)
    elif (sin_in >= 0.0 and cos_in < 0.0):    out = ma.pi-sc.arcsin(sin_in)
    elif (sin_in < 0.0 and cos_in < 0.0):     out = ma.pi-sc.arcsin(sin_in)
    elif (sin_in < 0.0 and cos_in >= 0.0):    out = 2.0*ma.pi + sc.arcsin(sin_in)
    else: out = float('nan')
    return out

def stripe_normal (wedge):
    """ Get normal vector of data slice from stripe number """
    eta = get_eta(wedge)
    ra, dec = GCToEq(0, (90.0+eta), wedge)
    l, b = EqTolb(ra, dec)
    x, y, z = lbr2xyz(l, b, 1.0)
    return x+dsun, y, z

def normalize_vector(vec):
    """normalize and return a vector; also scales any additional components of the list"""
    a, b, c = vec[0], vec[1], vec[2]
    bottom = sc.sqrt(a*a + b*b + c*c)
    V = []
    for v in vec:  V.append(v/bottom)
    return V

def getr (g, M=4.2):
    """converts a magnitude into a distance (kpc)"""
    return ( ( 10.**( (g-M)/5. ) )/ 100. )

def getg (r, M=4.2):
    """converts a distance (kpc) into a magnitude"""
    return M + 5.*(sc.log10(r*1000) - 1.)

def getM (g, d):
    """converts an apparent magnitude to absolute magnitude, given the distance"""
    return g - 5.*(sc.log10(d*1000) - 1.)

def raDeg (raHr, raMin, raSec, dec=0.0):  # Make this one better
    """#changes ra from time units to degrees, dec in degrees"""
    raTime = raHr + (raMin/60.0) + (raSec/3600.0)
    newra = raTime*(15.0)*(sc.cos(sc.radians(dec)) )
    #should be dec != 0.0?  Works if dec =0.0...
    #15.0 = (360 degrees)/(24 hours)
    #print 'converted ra, in degrees:'
    return newra

def check (expected, test):
    arcsec = 1.0 / 3600.0
    if (expected - test) < arcsec:  return "YES - total error: "+str((expected - test)*3600.0)+" arcseconds"
    else:  return "NO - test Failed: "+str((expected - test)*3600.0)+" arcseconds"


""" ------------------ Rotation Matrices ------------------ """

def Rot_x(t):
    return  sc.matrix([ [1.0,  0.0,                   0.0],
                        [0.0,  sc.cos(t),  -1.0*sc.sin(t)],
                        [0.0,  sc.sin(t),       sc.cos(t)]  ])

def Rot_y(t):
    return  sc.matrix([ [sc.cos(t),      0.0,  sc.sin(t)],
                        [0.0,            1.0,        0.0],
                        [-1.0*sc.sin(t), 0.0,  sc.cos(t)]  ])
    
def Rot_z(t):
    return  sc.matrix([ [sc.cos(t),  -1.0*sc.sin(t),  0.0],
                        [sc.sin(t),  sc.cos(t),       0.0],
                        [0.0,        0.0,             1.0]  ])
    

""" ------------------ Help Information ------------------ """

def help():
    return -1

# static variable to data inputs and outputs

INPUT_DATAFILE = sys.argv[1]
OUT_PATH = sys.argv[2]
START = int(sys.argv[3])
END = int(sys.argv[4]) + 1
CUTS = sys.argv[5]
correction = float(3.303/3.793)
size = START - END
cut = [([0]*2) for i in range(START, END)]

for wedge in range(START, END):
	with open(CUTS) as cutfile:
		reader = csv.DictReader(cutfile)
		for row in reader:
			file_wedge = int(row['Wedge'])
			start = float(row['Start'])
			end = float(row['End'])
			if(file_wedge == wedge):
				cut[wedge-START] = [start, end]

# Create Filehandle for output
# Wedge range 60 - 100
# Bit Flags for Accepted
#  mu nu g

for wedge in range(START, END):
    OUTPUT_DATAFILE1 = "{0}/{1}_mu_nu_r.star".format(OUT_PATH, wedge) 
    OUTPUT_DATAFILE2 = "{0}/{1}_l_b_r.star".format(OUT_PATH, wedge)
    OUTPUT_DATAFILE3 = "{0}/{1}_ra_dec_r.star".format(OUT_PATH, wedge)
    with open (OUTPUT_DATAFILE1, 'w') as fileout1, open (OUTPUT_DATAFILE2, 'w') as fileout2, open (OUTPUT_DATAFILE3, 'w') as fileout3:
    #fileout1 = open(OUTPUT_DATAFILE1, 'wb')
    #fileout2 = open(OUTPUT_DATAFILE2, 'wb')
    	row_out1 = csv.writer(fileout1, delimiter =' ')
    	row_out2 = csv.writer(fileout2, delimiter =' ')
    	row_out3 = csv.writer(fileout3, delimiter =' ')
    	with open(INPUT_DATAFILE) as DATAFILE:
        	dictionary = csv.DictReader(DATAFILE)
        	for row in dictionary:
        		l = float(row['l'])
        		b = float(row['b'])
        		ra = float(row['ra'])
        		dec = float(row['dec'])
        		#psfMag_g = float(row['psfMag_g'])
        		#extnct_g = float(row['extinction_g'])
        		#g = float(psfMag_g - (extnct_g * correction))
        		g = float(row['dered_g'])
        		r = getr(g)
        		mu, nu = lb2GC(l, b, wedge)
        		start = cut[wedge-START][0]
        		end = cut[wedge-START][1]
        		accepted = 0
        		if (abs(nu) <= 1.25):
        			accepted = accepted | 1
        		if (g <= 22.50):
        			accepted = accepted | 2
        		if (start >= 0.0):
        			if (mu >= start and mu <= end):
        				accepted = accepted | 4
        		else:
        			if ((mu >=(start+360) and mu <= 360) or (mu >=0 and mu <=end)):
        				accepted = accepted | 4
        		if (accepted == 7):
        			print ("ACCPETED in Wedge {3}:\tmu\t\tnu \t\tr\n                     \t{0}\t{1}\t{2}".format(mu, nu, r, wedge))
        			print ("                      \tl  \t\tb \t\tr\n                     \t{0}\t{1}\t{2}".format(l, b, r, wedge))
        			row_out1.writerow([mu, nu, r])
        			row_out2.writerow([l, b, r])
        			row_out3.writerow([ra, dec, r])
    print ("WEDGE {0} COMPLETED".format(wedge))
