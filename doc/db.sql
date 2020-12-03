CREATE TABLE `kezhuanzhai` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `债券代码` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `交易场所` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `债券简称` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `申购日期` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `申购代码` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `正股代码` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `正股简称` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `债券面值` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '	',
  `发行价格` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '发行价格',
  `转股价` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `中签号发布日` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '中签号发布日	',
  `中签率` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `上市时间` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `备忘录` text CHARACTER SET utf8 COLLATE utf8_bin,
  `正股价` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `市场类型` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `股权登记日` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `申购上限` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '注意单位: 万元',
  `转股价值` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `债现价` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `转股溢价率` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '注意单位: %',
  `每股配售额` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `发行规模` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '注意单位: 亿元',
  PRIMARY KEY (`id`),
  UNIQUE KEY `债券代码_UNIQUE` (`债券代码`)
) ENGINE=MyISAM AUTO_INCREMENT=736 DEFAULT CHARSET=utf8;

CREATE TABLE `kezhuanzhai_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `open` decimal(10,2) DEFAULT NULL,
  `high` decimal(10,2) DEFAULT NULL,
  `low` decimal(10,2) DEFAULT NULL,
  `close` decimal(10,2) DEFAULT NULL,
  `volume` decimal(10,2) DEFAULT NULL,
  `bond_code` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=172333 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='可转债';



CREATE TABLE `kezhuanzhai_data_tmp` (
  `bond_code` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `open` decimal(10,2) DEFAULT NULL,
  `high` decimal(10,2) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `rank` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


-- 数据清理
insert into kezhuanzhai_data_tmp
select bond_code, `open`,`high`,`date`,
(
                CASE bond_code
                WHEN @curType
                THEN @curRow := @curRow + 1
                ELSE @curRow := 1 AND @curType := bond_code END
              )  AS rank
               from kezhuanzhai_data JOIN (SELECT @curRow := 0, @curType := '') r
  order by bond_code, `date`