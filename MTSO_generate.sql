CREATE DATABASE  IF NOT EXISTS `MTSO` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `MTSO`;
-- MySQL dump 10.13  Distrib 5.6.13, for osx10.6 (i386)
--
-- Host: localhost    Database: MTSO
-- ------------------------------------------------------
-- Server version	5.7.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sdss_dr_12_v_1_0_2`
--

DROP TABLE IF EXISTS `sdss_dr_12_v_1_0_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sdss_dr_12_v_1_0_2` (
  `objID` bigint(8) NOT NULL COMMENT 'Unique SDSS identifier composed from [skyVersion,rerun,run,camcol,field,obj].',
  `ra` float NOT NULL COMMENT 'J2000 Right Ascension (r-band)',
  `decl` float NOT NULL COMMENT 'J2000 Declination (r-band)\n',
  `b` float NOT NULL COMMENT 'Galactic latitude\n',
  `l` float NOT NULL COMMENT 'Galactic Longitude',
  `psfMag_u` float NOT NULL COMMENT 'Point Spread Function Magnitude',
  `psfMag_g` float NOT NULL COMMENT 'Point Spread Function Magnitude',
  `psfMag_r` float NOT NULL COMMENT 'Point Spread Function Magnitude',
  `psfMag_i` float NOT NULL COMMENT 'Point Spread Function Magnitude',
  `psfMag_z` float NOT NULL COMMENT 'Point Spread Function Magnitude',
  `extinction_u` double NOT NULL COMMENT 'Extinction in u-band',
  `extinction_g` double NOT NULL COMMENT 'Extinction in g-band',
  `extinction_r` double NOT NULL COMMENT 'Extinction in r-band',
  `extinction_i` double NOT NULL COMMENT 'Extinction in i-band',
  `extinction_z` double NOT NULL COMMENT 'Extinction in z-band',
  PRIMARY KEY (`objID`),
  UNIQUE KEY `idsdss_dr_12_v_1_0_2_UNIQUE` (`objID`),
  KEY `b` (`b`),
  KEY `l` (`l`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
