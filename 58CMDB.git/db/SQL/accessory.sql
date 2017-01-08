SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `cmdb`.`t_accessory_band`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_accessory_band` (
  `brand_id` BIGINT NOT NULL,
  `brand_name` VARCHAR(45) NULL,
  PRIMARY KEY (`brand_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_accessory_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_accessory_type` (
  `accessory_type_id` BIGINT NOT NULL,
  `accessory_type_name` VARCHAR(45) NULL,
  PRIMARY KEY (`accessory_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_accessory_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_accessory_store` (
  `accessory_store_id` BIGINT NOT NULL,
  `accessory_store_name` VARCHAR(45) NULL,
  `accessory_store_position` VARCHAR(45) NULL,
  `accessory_store_poner` VARCHAR(45) NULL,
  PRIMARY KEY (`accessory_store_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_accessory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_accessory` (
  `accessory_id` BIGINT NOT NULL,
  `accessory_status` INT NULL,
  `idc_id` BIGINT NULL,
  `sn` INT NULL,
  `enable_time` DATETIME NULL,
  `due_time` DATETIME NULL,
  `accessory_type_id` BIGINT NOT NULL,
  `store_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_accessory_t_accessory_type1_idx` (`accessory_type_id` ASC),
  INDEX `fk_t_accessory_t_accessory_store1_idx` (`store_id` ASC),
  CONSTRAINT `fk_t_accessory_t_accessory_type1`
    FOREIGN KEY (`accessory_type_id`)
    REFERENCES `cmdb`.`t_accessory_type` (`accessory_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_accessory_t_accessory_store1`
    FOREIGN KEY (`store_id`)
    REFERENCES `cmdb`.`t_accessory_store` (`accessory_store_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t _cpu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t _cpu` (
  `accessory_id` BIGINT NOT NULL,
  `cpu_model` VARCHAR(45) NULL,
  `cpu_core` INT NULL,
  `cpu_frequency` FLOAT NULL,
  `cpu_power` INT NULL,
  `comment` TEXT NULL,
  `platform_type` VARCHAR(45) NULL,
  `cpu_ht_support` TINYINT NULL,
  `cpu_vm_support` TINYINT NULL,
  `cpu_memory_channel_num` INT NULL,
  `cpu_max_num` INT NULL,
  `cpu_node_support` TINYINT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t _cpu_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t _cpu_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t _cpu_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t _cpu_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_memory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_memory` (
  `accessory_id` BIGINT NOT NULL,
  `memory_capacity` INT NULL,
  `memroy_frequency` INT NULL,
  `memory_model` VARCHAR(45) NULL,
  `memory_specs` VARCHAR(45) NULL,
  `comment` TEXT NULL,
  `memory_ecc_support` TINYINT NULL,
  `memory_channel_num` INT NULL,
  `memory_max_underclocking` TINYINT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_memory_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_memory_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_memory_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_memory_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_disk`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_disk` (
  `accessory_id` BIGINT NOT NULL,
  `disk_capacity` INT NULL,
  `disk_interface` TINYINT NULL,
  `disk_speed` INT NULL,
  `comment` TEXT NULL,
  `disk_model` VARCHAR(45) NULL,
  `version` VARCHAR(45) NULL,
  `bandwidth` INT NULL,
  `iops` INT NULL,
  `disk_type` TINYINT NULL,
  `disk_cache` INT NULL,
  `disk_chip` VARCHAR(45) NULL,
  `disk_nand` INT NULL,
  `disk_nand_process` VARCHAR(45) NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_disk_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_disk_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_disk_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_disk_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_network_card`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_network_card` (
  `accessory_id` BIGINT NOT NULL,
  `speed` INT NULL,
  `network_card_interface` TINYINT NULL,
  `network_card_model` VARCHAR(45) NULL,
  `network_card_model` VARCHAR(45) NULL,
  `comment` TEXT NULL,
  `version` VARCHAR(45) NULL,
  `mac_address` VARCHAR(45) NULL,
  `network_card_iscsi_support` TINYINT NULL,
  `network_card_ncsi_support` TINYINT NULL,
  `network_card_pxe_support` TINYINT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_network_card_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_network_card_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_network_card_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_network_card_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_power`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_power` (
  `accessory_id` BIGINT NOT NULL,
  `power_model` VARCHAR(45) NULL,
  `power_specs` TINYINT NULL,
  `efficiency` INT NULL,
  `power_supply` TINYINT NULL,
  `version` VARCHAR(45) NULL,
  `brand_id` BIGINT NOT NULL,
  INDEX `fk_t_power_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_power_t_accessory1_idx` (`accessory_id` ASC),
  PRIMARY KEY (`accessory_id`),
  CONSTRAINT `fk_t_power_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_power_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_mother_board`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_mother_board` (
  `accessory_id` BIGINT NOT NULL,
  `mother_board_model` VARCHAR(45) NULL,
  `comment` TEXT NULL,
  `version` VARCHAR(45) NULL,
  `pci_num` INT NULL,
  `pcie_num` INT NULL,
  `sata_num` INT NULL,
  `sas_num` INT NULL,
  `m_2_num` INT NULL,
  `satadom_num` INT NULL,
  `lom_num` INT NULL,
  `dimm_num` INT NULL,
  `mother_board_chip` VARCHAR(45) NULL,
  `sd_support` TINYINT NULL,
  `sata_controller_support` TINYINT NULL,
  `sas_controller_support` TINYINT NULL,
  `usb_num` INT NULL,
  `double_bios_protection_support` TINYINT NULL,
  `asset_entry_support` TINYINT NULL,
  `command_bios_support` TINYINT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_mother_board_t_accessory_band_idx` (`brand_id` ASC),
  INDEX `fk_t_mother_board_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_mother_board_t_accessory_band`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_mother_board_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_array_card`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_array_card` (
  `accessory_id` BIGINT NOT NULL,
  `array_card_interface` TINYINT NULL,
  `array_card_cache` INT NULL,
  `array_card_buttery` TINYINT NULL,
  `comment` TEXT NULL,
  `version` VARCHAR(45) NULL,
  `cache_status` TINYINT NULL,
  `strip_size` INT NULL,
  `read_write_ratio` VARCHAR(45) NULL,
  `array_card_model` VARCHAR(45) NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_array_card_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_array_card_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_array_card_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_array_card_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_hba_card`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_hba_card` (
  `accessory_id` BIGINT NOT NULL,
  `hba_card_interface` TINYINT NULL,
  `comment` TEXT NULL,
  `version` VARCHAR(45) NULL,
  `hba_card_model` VARCHAR(45) NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_hba_card_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_hba_card_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_hba_card_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_hba_card_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_fan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_fan` (
  `accessory_id` BIGINT NOT NULL,
  `fan_redundancy_level` INT NULL,
  `fan_max_speed` INT NULL,
  `fan_auto_regulation_support` TINYINT NULL,
  `fan_position` TINYINT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_fan_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_fan_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_fan_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_fan_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_guide`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_guide` (
  `guide_id` INT NOT NULL,
  `comment` TEXT NULL,
  `used` INT NULL,
  `total_count` INT NULL,
  `guide_model` VARCHAR(45) NULL,
  PRIMARY KEY (`guide_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cmdb`.`t_gpu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmdb`.`t_gpu` (
  `accessory_id` BIGINT NOT NULL,
  `gpu_core_num` INT NULL,
  `gpu_memory` INT NULL,
  `gpu_frequency` INT NULL,
  `gpu_chip` VARCHAR(45) NULL,
  `gpu_memory_specs` VARCHAR(45) NULL,
  `gpu_power` INT NULL,
  `gpu_idle_power` INT NULL,
  `gpu_memory_bandwidth` INT NULL,
  `brand_id` BIGINT NOT NULL,
  PRIMARY KEY (`accessory_id`),
  INDEX `fk_t_gpu_t_accessory_band1_idx` (`brand_id` ASC),
  INDEX `fk_t_gpu_t_accessory1_idx` (`accessory_id` ASC),
  CONSTRAINT `fk_t_gpu_t_accessory_band1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `cmdb`.`t_accessory_band` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_gpu_t_accessory1`
    FOREIGN KEY (`accessory_id`)
    REFERENCES `cmdb`.`t_accessory` (`accessory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
