CREATE DATABASE  IF NOT EXISTS `58cmdb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `58cmdb`;
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (i386)
--
-- Host: 127.0.0.1    Database: 58cmdb
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `t_asset`
--

DROP TABLE IF EXISTS `t_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_asset` (
  `asset_id` bigint(20) NOT NULL,
  `asset_sn` varchar(45) DEFAULT NULL,
  `asset_is_device` tinyint(4) DEFAULT NULL,
  `asset_instock_time` datetime DEFAULT NULL,
  `asset_first_use_time` datetime DEFAULT NULL,
  `asset_outstock_time` datetime DEFAULT NULL,
  `asset_warranty_due_time` datetime DEFAULT NULL,
  `asset_receipt_time` datetime DEFAULT NULL,
  `asset_on_shelf_time` datetime DEFAULT NULL,
  `asset_off_shelf_time` datetime DEFAULT NULL,
  `asset_last_update_time` datetime DEFAULT NULL,
  `asset_status` tinyint(4) DEFAULT NULL,
  `asset_comment` text,
  `asset_position_id` bigint(20) DEFAULT NULL,
  `asset_device_type` tinyint(4) DEFAULT NULL,
  `order_item_id` bigint(20) DEFAULT NULL,
  `asset_ower_id` bigint(20) DEFAULT NULL,
  `asset_backup_ower_id` bigint(20) DEFAULT NULL,
  `asset_belong_org_id` bigint(20) DEFAULT NULL,
  `asset_operator_id` bigint(20) DEFAULT NULL,
  `asset_backup_operator_id` bigint(20) DEFAULT NULL,
  `asset_operator_org_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`asset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_asset`
--

