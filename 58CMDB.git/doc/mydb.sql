/*
 Navicat Premium Data Transfer

 Source Server         : g1-apo-test-v02
 Source Server Type    : MySQL
 Source Server Version : 50548
 Source Host           : g1-apo-test-v02
 Source Database       : mydb

 Target Server Type    : MySQL
 Target Server Version : 50548
 File Encoding         : utf-8

 Date: 03/10/2016 11:51:02 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `t_cluster`
-- ----------------------------
DROP TABLE IF EXISTS `t_cluster`;
CREATE TABLE `t_cluster` (
  `cluster_id` bigint(20) NOT NULL,
  `cluster_name` varchar(255) DEFAULT NULL,
  `cluster_manager_ids` varchar(255) DEFAULT NULL,
  `org_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`cluster_id`),
  KEY `org_id` (`org_id`),
  CONSTRAINT `idx_cluster_org` FOREIGN KEY (`org_id`) REFERENCES `t_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_dpt`
-- ----------------------------
DROP TABLE IF EXISTS `t_dpt`;
CREATE TABLE `t_dpt` (
  `bsp_dpt_id` char(22) NOT NULL,
  `dpt_level` tinyint(4) DEFAULT NULL,
  `dpt_name` varchar(255) DEFAULT NULL,
  `bsp_dpt_p_id` char(50) DEFAULT NULL,
  PRIMARY KEY (`bsp_dpt_id`),
  KEY `bsp_dpt_p_id` (`bsp_dpt_p_id`),
  CONSTRAINT ` idx_dpt_pid` FOREIGN KEY (`bsp_dpt_p_id`) REFERENCES `t_dpt` (`bsp_dpt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_ip_address`
-- ----------------------------
DROP TABLE IF EXISTS `t_ip_address`;
CREATE TABLE `t_ip_address` (
  `ip_address_id` bigint(20) DEFAULT NULL,
  `ip_address` varchar(255) DEFAULT NULL,
  `assign_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `ip_status` tinyint(4) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `ip_type` tinyint(4) DEFAULT NULL,
  `ip_segment_id` bigint(20) DEFAULT NULL,
  `ip_assigner_id` char(22) DEFAULT NULL,
  `ip_segment_name` varchar(255) DEFAULT NULL,
  KEY `ip_segment_id` (`ip_segment_id`),
  KEY `ip_assigner_id` (`ip_assigner_id`),
  KEY `ip_assigner_id_2` (`ip_assigner_id`),
  KEY `ip_assigner_id_3` (`ip_assigner_id`),
  KEY `ip_assigner_id_4` (`ip_assigner_id`),
  CONSTRAINT `idx_user` FOREIGN KEY (`ip_assigner_id`) REFERENCES `t_org_user` (`bsp_user_id`),
  CONSTRAINT `idx_ip_segment` FOREIGN KEY (`ip_segment_id`) REFERENCES `t_ip_segment` (`ip_segment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_ip_segment`
-- ----------------------------
DROP TABLE IF EXISTS `t_ip_segment`;
CREATE TABLE `t_ip_segment` (
  `ip_segment_id` bigint(20) NOT NULL,
  `ip_segment_address` varchar(255) DEFAULT NULL,
  `ip_segment_netmask` varchar(255) DEFAULT NULL,
  `ip_segment_isp` varchar(255) DEFAULT NULL,
  `vlan_Id` bigint(20) DEFAULT NULL,
  `ip_segment_gateway` varchar(255) DEFAULT NULL,
  `ip_segment_broadcast` varchar(255) DEFAULT NULL,
  KEY `ip_segment_id` (`ip_segment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_org`
-- ----------------------------
DROP TABLE IF EXISTS `t_org`;
CREATE TABLE `t_org` (
  `org_id` bigint(20) NOT NULL,
  `org_pid` bigint(20) DEFAULT NULL,
  `org_level` tinyint(4) DEFAULT NULL,
  `org_name` varchar(255) DEFAULT NULL,
  `org_operator_ids` varchar(255) DEFAULT NULL,
  `org_manager_ids` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_org_dpt`
-- ----------------------------
DROP TABLE IF EXISTS `t_org_dpt`;
CREATE TABLE `t_org_dpt` (
  `org_dpt_id` bigint(20) DEFAULT NULL,
  `bsp_dpt_id` char(22) DEFAULT NULL,
  `org_id` bigint(11) DEFAULT NULL,
  KEY `bsp_dpt_id` (`bsp_dpt_id`),
  KEY `org_id` (`org_id`),
  CONSTRAINT `idx_dpt_dpt` FOREIGN KEY (`org_id`) REFERENCES `t_org` (`org_id`),
  CONSTRAINT `idx_dpt_org` FOREIGN KEY (`bsp_dpt_id`) REFERENCES `t_dpt` (`bsp_dpt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_org_user`
-- ----------------------------
DROP TABLE IF EXISTS `t_org_user`;
CREATE TABLE `t_org_user` (
  `bsp_user_id` char(50) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_real_name` varchar(255) DEFAULT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `user_mobile` varchar(255) DEFAULT NULL,
  `user_tel` varchar(50) DEFAULT NULL,
  `user_child_tel` varchar(255) DEFAULT NULL,
  `user_gender` char(50) DEFAULT NULL,
  `employ_id` varchar(255) DEFAULT NULL,
  `qq` varchar(255) DEFAULT NULL,
  `bsp_leader_id` char(22) DEFAULT NULL,
  `org_dpt_id` char(22) DEFAULT NULL,
  `dpt_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`bsp_user_id`),
  KEY `bsp_leader_id` (`bsp_leader_id`),
  KEY `org_dpt_id` (`org_dpt_id`),
  CONSTRAINT `idx_org_dpt` FOREIGN KEY (`org_dpt_id`) REFERENCES `t_dpt` (`bsp_dpt_id`),
  CONSTRAINT `idx_pid` FOREIGN KEY (`bsp_leader_id`) REFERENCES `t_org_user` (`bsp_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
