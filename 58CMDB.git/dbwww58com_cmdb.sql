-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: dep_cmdb
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
-- Table structure for table `accessory_taccessory`
--

DROP TABLE IF EXISTS `accessory_taccessory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_taccessory` (
  `accessory_id` bigint(20) NOT NULL,
  `accessory_status` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `sn` int(11) DEFAULT NULL,
  `enable_time` datetime DEFAULT NULL,
  `due_time` datetime DEFAULT NULL,
  `brand` varchar(45) NOT NULL,
  `accessory_type_id` bigint(20) NOT NULL,
  `asset_id_id` bigint(20) DEFAULT NULL,
  `idc_id_id` bigint(20) DEFAULT NULL,
  `store_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`),
  KEY `accessory_taccessory_cdb0e412` (`accessory_type_id`),
  KEY `accessory_taccessory_51c6d5db` (`asset_id_id`),
  KEY `accessory_taccessory_cd352ef9` (`idc_id_id`),
  KEY `accessory_taccessory_7473547c` (`store_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_taccessory`
--

LOCK TABLES `accessory_taccessory` WRITE;
/*!40000 ALTER TABLE `accessory_taccessory` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_taccessory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_taccessorybrand`
--

DROP TABLE IF EXISTS `accessory_taccessorybrand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_taccessorybrand` (
  `brand_id` bigint(20) NOT NULL,
  `brand_name` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`brand_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_taccessorybrand`
--

LOCK TABLES `accessory_taccessorybrand` WRITE;
/*!40000 ALTER TABLE `accessory_taccessorybrand` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_taccessorybrand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_taccessorystore`
--

DROP TABLE IF EXISTS `accessory_taccessorystore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_taccessorystore` (
  `accessory_store_id` bigint(20) NOT NULL,
  `accessory_store_name` varchar(45) NOT NULL,
  `accessory_store_position` varchar(45) NOT NULL,
  `accessory_store_owner` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `accessory_idc_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`accessory_store_id`),
  KEY `accessory_taccessorystore_1917dc42` (`accessory_idc_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_taccessorystore`
--

LOCK TABLES `accessory_taccessorystore` WRITE;
/*!40000 ALTER TABLE `accessory_taccessorystore` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_taccessorystore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_taccessorytype`
--

DROP TABLE IF EXISTS `accessory_taccessorytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_taccessorytype` (
  `accessory_type_id` bigint(20) NOT NULL,
  `accessory_type_name` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_taccessorytype`
--

LOCK TABLES `accessory_taccessorytype` WRITE;
/*!40000 ALTER TABLE `accessory_taccessorytype` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_taccessorytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tarraycard`
--

DROP TABLE IF EXISTS `accessory_tarraycard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tarraycard` (
  `accessory_id` bigint(20) NOT NULL,
  `array_card_interface` int(11) DEFAULT NULL,
  `array_card_cache` int(11) DEFAULT NULL,
  `array_card_buttery` int(11) DEFAULT NULL,
  `comment` longtext NOT NULL,
  `version` varchar(45) NOT NULL,
  `cache_status` int(11) DEFAULT NULL,
  `strip_size` int(11) DEFAULT NULL,
  `read_write_ratio` varchar(45) NOT NULL,
  `array_card_model` varchar(45) NOT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tarraycard`
--

LOCK TABLES `accessory_tarraycard` WRITE;
/*!40000 ALTER TABLE `accessory_tarraycard` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tarraycard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tcpu`
--

DROP TABLE IF EXISTS `accessory_tcpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tcpu` (
  `accessory_id` bigint(20) NOT NULL,
  `cpu_model` varchar(45) NOT NULL,
  `cpu_core` int(11) DEFAULT NULL,
  `cpu_frequency` double DEFAULT NULL,
  `comment` longtext NOT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tcpu`
--

LOCK TABLES `accessory_tcpu` WRITE;
/*!40000 ALTER TABLE `accessory_tcpu` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tcpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tdisk`
--

DROP TABLE IF EXISTS `accessory_tdisk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tdisk` (
  `accessory_id` bigint(20) NOT NULL,
  `disk_capacity` int(11) DEFAULT NULL,
  `disk_interface` int(11) DEFAULT NULL,
  `comment` longtext NOT NULL,
  `disk_model` varchar(45) NOT NULL,
  `version` varchar(45) NOT NULL,
  `bandwidth` int(11) DEFAULT NULL,
  `disk_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tdisk`
--

LOCK TABLES `accessory_tdisk` WRITE;
/*!40000 ALTER TABLE `accessory_tdisk` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tdisk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tfan`
--

DROP TABLE IF EXISTS `accessory_tfan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tfan` (
  `accessory_id` bigint(20) NOT NULL,
  `fan_redundancy_level` int(11) DEFAULT NULL,
  `fan_max_speed` int(11) DEFAULT NULL,
  `fan_auto_regulation_support` int(11) DEFAULT NULL,
  `fan_position` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tfan`
--

LOCK TABLES `accessory_tfan` WRITE;
/*!40000 ALTER TABLE `accessory_tfan` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tfan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tgpu`
--

DROP TABLE IF EXISTS `accessory_tgpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tgpu` (
  `accessory_id` bigint(20) NOT NULL,
  `gpu_core_num` int(11) DEFAULT NULL,
  `gpu_memory` int(11) DEFAULT NULL,
  `gpu_frequency` int(11) DEFAULT NULL,
  `gpu_chip` varchar(45) NOT NULL,
  `gpu_memory_specs` varchar(45) NOT NULL,
  `gpu_power` int(11) DEFAULT NULL,
  `gpu_idle_power` int(11) DEFAULT NULL,
  `gpu_memory_bandwidth` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tgpu`
--

LOCK TABLES `accessory_tgpu` WRITE;
/*!40000 ALTER TABLE `accessory_tgpu` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tgpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tguide`
--

DROP TABLE IF EXISTS `accessory_tguide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tguide` (
  `guide_id` int(11) NOT NULL,
  `comment` longtext NOT NULL,
  `used` int(11) DEFAULT NULL,
  `total_count` int(11) DEFAULT NULL,
  `guide_model` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`guide_id`),
  UNIQUE KEY `guide_model` (`guide_model`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tguide`
--

LOCK TABLES `accessory_tguide` WRITE;
/*!40000 ALTER TABLE `accessory_tguide` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tguide` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_thbacard`
--

DROP TABLE IF EXISTS `accessory_thbacard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_thbacard` (
  `accessory_id` bigint(20) NOT NULL,
  `hba_card_interface` int(11) DEFAULT NULL,
  `comment` longtext NOT NULL,
  `version` varchar(45) NOT NULL,
  `hba_card_model` varchar(45) NOT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_thbacard`
--

LOCK TABLES `accessory_thbacard` WRITE;
/*!40000 ALTER TABLE `accessory_thbacard` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_thbacard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tmemory`
--

DROP TABLE IF EXISTS `accessory_tmemory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tmemory` (
  `accessory_id` bigint(20) NOT NULL,
  `memory_capacity` int(11) DEFAULT NULL,
  `memroy_frequency` int(11) DEFAULT NULL,
  `memory_specs` varchar(45) NOT NULL,
  `comment` longtext NOT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tmemory`
--

LOCK TABLES `accessory_tmemory` WRITE;
/*!40000 ALTER TABLE `accessory_tmemory` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tmemory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tmotherboard`
--

DROP TABLE IF EXISTS `accessory_tmotherboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tmotherboard` (
  `accessory_id` bigint(20) NOT NULL,
  `mother_board_model` varchar(45) NOT NULL,
  `comment` longtext NOT NULL,
  `version` varchar(45) NOT NULL,
  `pci_count` int(11) DEFAULT NULL,
  `pcie_count` int(11) DEFAULT NULL,
  `sata_count` int(11) DEFAULT NULL,
  `sas_count` int(11) DEFAULT NULL,
  `m_2_count` int(11) DEFAULT NULL,
  `satadom_count` int(11) DEFAULT NULL,
  `lom_count` int(11) DEFAULT NULL,
  `dimm_count` int(11) DEFAULT NULL,
  `mother_board_chip` varchar(45) NOT NULL,
  `sd_support` int(11) DEFAULT NULL,
  `sata_controller_support` int(11) DEFAULT NULL,
  `sas_controller_support` int(11) DEFAULT NULL,
  `usb_count` int(11) DEFAULT NULL,
  `double_bios_protection_support` int(11) DEFAULT NULL,
  `asset_entry_support` int(11) DEFAULT NULL,
  `command_bios_support` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tmotherboard`
--

LOCK TABLES `accessory_tmotherboard` WRITE;
/*!40000 ALTER TABLE `accessory_tmotherboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tmotherboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tnetworkcard`
--

DROP TABLE IF EXISTS `accessory_tnetworkcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tnetworkcard` (
  `accessory_id` bigint(20) NOT NULL,
  `speed` int(11) DEFAULT NULL,
  `network_card_interface` int(11) DEFAULT NULL,
  `network_card_model` varchar(45) NOT NULL,
  `comment` longtext NOT NULL,
  `version` varchar(45) NOT NULL,
  `mac_address` varchar(45) NOT NULL,
  `network_card_ncsi_support` int(11) DEFAULT NULL,
  `network_card_pxe_support` int(11) DEFAULT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tnetworkcard`
--

LOCK TABLES `accessory_tnetworkcard` WRITE;
/*!40000 ALTER TABLE `accessory_tnetworkcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tnetworkcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accessory_tpower`
--

DROP TABLE IF EXISTS `accessory_tpower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessory_tpower` (
  `accessory_id` bigint(20) NOT NULL,
  `power_model` varchar(45) NOT NULL,
  `power_specs` int(11) DEFAULT NULL,
  `efficiency` int(11) DEFAULT NULL,
  `power_supply` int(11) DEFAULT NULL,
  `version` varchar(45) NOT NULL,
  PRIMARY KEY (`accessory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessory_tpower`
--

LOCK TABLES `accessory_tpower` WRITE;
/*!40000 ALTER TABLE `accessory_tpower` DISABLE KEYS */;
/*!40000 ALTER TABLE `accessory_tpower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_tauth`
--

DROP TABLE IF EXISTS `auth_tauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_tauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apiid` varchar(45) NOT NULL,
  `script` varchar(32) NOT NULL,
  `token` varchar(45) NOT NULL,
  `exp_time` datetime DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_tauth`
--

LOCK TABLES `auth_tauth` WRITE;
/*!40000 ALTER TABLE `auth_tauth` DISABLE KEYS */;
INSERT INTO `auth_tauth` VALUES (6,'testid','8a5da52ed126447d359e70c05721a8aa','747512817f7ead0c8b739809f1d9a118','2016-05-05 19:35:00',NULL);
/*!40000 ALTER TABLE `auth_tauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'content type','contenttypes','contenttype'),(2,'session','sessions','session'),(3,'t ip segment','ips','tipsegment'),(4,'t ip address','ips','tipaddress'),(5,'t bus line','dpt','tbusline'),(6,'t org','dpt','torg'),(7,'t org dpt','dpt','torgdpt'),(8,'t dpt','dpt','tdpt'),(9,'t cluster','dpt','tcluster'),(10,'t org user','dpt','torguser'),(11,'t memory','accessory','tmemory'),(12,'t accessory store','accessory','taccessorystore'),(13,'t mother board','accessory','tmotherboard'),(14,'t network card','accessory','tnetworkcard'),(15,'t accessory brand','accessory','taccessorybrand'),(16,'t fan','accessory','tfan'),(17,'t accessory','accessory','taccessory'),(18,'t hba card','accessory','thbacard'),(19,'t array card','accessory','tarraycard'),(20,'t power','accessory','tpower'),(21,'t guide','accessory','tguide'),(22,'t gpu','accessory','tgpu'),(23,'t cpu','accessory','tcpu'),(24,'t accessory type','accessory','taccessorytype'),(25,'t disk','accessory','tdisk'),(26,'t rack','idc','track'),(27,'t logic section','idc','tlogicsection'),(28,'t position','idc','tposition'),(29,'t logic section type','idc','tlogicsectiontype'),(30,'t idc','idc','tidc'),(31,'t slot type','server_device','tslottype'),(32,'t network interface','server_device','tnetworkinterface'),(33,'t slot','server_device','tslot'),(34,'t device producer type','server_device','tdeviceproducertype'),(35,'t os type','server_device','tostype'),(36,'t network interface config','server_device','tnetworkinterfaceconfig'),(37,'t server','server_device','tserver'),(38,'t server device type','server_device','tserverdevicetype'),(39,'t network interface ip','server_device','tnetworkinterfaceip'),(40,'t selection version record','server_device','tselectionversionrecord'),(41,'t server selection','server_device','tserverselection'),(42,'t asset','server_device','tasset'),(43,'t selection version','server_device','tselectionversion'),(44,'t inc server type','server_device','tincservertype'),(45,'t nic port link','net_device','tnicportlink'),(46,'t idc module','net_device','tidcmodule'),(47,'t net device','net_device','tnetdevice'),(48,'t nic port','net_device','tnicport'),(49,'t auth','auth','tauth');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'net_device','0001_initial','2016-05-03 17:59:25'),(2,'idc','0001_initial','2016-05-03 17:59:25'),(3,'dpt','0001_initial','2016-05-03 17:59:25'),(4,'server_device','0001_initial','2016-05-03 17:59:26'),(5,'accessory','0001_initial','2016-05-03 17:59:27'),(6,'accessory','0002_auto_20160503_1734','2016-05-03 17:59:27'),(7,'accessory','0003_auto_20160503_1747','2016-05-03 17:59:28'),(8,'auth','0001_initial','2016-05-03 17:59:28'),(9,'contenttypes','0001_initial','2016-05-03 17:59:28'),(10,'ips','0001_initial','2016-05-03 17:59:28'),(11,'net_device','0002_auto_20160503_1734','2016-05-03 17:59:28'),(12,'sessions','0001_initial','2016-05-03 17:59:28'),(13,'idc','0002_auto_20160503_1820','2016-05-03 18:20:17'),(14,'idc','0003_auto_20160504_1619','2016-05-04 16:22:02'),(15,'accessory','0004_auto_20160505_1615','2016-05-05 16:53:18');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_tbusline`
--

DROP TABLE IF EXISTS `dpt_tbusline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_tbusline` (
  `busline_id` bigint(20) NOT NULL,
  `busline_code` varchar(100) NOT NULL,
  `busline_name` varchar(100) NOT NULL,
  `operator_ids` varchar(255) NOT NULL,
  `owner_ids` varchar(255) NOT NULL,
  `owner_id` varchar(22) NOT NULL,
  `operator_id` varchar(22) NOT NULL,
  `owner_name` varchar(255) NOT NULL,
  `operator_name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`busline_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_tbusline`
--

LOCK TABLES `dpt_tbusline` WRITE;
/*!40000 ALTER TABLE `dpt_tbusline` DISABLE KEYS */;
/*!40000 ALTER TABLE `dpt_tbusline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_tcluster`
--

DROP TABLE IF EXISTS `dpt_tcluster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_tcluster` (
  `cluster_id` bigint(20) NOT NULL,
  `cluster_name` varchar(50) NOT NULL,
  `deploy_path` varchar(200) NOT NULL,
  `version` varchar(50) NOT NULL,
  `cluster_type` int(11) NOT NULL,
  `type_value` varchar(20) NOT NULL,
  `cluster_state` int(11) NOT NULL,
  `monitor_state` int(11) NOT NULL,
  `deploy_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `deploy_email` varchar(255) NOT NULL,
  `cluster_manager_id` varchar(255) NOT NULL,
  `cluster_manager_name` varchar(255) NOT NULL,
  `org_id` bigint(20) NOT NULL,
  `org_name` varchar(255) NOT NULL,
  `delete_status` varchar(1) NOT NULL,
  PRIMARY KEY (`cluster_id`),
  UNIQUE KEY `cluster_name` (`cluster_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_tcluster`
--

LOCK TABLES `dpt_tcluster` WRITE;
/*!40000 ALTER TABLE `dpt_tcluster` DISABLE KEYS */;
/*!40000 ALTER TABLE `dpt_tcluster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_tdpt`
--

DROP TABLE IF EXISTS `dpt_tdpt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_tdpt` (
  `dpt_id` bigint(20) NOT NULL,
  `dpt_level` int(11) NOT NULL,
  `dpt_name` varchar(255) NOT NULL,
  `dpt_bsp_id` varchar(22) NOT NULL,
  `dpt_pid` bigint(20) NOT NULL,
  PRIMARY KEY (`dpt_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_tdpt`
--

LOCK TABLES `dpt_tdpt` WRITE;
/*!40000 ALTER TABLE `dpt_tdpt` DISABLE KEYS */;
/*!40000 ALTER TABLE `dpt_tdpt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_torg`
--

DROP TABLE IF EXISTS `dpt_torg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_torg` (
  `org_id` bigint(20) NOT NULL,
  `org_level` int(11) DEFAULT NULL,
  `org_name` varchar(255) NOT NULL,
  `org_bsp_id` varchar(25) NOT NULL,
  `org_bsp_pid` varchar(25) NOT NULL,
  PRIMARY KEY (`org_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_torg`
--

LOCK TABLES `dpt_torg` WRITE;
/*!40000 ALTER TABLE `dpt_torg` DISABLE KEYS */;
INSERT INTO `dpt_torg` VALUES (1,0,'58同城','2011010814223073b228a5','0'),(646308,1,'技术工程平台部','201103141117372668898e','2011010814223073b228a5'),(646309,1,'品牌及公关部','2011033115254725a5407b','2011010814223073b228a5'),(646310,1,'总裁办','20110402112444433ffd8b','2011010814223073b228a5'),(646311,1,'58到家','20140716184318459a3e72','2011010814223073b228a5'),(646312,1,'投资并购部','201408151950264f0f6d4b','2011010814223073b228a5'),(646313,1,'C2C平台事业部','2014090914540439d96f41','2011010814223073b228a5'),(646314,1,'分类信息事业群','2015031013263432a2e19a','2011010814223073b228a5'),(646315,1,'房产事业群','201504291351016f1df260','2011010814223073b228a5');
/*!40000 ALTER TABLE `dpt_torg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_torgdpt`
--

DROP TABLE IF EXISTS `dpt_torgdpt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_torgdpt` (
  `org_dpt_id` bigint(20) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `bsp_dpt_id` bigint(20) DEFAULT NULL,
  `org_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`org_dpt_id`),
  KEY `dpt_torgdpt_7664c5e2` (`bsp_dpt_id`),
  KEY `dpt_torgdpt_9cf869aa` (`org_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_torgdpt`
--

LOCK TABLES `dpt_torgdpt` WRITE;
/*!40000 ALTER TABLE `dpt_torgdpt` DISABLE KEYS */;
/*!40000 ALTER TABLE `dpt_torgdpt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dpt_torguser`
--

DROP TABLE IF EXISTS `dpt_torguser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dpt_torguser` (
  `bsp_user_id` varchar(50) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_real_name` varchar(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_mobile` varchar(255) NOT NULL,
  `user_tel` varchar(50) NOT NULL,
  `user_child_tel` varchar(255) NOT NULL,
  `user_gender` varchar(2) NOT NULL,
  `employ_id` varchar(255) NOT NULL,
  `qq` varchar(255) NOT NULL,
  `bsp_leader` varchar(22) NOT NULL,
  `dpt_name` varchar(255) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `org_dpt_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`bsp_user_id`),
  KEY `dpt_torguser_f82bd571` (`org_dpt_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dpt_torguser`
--

LOCK TABLES `dpt_torguser` WRITE;
/*!40000 ALTER TABLE `dpt_torguser` DISABLE KEYS */;
/*!40000 ALTER TABLE `dpt_torguser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc_tidc`
--

DROP TABLE IF EXISTS `idc_tidc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc_tidc` (
  `idc_id` bigint(20) NOT NULL,
  `idc_region` varchar(45) NOT NULL,
  `idc_zone` varchar(45) NOT NULL,
  `idc_campus` varchar(45) NOT NULL,
  `idc_address` longtext NOT NULL,
  `idc_phone` varchar(45) NOT NULL,
  `idc_fax` varchar(45) NOT NULL,
  `idc_email` varchar(45) NOT NULL,
  `idc_owner_master_id` varchar(255) NOT NULL,
  `idc_owner_backup_id` varchar(255) NOT NULL,
  `idc_contacts` varchar(255) NOT NULL,
  `idc_name` varchar(255) NOT NULL,
  `idc_enable_time` datetime DEFAULT NULL,
  `idc_due_time` datetime DEFAULT NULL,
  `idc_resource_type` varchar(255) NOT NULL,
  `idc_supplier` longtext NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`idc_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc_tidc`
--

LOCK TABLES `idc_tidc` WRITE;
/*!40000 ALTER TABLE `idc_tidc` DISABLE KEYS */;
INSERT INTO `idc_tidc` VALUES (65716593825984,'华北','天津','泰达服务外包产业园','天津市开发区第五大街与北海路口泰达服务外包产业园内腾讯公司3栋','15022575804','','58idc-tj@asiacom.net.cn','胡鑫','冯然','郭燕磊','天津滨海M303',NULL,NULL,'租用机房','腾讯',NULL),(65716593825989,'华北','天津','泰达服务外包产业园','天津市开发区第五大街与北海路口泰达服务外包产业园内腾讯公司3栋','15022575804','','58idc-tj@asiacom.net.cn','胡鑫','冯然','郭燕磊','天津滨海M204',NULL,NULL,'租用机房','腾讯',NULL),(65716593825991,'华北','天津','泰达服务外包产业园','天津市开发区第五大街与北海路口泰达服务外包产业园内腾讯公司3栋','15022575804','','58idc-tj@asiacom.net.cn','胡鑫','冯然','郭燕磊','天津滨海M203',NULL,NULL,'租用机房','腾讯',NULL),(65716593825993,'华北','北京','世纪互联M6机房','朝阳区酒仙桥东路1号M6楼4层（楼南侧中青印刷厂入口）','010-84562121-1058','','gao.si@21vianet.com','胡鑫','冯然','高思','北京M6机房一期',NULL,NULL,'租用机房','世纪互联',NULL),(65716593825996,'华北','北京','世纪互联M6机房','朝阳区酒仙桥东路1号M6楼4层（楼南侧中青印刷厂入口）','010-84562121-1058','','gao.si@21vianet.com','胡鑫','冯然','高思','北京M6机房二期',NULL,NULL,'租用机房','世纪互联',NULL),(65716593825998,'华北','北京','世纪互联同济机房','北京亦庄经济技术开发区同济中路15号','010-84562121-1058','','gao.si@21vianet.com','胡鑫','冯然','高思','北京同济101机房',NULL,NULL,'租用机房','世纪互联',NULL),(65716593826000,'华北','北京','世纪互联同济机房','北京亦庄经济技术开发区同济中路15号','010-84562121-1058','','gao.si@21vianet.com','胡鑫','冯然','高思','北京同济103机房',NULL,NULL,'租用机房','世纪互联',NULL),(65716593826002,'华北','北京','世纪互联电话局机房','北京亦庄经济技术开发区中和街1号','010-84562121-1058','','gao.si@21vianet.com','胡鑫','冯然','高思','北京电话局机房',NULL,NULL,'租用机房','世纪互联',NULL),(65716593826005,'华北','北京','定福庄联通电话局','北京朝阳区三间房南里6号','010-85235887-8098','','cscbj@dnion.com','田少奎','李俊义','赵曙光','G2-数据中心',NULL,NULL,'租用机房','帝联',NULL),(65716593826007,'华北','北京','星光影视园','北京市大兴区西红门镇北兴路东段2号星光影视园A-1楼','4006519966','','cc@21vianet.com','田少奎','李俊义','周萌萌','G1-数据中心',NULL,NULL,'租用机房','世纪互联',NULL);
/*!40000 ALTER TABLE `idc_tidc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc_tlogicsection`
--

DROP TABLE IF EXISTS `idc_tlogicsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc_tlogicsection` (
  `logic_section_id` bigint(20) NOT NULL,
  `logic_section_name` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `idc_id` bigint(20) DEFAULT NULL,
  `logic_section_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`logic_section_id`),
  KEY `idc_tlogicsection_0869e37a` (`idc_id`),
  KEY `idc_tlogicsection_770b0b1c` (`logic_section_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc_tlogicsection`
--

LOCK TABLES `idc_tlogicsection` WRITE;
/*!40000 ALTER TABLE `idc_tlogicsection` DISABLE KEYS */;
/*!40000 ALTER TABLE `idc_tlogicsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc_tlogicsectiontype`
--

DROP TABLE IF EXISTS `idc_tlogicsectiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc_tlogicsectiontype` (
  `logic_section_type_id` bigint(20) NOT NULL,
  `logic_section_type_name` varchar(45) NOT NULL,
  `logic_section_type_desc` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`logic_section_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc_tlogicsectiontype`
--

LOCK TABLES `idc_tlogicsectiontype` WRITE;
/*!40000 ALTER TABLE `idc_tlogicsectiontype` DISABLE KEYS */;
/*!40000 ALTER TABLE `idc_tlogicsectiontype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc_tposition`
--

DROP TABLE IF EXISTS `idc_tposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc_tposition` (
  `position_id` bigint(20) NOT NULL,
  `positon_spec_height` varchar(45) NOT NULL,
  `positon_num` int(11) DEFAULT NULL,
  `position_status` varchar(255) NOT NULL,
  `start_spec_height` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `rack_id_id` bigint(20) DEFAULT NULL,
  `position_comment` longtext NOT NULL,
  PRIMARY KEY (`position_id`),
  KEY `idc_tposition_21556361` (`rack_id_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc_tposition`
--

LOCK TABLES `idc_tposition` WRITE;
/*!40000 ALTER TABLE `idc_tposition` DISABLE KEYS */;
/*!40000 ALTER TABLE `idc_tposition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc_track`
--

DROP TABLE IF EXISTS `idc_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc_track` (
  `rack_id` bigint(20) NOT NULL,
  `rack_name` varchar(45) NOT NULL,
  `rack_code` varchar(45) NOT NULL,
  `rack_depth` int(11) DEFAULT NULL,
  `rack_height` int(11) DEFAULT NULL,
  `rack_width` int(11) DEFAULT NULL,
  `rack_spec_height` varchar(45) NOT NULL,
  `rack_energy_type` varchar(45) NOT NULL,
  `rack_power_max` int(11) DEFAULT NULL,
  `rack_power_rating` int(11) DEFAULT NULL,
  `rack_virtualization` varchar(45) NOT NULL,
  `rack_extranet` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `idc_id_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`rack_id`),
  KEY `idc_track_cd352ef9` (`idc_id_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc_track`
--

LOCK TABLES `idc_track` WRITE;
/*!40000 ALTER TABLE `idc_track` DISABLE KEYS */;
/*!40000 ALTER TABLE `idc_track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ips_tipaddress`
--

DROP TABLE IF EXISTS `ips_tipaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips_tipaddress` (
  `ip_address_id` bigint(20) NOT NULL,
  `ip_address` varchar(255) NOT NULL,
  `assign_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `ip_status` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `ip_type` int(11) DEFAULT NULL,
  `ip_segment_name` varchar(255) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `ip_assigner_id` varchar(50) DEFAULT NULL,
  `ip_segment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ip_address_id`),
  KEY `ips_tipaddress_7828f71a` (`ip_assigner_id`),
  KEY `ips_tipaddress_3d0370ca` (`ip_segment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ips_tipaddress`
--

LOCK TABLES `ips_tipaddress` WRITE;
/*!40000 ALTER TABLE `ips_tipaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `ips_tipaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ips_tipsegment`
--

DROP TABLE IF EXISTS `ips_tipsegment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips_tipsegment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_segment_id` bigint(20) NOT NULL,
  `ip_segment_address` varchar(255) NOT NULL,
  `ip_segment_netmask` varchar(255) NOT NULL,
  `ip_segment_isp` varchar(255) NOT NULL,
  `ip_segment_gateway` varchar(255) NOT NULL,
  `ip_segment_broadcast` varchar(255) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ips_tipsegment`
--

LOCK TABLES `ips_tipsegment` WRITE;
/*!40000 ALTER TABLE `ips_tipsegment` DISABLE KEYS */;
/*!40000 ALTER TABLE `ips_tipsegment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `net_device_tidcmodule`
--

DROP TABLE IF EXISTS `net_device_tidcmodule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `net_device_tidcmodule` (
  `module_id` bigint(20) NOT NULL,
  `module_name` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`module_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_device_tidcmodule`
--

LOCK TABLES `net_device_tidcmodule` WRITE;
/*!40000 ALTER TABLE `net_device_tidcmodule` DISABLE KEYS */;
/*!40000 ALTER TABLE `net_device_tidcmodule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `net_device_tnetdevice`
--

DROP TABLE IF EXISTS `net_device_tnetdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `net_device_tnetdevice` (
  `net_device_id` bigint(20) NOT NULL,
  `net_device_name` varchar(45) NOT NULL,
  `device_level` int(11) DEFAULT NULL,
  `t_net_devicecol` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `asset_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`net_device_id`),
  KEY `net_device_tnetdevice_51c6d5db` (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_device_tnetdevice`
--

LOCK TABLES `net_device_tnetdevice` WRITE;
/*!40000 ALTER TABLE `net_device_tnetdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `net_device_tnetdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `net_device_tnicport`
--

DROP TABLE IF EXISTS `net_device_tnicport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `net_device_tnicport` (
  `nic_port_id` bigint(20) NOT NULL,
  `nic_port_name` varchar(45) NOT NULL,
  `nic_port_speed` int(11) NOT NULL,
  `nic_port_transfer_medium` int(11) NOT NULL,
  `nic_port_bandwidth` int(11) NOT NULL,
  `nic_port_mode` int(11) NOT NULL,
  `nic_port_link_type` int(11) NOT NULL,
  `nic_port_num` int(11) NOT NULL,
  `nic_port_level` int(11) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `asset_id` bigint(20) NOT NULL,
  `nic_port_planned_position_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`nic_port_id`),
  KEY `net_device_tnicport_51c6d5db` (`asset_id`),
  KEY `net_device_tnicport_bb85bec6` (`nic_port_planned_position_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_device_tnicport`
--

LOCK TABLES `net_device_tnicport` WRITE;
/*!40000 ALTER TABLE `net_device_tnicport` DISABLE KEYS */;
/*!40000 ALTER TABLE `net_device_tnicport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `net_device_tnicportlink`
--

DROP TABLE IF EXISTS `net_device_tnicportlink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `net_device_tnicportlink` (
  `nic_port_link_id` bigint(20) NOT NULL,
  `cable_type` int(11) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `nic_port_id_lower_id` bigint(20) NOT NULL,
  `nic_port_id_upper_id` bigint(20) NOT NULL,
  PRIMARY KEY (`nic_port_link_id`),
  KEY `net_device_tnicportlink_948b97c7` (`nic_port_id_lower_id`),
  KEY `net_device_tnicportlink_9a1651a7` (`nic_port_id_upper_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_device_tnicportlink`
--

LOCK TABLES `net_device_tnicportlink` WRITE;
/*!40000 ALTER TABLE `net_device_tnicportlink` DISABLE KEYS */;
/*!40000 ALTER TABLE `net_device_tnicportlink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tasset`
--

DROP TABLE IF EXISTS `server_device_tasset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tasset` (
  `asset_id` bigint(20) NOT NULL,
  `asset_sn` varchar(45) NOT NULL,
  `asset_is_device` int(11) DEFAULT NULL,
  `asset_instock_time` datetime DEFAULT NULL,
  `asset_first_use_time` datetime DEFAULT NULL,
  `asset_outstock_time` datetime DEFAULT NULL,
  `asset_warranty_due_time` datetime DEFAULT NULL,
  `asset_receipt_time` datetime DEFAULT NULL,
  `asset_on_shelf_time` datetime DEFAULT NULL,
  `asset_off_shelf_time` datetime DEFAULT NULL,
  `asset_last_update_time` datetime NOT NULL,
  `asset_status` int(11) DEFAULT NULL,
  `asset_comment` longtext NOT NULL,
  `device_type` int(11) DEFAULT NULL,
  `order_item_id` bigint(20) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `asset_backup_operator_id_id` varchar(50) NOT NULL,
  `asset_backup_ower_id_id` varchar(50) NOT NULL,
  `asset_belong_org_id_id` bigint(20) NOT NULL,
  `asset_operator_id_id` varchar(50) NOT NULL,
  `asset_operator_org_id_id` bigint(20) NOT NULL,
  `asset_ower_id_id` varchar(50) NOT NULL,
  `position_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`asset_id`),
  KEY `server_device_tasset_21195d20` (`asset_last_update_time`),
  KEY `server_device_tasset_9dded4c7` (`asset_backup_operator_id_id`),
  KEY `server_device_tasset_56321aba` (`asset_backup_ower_id_id`),
  KEY `server_device_tasset_9acfe678` (`asset_belong_org_id_id`),
  KEY `server_device_tasset_27af2f4d` (`asset_operator_id_id`),
  KEY `server_device_tasset_f9bdff0b` (`asset_operator_org_id_id`),
  KEY `server_device_tasset_955e4753` (`asset_ower_id_id`),
  KEY `server_device_tasset_bce5bd07` (`position_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tasset`
--

LOCK TABLES `server_device_tasset` WRITE;
/*!40000 ALTER TABLE `server_device_tasset` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tasset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tdeviceproducertype`
--

DROP TABLE IF EXISTS `server_device_tdeviceproducertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tdeviceproducertype` (
  `device_producer_type_id` bigint(20) NOT NULL,
  `producer_id` bigint(20) DEFAULT NULL,
  `producer_name` varchar(45) NOT NULL,
  `device_type` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`device_producer_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tdeviceproducertype`
--

LOCK TABLES `server_device_tdeviceproducertype` WRITE;
/*!40000 ALTER TABLE `server_device_tdeviceproducertype` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tdeviceproducertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tincservertype`
--

DROP TABLE IF EXISTS `server_device_tincservertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tincservertype` (
  `inc_server_type_id` bigint(20) NOT NULL,
  `inc_server_type_name` varchar(45) NOT NULL,
  `inc_server_code` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`inc_server_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tincservertype`
--

LOCK TABLES `server_device_tincservertype` WRITE;
/*!40000 ALTER TABLE `server_device_tincservertype` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tincservertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tnetworkinterface`
--

DROP TABLE IF EXISTS `server_device_tnetworkinterface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tnetworkinterface` (
  `network_interface_id` bigint(20) NOT NULL,
  `network_interface_name` varchar(45) NOT NULL,
  `network_interface_type` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `server_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`network_interface_id`),
  KEY `server_device_tnetworkinterface_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tnetworkinterface`
--

LOCK TABLES `server_device_tnetworkinterface` WRITE;
/*!40000 ALTER TABLE `server_device_tnetworkinterface` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tnetworkinterface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tnetworkinterfaceconfig`
--

DROP TABLE IF EXISTS `server_device_tnetworkinterfaceconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tnetworkinterfaceconfig` (
  `network_interface_config_id` bigint(20) NOT NULL,
  `network_interface_link_type` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `network_interface_id` bigint(20) DEFAULT NULL,
  `nic_port_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`network_interface_config_id`),
  KEY `server_device_tnetworkinterfaceconfig_cea58354` (`network_interface_id`),
  KEY `server_device_tnetworkinterfaceconfig_90ea87ad` (`nic_port_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tnetworkinterfaceconfig`
--

LOCK TABLES `server_device_tnetworkinterfaceconfig` WRITE;
/*!40000 ALTER TABLE `server_device_tnetworkinterfaceconfig` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tnetworkinterfaceconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tnetworkinterfaceip`
--

DROP TABLE IF EXISTS `server_device_tnetworkinterfaceip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tnetworkinterfaceip` (
  `network_interface_ip_id` bigint(20) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `network_interface_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`network_interface_ip_id`),
  KEY `server_device_tnetworkinterfaceip_cea58354` (`network_interface_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tnetworkinterfaceip`
--

LOCK TABLES `server_device_tnetworkinterfaceip` WRITE;
/*!40000 ALTER TABLE `server_device_tnetworkinterfaceip` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tnetworkinterfaceip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tostype`
--

DROP TABLE IF EXISTS `server_device_tostype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tostype` (
  `os_type_id` bigint(20) NOT NULL,
  `os_type_name` varchar(45) NOT NULL,
  `os_type_version` varchar(45) NOT NULL,
  `os_full_name` varchar(45) NOT NULL,
  `os_default_version` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`os_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tostype`
--

LOCK TABLES `server_device_tostype` WRITE;
/*!40000 ALTER TABLE `server_device_tostype` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tostype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tselectionversion`
--

DROP TABLE IF EXISTS `server_device_tselectionversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tselectionversion` (
  `server_selection_version_id` bigint(20) NOT NULL,
  `server_selection_version_start_time` datetime DEFAULT NULL,
  `server_selection_version_end_time` datetime DEFAULT NULL,
  `server_selection_version_author_id` bigint(20) DEFAULT NULL,
  `server_selection_versionnumber` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`server_selection_version_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tselectionversion`
--

LOCK TABLES `server_device_tselectionversion` WRITE;
/*!40000 ALTER TABLE `server_device_tselectionversion` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tselectionversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tselectionversionrecord`
--

DROP TABLE IF EXISTS `server_device_tselectionversionrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tselectionversionrecord` (
  `server_selection_version_record_id` bigint(20) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `server_selection_id` bigint(20) DEFAULT NULL,
  `server_selection_version_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_selection_version_record_id`),
  KEY `server_device_tselectionversionrecord_2a23b0fb` (`server_selection_id`),
  KEY `server_device_tselectionversionrecord_a28cd537` (`server_selection_version_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tselectionversionrecord`
--

LOCK TABLES `server_device_tselectionversionrecord` WRITE;
/*!40000 ALTER TABLE `server_device_tselectionversionrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tselectionversionrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tserver`
--

DROP TABLE IF EXISTS `server_device_tserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tserver` (
  `server_id` bigint(20) NOT NULL,
  `server_comment` longtext NOT NULL,
  `server_bios_os` varchar(45) NOT NULL,
  `server_status` int(11) DEFAULT NULL,
  `server_bmc` varchar(45) NOT NULL,
  `server_host_name` varchar(45) NOT NULL,
  `server_kernel_version` varchar(45) NOT NULL,
  `server_ads_status` int(11) DEFAULT NULL,
  `server_ads_check_time` date DEFAULT NULL,
  `server_ads_installed` int(11) DEFAULT NULL,
  `server_ads_update_time` date DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `asset_id` bigint(20) DEFAULT NULL,
  `inc_server_type_id` bigint(20) DEFAULT NULL,
  `os_type_id` bigint(20) DEFAULT NULL,
  `server_device_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_id`),
  KEY `server_device_tserver_51c6d5db` (`asset_id`),
  KEY `server_device_tserver_41f7e7ef` (`inc_server_type_id`),
  KEY `server_device_tserver_f9b38fec` (`os_type_id`),
  KEY `server_device_tserver_2e67371a` (`server_device_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tserver`
--

LOCK TABLES `server_device_tserver` WRITE;
/*!40000 ALTER TABLE `server_device_tserver` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tserver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tserverdevicetype`
--

DROP TABLE IF EXISTS `server_device_tserverdevicetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tserverdevicetype` (
  `server_type_id` bigint(20) NOT NULL,
  `server_device_type_name` varchar(45) NOT NULL,
  `server_hight` int(11) DEFAULT NULL,
  `server_width` int(11) DEFAULT NULL,
  `server_depth` int(11) DEFAULT NULL,
  `server_electricity` varchar(45) NOT NULL,
  `server_weight` int(11) DEFAULT NULL,
  `server_score` varchar(45) NOT NULL,
  `server_minios` varchar(45) NOT NULL,
  `server_max_power` int(11) DEFAULT NULL,
  `server_rated_power` int(11) DEFAULT NULL,
  `server_power_type` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `device_producer_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_type_id`),
  KEY `server_device_tserverdevicetype_5447f89e` (`device_producer_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tserverdevicetype`
--

LOCK TABLES `server_device_tserverdevicetype` WRITE;
/*!40000 ALTER TABLE `server_device_tserverdevicetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tserverdevicetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tserverselection`
--

DROP TABLE IF EXISTS `server_device_tserverselection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tserverselection` (
  `server_selection_id` bigint(20) NOT NULL,
  `server_selection_datetime` datetime DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `device_producer_type_id` bigint(20) DEFAULT NULL,
  `inc_server_type_id` bigint(20) DEFAULT NULL,
  `server_device_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`server_selection_id`),
  KEY `server_device_tserverselection_5447f89e` (`device_producer_type_id`),
  KEY `server_device_tserverselection_41f7e7ef` (`inc_server_type_id`),
  KEY `server_device_tserverselection_2e67371a` (`server_device_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tserverselection`
--

LOCK TABLES `server_device_tserverselection` WRITE;
/*!40000 ALTER TABLE `server_device_tserverselection` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tserverselection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tslot`
--

DROP TABLE IF EXISTS `server_device_tslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tslot` (
  `slot_id` bigint(20) NOT NULL,
  `slot_face_direction` int(11) DEFAULT NULL,
  `insert_accessory_id` bigint(20) DEFAULT NULL,
  `slot_num` varchar(45) NOT NULL,
  `delete_status` int(11) DEFAULT NULL,
  `access_id` bigint(20) DEFAULT NULL,
  `slot_type_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`slot_id`),
  KEY `server_device_tslot_ae441468` (`access_id`),
  KEY `server_device_tslot_872f1fab` (`slot_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tslot`
--

LOCK TABLES `server_device_tslot` WRITE;
/*!40000 ALTER TABLE `server_device_tslot` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_device_tslottype`
--

DROP TABLE IF EXISTS `server_device_tslottype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_device_tslottype` (
  `slot_type_id` bigint(20) NOT NULL,
  `slot_type_name` varchar(45) NOT NULL,
  `slot_spec` int(11) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`slot_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_device_tslottype`
--

LOCK TABLES `server_device_tslottype` WRITE;
/*!40000 ALTER TABLE `server_device_tslottype` DISABLE KEYS */;
/*!40000 ALTER TABLE `server_device_tslottype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-05 19:31:44
