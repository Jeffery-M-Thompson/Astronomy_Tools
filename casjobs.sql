/*
	This file is the sql statements used to extract Main Sequence Stars from the
	Sloan Digital Sky Server Data Release 12.
	
	The selection criteria is found in Cole, N. 2009 PhD Thesis - Maximum 
	Likelihood Fitting of Tidal Streams with Application to the Sagittarius
	Dwarf Tidal Tails
	
	The correction to the extinction values are based on the work of Schlafly
	and Finkbeiner 2011 - Measuring Reddening with Sloan Digital Sky Survey
	Stellar Spectra and Recalibrating SFD.
	The correction to the extinction comes from taking the new Rv 3.1 values
	from the Schlafly, Finkbeiner 2011 paper and dividing by the old Rv 3.1
	which can be found in the original EDR paper Table 22.
	The ratio of these two values is multiplied across the extinction value
	to give a corrected reddening value. 
	
	The data retrieved will still have the uncorrected extinction and any
	post data retrival processing will need to have the correction applied
	also before using the psfMag for any band.			
*/

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
  (flags & dbo.fPhotoFlags('EDGE')) = 0)))
  
/*
   Testing a new query to get better efficiency from the database.
   pushing all direct comparisions up in order.
   If CasJob times are still slow I will convert all between statements to direct comparisions.
*/

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
 
Select objid, ra, dec, l ,b, psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z, 
  extinction_u, extinction_g, extinction_r, extinction_i, extinction_z
  into mydb.MSTSouth_Neg_86_To_Neg_88 from star
  WHERE
    (b <= -86.0) and (b > -88.0) and 
    ((flags & dbo.fPhotoFlags('SATURATED')) = 0) and
    ((flags & dbo.fPhotoFlags('EDGE')) = 0) and
    ((psfmag_g -(@correction_g * extinction_g)) between 16.0 and 23.0) and
    ((psfmag_g -(@correction_g * extinction_g)) - (psfmag_r -(@correction_r * extinction_r)) between 0.1 and 0.3) and
    ((psfmag_u -(@correction_u * extinction_u)) - (psfmag_g -(@correction_g * extinction_g)) > 0.4)
