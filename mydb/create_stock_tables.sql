-- -----------------------------------------------------
-- Table `research`.`stock_basic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `research`.`stock_basic` (
  `code` VARCHAR(45) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `exchange` VARCHAR(255) NOT NULL,
  `curr_type` VARCHAR(45) NULL,
  `market` VARCHAR(255) NOT NULL,
  `list_status` VARCHAR(45) NULL,
  `list_date` DATE NOT NULL,
  `delist_date` DATE NULL,
  `is_to_hk` VARCHAR(45) NULL,
  PRIMARY KEY (`code`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC),
  INDEX `market_IDX` (`market` ASC),
  INDEX `is_to_hk_IDX` (`is_to_hk` ASC),
  INDEX `exchange_IDX` (`exchange` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `research`.`trade_calendar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `research`.`trade_calendar` (
  `exchange` VARCHAR(255) NOT NULL,
  `cal_date` DATE NOT NULL,
  `pretrade_date` DATE NULL,
  `is_open` TINYINT(1) NOT NULL,
  INDEX `exchange_IDX` (`exchange` ASC),
  INDEX `cal_date_IDX` (`cal_date` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `research`.`stock_daily_quotes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `research`.`stock_daily_quotes` (
  `code` VARCHAR(45) NOT NULL,
  `trade_date` DATE NOT NULL,
  `open` DOUBLE NULL,
  `high` DOUBLE NULL,
  `low` DOUBLE NULL,
  `close` DOUBLE NULL,
  `pre_close` DOUBLE NULL,
  `change` DOUBLE NULL,
  `pct_chg` DOUBLE NULL,
  `vol` DOUBLE NULL,
  `amount` DOUBLE NULL,
  INDEX `code_IDX` (`code` ASC),
  INDEX `trade_date_IDX` (`trade_date` ASC),
  UNIQUE INDEX `code_trade_date_UNIQUE` (`code` ASC, `trade_date` ASC),
  CONSTRAINT `stock_basis_code`
    FOREIGN KEY (`code`)
    REFERENCES `research`.`stock_basic` (`code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `research`.`stock_adj_factor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `research`.`stock_adj_factor` (
  `code` VARCHAR(45) NOT NULL,
  `trade_date` DATE NOT NULL,
  `adj_factor` DOUBLE NULL,
  INDEX `code_IDX` (`code` ASC),
  INDEX `trade_date_IDX` (`trade_date` ASC),
  UNIQUE INDEX `code_trade_date_UNIQUE` (`code` ASC, `trade_date` ASC),
  CONSTRAINT `stock_daily_quotes_code_td`
    FOREIGN KEY (`code` , `trade_date`)
    REFERENCES `research`.`stock_daily_quotes` (`code` , `trade_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;