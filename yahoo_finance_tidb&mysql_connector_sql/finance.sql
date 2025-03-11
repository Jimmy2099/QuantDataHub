SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for financial_record
-- ----------------------------
DROP TABLE IF EXISTS `financial_record`;
CREATE TABLE `financial_record`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_id` bigint NULL DEFAULT NULL,
  `date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `amount` double NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30001 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for stock_code
-- ----------------------------
DROP TABLE IF EXISTS `stock_code`;
CREATE TABLE `stock_code`  (
  `Stock Code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Company Name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `Exchange` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Available` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Available',
  PRIMARY KEY (`Stock Code`, `Exchange`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for stock_market_data
-- ----------------------------
DROP TABLE IF EXISTS `stock_market_data`;
CREATE TABLE `stock_market_data`  (
  `Date` datetime NOT NULL,
  `Stock Code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Open` double NULL DEFAULT NULL,
  `High` double NULL DEFAULT NULL,
  `Low` double NULL DEFAULT NULL,
  `Close` double NULL DEFAULT NULL,
  `Adj Close` double NULL DEFAULT NULL,
  `Volume` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`Date`, `Stock Code`) USING BTREE,
  INDEX `ix_stock_market_data_Date`(`Date` ASC) USING BTREE,
  INDEX `stock_market_data_Date_idx`(`Date` ASC) USING BTREE,
  INDEX `stock_market_data_Stock Code_idx`(`Stock Code` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