LOCK TABLES `t_asset` WRITE;
/*!40000 ALTER TABLE `t_asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_device_producer_type`
--

DROP TABLE IF EXISTS `t_device_producer_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_device_producer_type` (
  `producer_id` bigint(20) NOT NULL,
  `producer_name` varchar(45) DEFAULT NULL,
  `device_type` varchar(45) DEFAULT NULL,
  `device_type_id` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`producer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_device_producer_type`
--

LOCK TABLES `t_device_producer_type` WRITE;
/*!40000 ALTER TABLE `t_device_producer_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_device_producer_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_inc_server_type`
--

DROP TABLE IF EXISTS `t_inc_server_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_inc_server_type` (
  `inc_server_type_id` bigint(20) NOT NULL,
  `inc_server_type_name` varchar(45) DEFAULT NULL,
  `inc_server_code` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`inc_server_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_inc_server_type`
--

LOCK TABLES `t_inc_server_type` WRITE;
/*!40000 ALTER TABLE `t_inc_server_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_inc_server_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_network_interface`
--

DROP TABLE IF EXISTS `t_network_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_network_interface` (
  `network_interface_id` bigint(20) NOT NULL,
  `server_id` bigint(20) DEFAULT NULL,
  `network_interface_name` varchar(45) DEFAULT NULL,
  `network_interface_type` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`network_interface_id`),
  KEY `fk_t_network_interface_1_idx` (`server_id`),
  CONSTRAINT `fk_t_network_interface_1` FOREIGN KEY (`server_id`) REFERENCES `t_server` (`server_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_network_interface`
--

LOCK TABLES `t_network_interface` WRITE;
/*!40000 ALTER TABLE `t_network_interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_network_interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_network_interface_config`
--

DROP TABLE IF EXISTS `t_network_interface_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_network_interface_config` (
  `network_interface_config_id` bigint(20) NOT NULL,
  `network_interface_id` bigint(20) DEFAULT NULL,
  `nic_port_id` bigint(20) DEFAULT NULL,
  `network_interface_tranfer_type` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`network_interface_config_id`),
  KEY `fk_t_network_interface_config_1_idx` (`network_interface_id`),
  CONSTRAINT `fk_t_network_interface_config_1` FOREIGN KEY (`network_interface_id`) REFERENCES `t_network_interface` (`network_interface_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_network_interface_config`
--

LOCK TABLES `t_network_interface_config` WRITE;
/*!40000 ALTER TABLE `t_network_interface_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_network_interface_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_network_interface_ip`
--

DROP TABLE IF EXISTS `t_network_interface_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_network_interface_ip` (
  `network_interface_ip_id` bigint(20) NOT NULL,
  `network_interface_id` bigint(20) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`network_interface_ip_id`),
  KEY `fk_t_network_interface_ip_1_idx` (`network_interface_id`),
  CONSTRAINT `fk_t_network_interface_ip_1` FOREIGN KEY (`network_interface_id`) REFERENCES `t_network_interface` (`network_interface_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_network_interface_ip`
--

LOCK TABLES `t_network_interface_ip` WRITE;
/*!40000 ALTER TABLE `t_network_interface_ip` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_network_interface_ip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_os_type`
--

DROP TABLE IF EXISTS `t_os_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_os_type` (
  `os_type_id` bigint(20) NOT NULL,
  `os_type_name` varchar(45) DEFAULT NULL,
  `os_type_version` varchar(45) DEFAULT NULL,
  `os_full_name` varchar(45) DEFAULT NULL,
  `os_default_version` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`os_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_os_type`
--

LOCK TABLES `t_os_type` WRITE;
/*!40000 ALTER TABLE `t_os_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_os_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_selection_version`
--

DROP TABLE IF EXISTS `t_selection_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_selection_version` (
  `server_selection_version_id` bigint(20) NOT NULL,
  `server_selection_version_start_time` datetime DEFAULT NULL,
  `server_selection_version_end_time` datetime DEFAULT NULL,
  `server_selection_version_author_id` bigint(20) DEFAULT NULL,
  `server_selection_versionnumber` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`server_selection_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_selection_version`
--

LOCK TABLES `t_selection_version` WRITE;
/*!40000 ALTER TABLE `t_selection_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_selection_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_selection_version_record`
--

DROP TABLE IF EXISTS `t_selection_version_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_selection_version_record` (
  `server_selection_version_record_id` bigint(20) NOT NULL,
  `server_selection_version_id` bigint(20) DEFAULT NULL,
  `server_selection_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_selection_version_record_id`),
  KEY `fk_t_selection_version_record_1_idx` (`server_selection_version_id`),
  KEY `fk_t_selection_version_record_2_idx` (`server_selection_id`),
  CONSTRAINT `fk_t_selection_version_record_1` FOREIGN KEY (`server_selection_version_id`) REFERENCES `t_selection_version` (`server_selection_version_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_selection_version_record_2` FOREIGN KEY (`server_selection_id`) REFERENCES `t_server_selection` (`server_selection_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_selection_version_record`
--

LOCK TABLES `t_selection_version_record` WRITE;
/*!40000 ALTER TABLE `t_selection_version_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_selection_version_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_server`
--

DROP TABLE IF EXISTS `t_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_server` (
  `server_id` bigint(20) NOT NULL,
  `asset_id` bigint(20) DEFAULT NULL,
  `inc_server_type_id` bigint(20) DEFAULT NULL,
  `server_comment` text,
  `server_bios_os` varchar(45) DEFAULT NULL,
  `server_device_type_id` bigint(20) DEFAULT NULL,
  `server_status` tinyint(4) DEFAULT NULL,
  `server_bmc` varchar(45) DEFAULT NULL,
  `server_host_name` varchar(45) DEFAULT NULL,
  `os_type_id` bigint(20) DEFAULT NULL,
  `server_kernel_version` varchar(45) DEFAULT NULL,
  `server_ads_status` tinyint(4) DEFAULT NULL,
  `server_ads_check_time` datetime DEFAULT NULL,
  `server_ads_installed` tinyint(4) DEFAULT NULL,
  `server_ads_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`server_id`),
  KEY `fk_t_server_1_idx` (`asset_id`),
  KEY `fk_t_server_2_idx` (`inc_server_type_id`),
  KEY `fk_t_server_3_idx` (`server_device_type_id`),
  KEY `fk_t_server_4_idx` (`os_type_id`),
  CONSTRAINT `fk_t_server_1` FOREIGN KEY (`asset_id`) REFERENCES `t_asset` (`asset_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_server_2` FOREIGN KEY (`inc_server_type_id`) REFERENCES `t_inc_server_type` (`inc_server_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_server_3` FOREIGN KEY (`server_device_type_id`) REFERENCES `t_server_device_type` (`server_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_server_4` FOREIGN KEY (`os_type_id`) REFERENCES `t_os_type` (`os_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_server`
--

LOCK TABLES `t_server` WRITE;
/*!40000 ALTER TABLE `t_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_server_device_type`
--

DROP TABLE IF EXISTS `t_server_device_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_server_device_type` (
  `server_type_id` bigint(20) NOT NULL,
  `device_producer_type_id` bigint(20) DEFAULT NULL,
  `server_device_type_name` varchar(45) DEFAULT NULL,
  `server_hight` int(11) DEFAULT NULL,
  `server_width` int(11) DEFAULT NULL,
  `server_depth` int(11) DEFAULT NULL,
  `server_electricity` varchar(45) DEFAULT NULL,
  `server_weight` int(11) DEFAULT NULL,
  `server_score` varchar(45) DEFAULT NULL,
  `server_minios` varchar(45) DEFAULT NULL,
  `server_max_power` int(11) DEFAULT NULL,
  `server_rated_power` int(11) DEFAULT NULL,
  `server_power_type` varchar(45) DEFAULT NULL,
  `server_mother_board_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_type_id`),
  KEY `fk_t_server_device_type_1_idx` (`device_producer_type_id`),
  CONSTRAINT `fk_t_server_device_type_1` FOREIGN KEY (`device_producer_type_id`) REFERENCES `t_device_producer_type` (`producer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_server_device_type`
--

LOCK TABLES `t_server_device_type` WRITE;
/*!40000 ALTER TABLE `t_server_device_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_server_device_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_server_selection`
--

DROP TABLE IF EXISTS `t_server_selection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_server_selection` (
  `server_selection_id` bigint(20) NOT NULL,
  `inc_server_type_id` bigint(20) DEFAULT NULL,
  `server_device_type_id` bigint(20) DEFAULT NULL,
  `device_producer_id` bigint(20) DEFAULT NULL,
  `server_selection_datetime` datetime DEFAULT NULL,
  `server_device_ablity_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_selection_id`),
  KEY `fk_t_server_selection_1_idx` (`inc_server_type_id`),
  KEY `fk_t_server_selection_2_idx` (`server_device_type_id`),
  KEY `fk_t_server_selection_3_idx` (`device_producer_id`),
  CONSTRAINT `fk_t_server_selection_3` FOREIGN KEY (`device_producer_id`) REFERENCES `t_device_producer_type` (`producer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_server_selection_1` FOREIGN KEY (`inc_server_type_id`) REFERENCES `t_inc_server_type` (`inc_server_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_server_selection_2` FOREIGN KEY (`server_device_type_id`) REFERENCES `t_server_device_type` (`server_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_server_selection`
--

LOCK TABLES `t_server_selection` WRITE;
/*!40000 ALTER TABLE `t_server_selection` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_server_selection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_slot`
--

DROP TABLE IF EXISTS `t_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_slot` (
  `slot_id` bigint(20) NOT NULL,
  `access_id` bigint(20) DEFAULT NULL,
  `slot_type_id` bigint(20) DEFAULT NULL,
  `slot_face_direction` tinyint(4) DEFAULT NULL,
  `insert_accessory_id` bigint(20) DEFAULT NULL,
  `slot_num` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`slot_id`),
  KEY `fk_t_slot_1_idx` (`access_id`),
  KEY `fk_t_slot_2_idx` (`slot_type_id`),
  CONSTRAINT `fk_t_slot_2` FOREIGN KEY (`slot_type_id`) REFERENCES `t_slot_type` (`slot_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_slot_1` FOREIGN KEY (`access_id`) REFERENCES `t_asset` (`asset_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_slot`
--

LOCK TABLES `t_slot` WRITE;
/*!40000 ALTER TABLE `t_slot` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_slot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_slot_type`
--

DROP TABLE IF EXISTS `t_slot_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_slot_type` (
  `slot_type_id` bigint(20) NOT NULL,
  `slot_type_name` varchar(45) DEFAULT NULL,
  `slot_spec` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`slot_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_slot_type`
--

LOCK TABLES `t_slot_type` WRITE;
/*!40000 ALTER TABLE `t_slot_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_slot_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-10 15:09:36
