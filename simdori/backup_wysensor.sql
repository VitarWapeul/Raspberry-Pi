-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: wysensor
-- ------------------------------------------------------
-- Server version	10.3.27-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `WySensor_TLV`
--

DROP TABLE IF EXISTS `WySensor_TLV`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WySensor_TLV` (
  `tlv_index` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime(2) NOT NULL,
  `mac` varchar(17) NOT NULL,
  `MagicNumber` varchar(16) NOT NULL,
  `version` varchar(8) NOT NULL,
  `TotalPacketLen` varchar(8) NOT NULL,
  `platform` varchar(8) NOT NULL,
  `fameNumber` varchar(8) NOT NULL,
  `timeCpuCycle` varchar(8) NOT NULL,
  `numDetectedObj` varchar(8) NOT NULL,
  `numTLVs` varchar(8) NOT NULL,
  `subFrameNumber` varchar(8) NOT NULL,
  `TLV1type` varchar(8) NOT NULL,
  `TLV1length` varchar(8) NOT NULL,
  `rangeBinIndexMax` varchar(4) NOT NULL,
  `rangeBinIndexPhase` varchar(4) NOT NULL,
  `maxVal` varchar(8) NOT NULL,
  `processingCyclesOut` varchar(8) NOT NULL,
  `rangeBinStratIndex` varchar(4) NOT NULL,
  `rangeBinEndIndex` varchar(4) NOT NULL,
  `unwrapPhasePeak_mm` varchar(8) NOT NULL,
  `outputFilterBreathOut` varchar(8) NOT NULL,
  `outputFilterHreatOut` varchar(8) NOT NULL,
  `heartRateEst_FFT` varchar(8) NOT NULL,
  `heartRateEst_FFT_4hz` varchar(8) NOT NULL,
  `heartRateEst_xCorr` varchar(8) NOT NULL,
  `heartReatEst_peakCount` varchar(8) NOT NULL,
  `breathingRateEst_FFT` varchar(8) NOT NULL,
  `breathingRateEst_xCorr` varchar(8) NOT NULL,
  `breathingRateEst_peakCount` varchar(8) NOT NULL,
  `confidenceMetricBreathOut` varchar(8) NOT NULL,
  `confidenceMetricBreathOut_xCorr` varchar(8) NOT NULL,
  `confidenceMetricHeartOut` varchar(8) NOT NULL,
  `confidenceMetricHeartOut_4Hz` varchar(8) NOT NULL,
  `confidenceMetricHeartOut_xCorr` varchar(8) NOT NULL,
  `sumEnergyBreathWfm` varchar(8) NOT NULL,
  `sumEnergyHeartWfm` varchar(8) NOT NULL,
  `motionDetectedFlag` varchar(8) NOT NULL,
  `BreathingRate_HarmEnergy` varchar(8) NOT NULL,
  `HeartRate_HarmEnergy` varchar(8) NOT NULL,
  `reserved1` varchar(8) NOT NULL,
  `reserved2` varchar(8) NOT NULL,
  `reserved3` varchar(8) NOT NULL,
  `reserved4` varchar(8) NOT NULL,
  `reserved5` varchar(8) NOT NULL,
  `reserved6` varchar(8) NOT NULL,
  `reserved7` varchar(8) NOT NULL,
  `reserved8` varchar(8) NOT NULL,
  `TLV2type` varchar(8) NOT NULL,
  `TLV2length` varchar(8) NOT NULL,
  `RangeProfile` text NOT NULL,
  PRIMARY KEY (`tlv_index`)
) ENGINE=InnoDB AUTO_INCREMENT=1662274 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-18 16:59:57
