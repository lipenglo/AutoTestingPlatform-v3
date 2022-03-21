/*
 Navicat MySQL Data Transfer

 Source Server         : 192.168.2.38
 Source Server Type    : MySQL
 Source Server Version : 50727
 Source Host           : 192.168.2.38:3306
 Source Schema         : AutoTesting_v3

 Target Server Type    : MySQL
 Target Server Version : 50727
 File Encoding         : 65001

 Date: 09/02/2022 15:27:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for Api_BatchTask_apibatchtask
-- ----------------------------
DROP TABLE IF EXISTS `Api_BatchTask_apibatchtask`;
CREATE TABLE `Api_BatchTask_apibatchtask`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `batchName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `priority` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pushTo` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `hookId` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hookState` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_pid_id_e91ce8c6_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_BatchTask_apibatchtask_uid_id_2bce7e9c_fk_login_usertable_id`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_BatchTask_apibat_pid_id_e91ce8c6_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibatchtask_uid_id_2bce7e9c_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_BatchTask_apibatchtask
-- ----------------------------

-- ----------------------------
-- Table structure for Api_BatchTask_apibatchtaskhistory
-- ----------------------------
DROP TABLE IF EXISTS `Api_BatchTask_apibatchtaskhistory`;
CREATE TABLE `Api_BatchTask_apibatchtaskhistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `batchTask_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `batchName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_batchTask_id_e5c86996_fk_Api_Batch`(`batchTask_id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_uid_id_a20559fc_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_BatchTask_apibat_batchTask_id_e5c86996_fk_Api_Batch` FOREIGN KEY (`batchTask_id`) REFERENCES `Api_BatchTask_apibatchtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibat_uid_id_a20559fc_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_BatchTask_apibatchtaskhistory
-- ----------------------------

-- ----------------------------
-- Table structure for Api_BatchTask_apibatchtaskrunlog
-- ----------------------------
DROP TABLE IF EXISTS `Api_BatchTask_apibatchtaskrunlog`;
CREATE TABLE `Api_BatchTask_apibatchtaskrunlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `runType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `batchTask_id` int(11) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `versions` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_batchTask_id_68d6dc86_fk_Api_Batch`(`batchTask_id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_testReport_id_49969106_fk_Api_TestR`(`testReport_id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_uid_id_2e161111_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_BatchTask_apibat_batchTask_id_68d6dc86_fk_Api_Batch` FOREIGN KEY (`batchTask_id`) REFERENCES `Api_BatchTask_apibatchtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibat_testReport_id_49969106_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibat_uid_id_2e161111_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_BatchTask_apibatchtaskrunlog
-- ----------------------------

-- ----------------------------
-- Table structure for Api_BatchTask_apibatchtasktestset
-- ----------------------------
DROP TABLE IF EXISTS `Api_BatchTask_apibatchtasktestset`;
CREATE TABLE `Api_BatchTask_apibatchtasktestset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `batchTask_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_batchTask_id_426a80ba_fk_Api_Batch`(`batchTask_id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_task_id_a6db1c28_fk_Api_Timin`(`task_id`) USING BTREE,
  INDEX `Api_BatchTask_apibat_uid_id_db5f44d3_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_BatchTask_apibat_batchTask_id_426a80ba_fk_Api_Batch` FOREIGN KEY (`batchTask_id`) REFERENCES `Api_BatchTask_apibatchtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibat_task_id_a6db1c28_fk_Api_Timin` FOREIGN KEY (`task_id`) REFERENCES `Api_TimingTask_apitimingtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_BatchTask_apibat_uid_id_db5f44d3_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_BatchTask_apibatchtasktestset
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_apicasehistory
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_apicasehistory`;
CREATE TABLE `Api_CaseMaintenance_apicasehistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caseName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `case_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__case_id_bf5bfe9c_fk_Api_CaseM`(`case_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__fun_id_a6735c09_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__page_id_8196db08_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__pid_id_b5ce504d_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__uid_id_72e89898_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__case_id_bf5bfe9c_fk_Api_CaseM` FOREIGN KEY (`case_id`) REFERENCES `Api_CaseMaintenance_casebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__fun_id_a6735c09_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__page_id_8196db08_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__pid_id_b5ce504d_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__uid_id_72e89898_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_apicasehistory
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapibase
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapibase`;
CREATE TABLE `Api_CaseMaintenance_caseapibase`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requestType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `requestUrl` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `requestParamsType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `bodyRequestSaveType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_f2688f24_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_f2688f24_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 382 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapibase
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapibody
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapibody`;
CREATE TABLE `Api_CaseMaintenance_caseapibody`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `filePath` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `paramsType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_287b3d1b_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_287b3d1b_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 590 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapibody
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapiextract
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapiextract`;
CREATE TABLE `Api_CaseMaintenance_caseapiextract`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_ca2c95d4_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_ca2c95d4_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 277 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapiextract
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapiheaders
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapiheaders`;
CREATE TABLE `Api_CaseMaintenance_caseapiheaders`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_f3fb58e1_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_f3fb58e1_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 156 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapiheaders
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapioperation
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapioperation`;
CREATE TABLE `Api_CaseMaintenance_caseapioperation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `methodsName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dataBaseId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sql` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_147332a4_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_147332a4_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapioperation
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapiparams
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapiparams`;
CREATE TABLE `Api_CaseMaintenance_caseapiparams`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_726191e6_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_726191e6_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 176 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapiparams
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_caseapivalidate
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_caseapivalidate`;
CREATE TABLE `Api_CaseMaintenance_caseapivalidate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `checkName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `validateType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `valueType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expectedResults` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testSet_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__testSet_id_ef53de76_fk_Api_CaseM`(`testSet_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__testSet_id_ef53de76_fk_Api_CaseM` FOREIGN KEY (`testSet_id`) REFERENCES `Api_CaseMaintenance_casetestset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 183 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_caseapivalidate
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_casebasedata
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_casebasedata`;
CREATE TABLE `Api_CaseMaintenance_casebasedata`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `priority` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `caseName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `caseState` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `environmentId_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__environmentId_id_8dddf3c2_fk_PageEnvir`(`environmentId_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__fun_id_073979e4_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__page_id_1579dcf6_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__pid_id_bd41d314_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__uid_id_87597845_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__environmentId_id_8dddf3c2_fk_PageEnvir` FOREIGN KEY (`environmentId_id`) REFERENCES `PageEnvironment_pageenvironment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__fun_id_073979e4_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__page_id_1579dcf6_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__pid_id_bd41d314_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__uid_id_87597845_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 62 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_casebasedata
-- ----------------------------

-- ----------------------------
-- Table structure for Api_CaseMaintenance_casetestset
-- ----------------------------
DROP TABLE IF EXISTS `Api_CaseMaintenance_casetestset`;
CREATE TABLE `Api_CaseMaintenance_casetestset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `pluralIntId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `testName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_synchronous` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `caseId_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_CaseMaintenance__apiId_id_34007328_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__caseId_id_5f54f27b_fk_Api_CaseM`(`caseId_id`) USING BTREE,
  INDEX `Api_CaseMaintenance__uid_id_b7a73a63_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_CaseMaintenance__apiId_id_34007328_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__caseId_id_5f54f27b_fk_Api_CaseM` FOREIGN KEY (`caseId_id`) REFERENCES `Api_CaseMaintenance_casebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_CaseMaintenance__uid_id_b7a73a63_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 396 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_CaseMaintenance_casetestset
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apiassociateduser
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apiassociateduser`;
CREATE TABLE `Api_IntMaintenance_apiassociateduser`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `opertateInfo_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_468d2ad5_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_opertateInfo_id_6f0634b9_fk_info_oper`(`opertateInfo_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_uid_id_b8dca87f_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_468d2ad5_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_opertateInfo_id_6f0634b9_fk_info_oper` FOREIGN KEY (`opertateInfo_id`) REFERENCES `info_operateinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_uid_id_b8dca87f_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 181 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apiassociateduser
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apibasedata
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apibasedata`;
CREATE TABLE `Api_IntMaintenance_apibasedata`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apiName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `requestType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `requestUrl` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `requestParamsType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `bodyRequestSaveType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `apiState` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cuid` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `environment_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `requestUrlRadio` int(11) NOT NULL,
  `assignedToUser` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_environment_id_9e9156c1_fk_PageEnvir`(`environment_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_fun_id_430c0e8c_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_page_id_7ed062d5_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_pid_id_120ff661_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_uid_id_e953ce75_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_environment_id_9e9156c1_fk_PageEnvir` FOREIGN KEY (`environment_id`) REFERENCES `PageEnvironment_pageenvironment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_fun_id_430c0e8c_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_page_id_7ed062d5_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_pid_id_120ff661_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_uid_id_e953ce75_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 139 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apibasedata
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apibody
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apibody`;
CREATE TABLE `Api_IntMaintenance_apibody`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `paramsType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `filePath` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_f07aeba7_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_f07aeba7_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 244 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apibody
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apidynamic
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apidynamic`;
CREATE TABLE `Api_IntMaintenance_apidynamic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_read` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `case_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_c_apiId_id_63dff60f_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  INDEX `Api_IntMaintenance_c_case_id_51ef1537_fk_Api_CaseM`(`case_id`) USING BTREE,
  INDEX `Api_IntMaintenance_c_uid_id_dafa812a_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_c_apiId_id_63dff60f_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_c_case_id_51ef1537_fk_Api_CaseM` FOREIGN KEY (`case_id`) REFERENCES `Api_CaseMaintenance_casebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_c_uid_id_dafa812a_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apidynamic
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apiextract
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apiextract`;
CREATE TABLE `Api_IntMaintenance_apiextract`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_b9146bc5_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_b9146bc5_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 164 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apiextract
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apiheaders
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apiheaders`;
CREATE TABLE `Api_IntMaintenance_apiheaders`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_913d4a6a_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_913d4a6a_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 85 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apiheaders
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apihistory
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apihistory`;
CREATE TABLE `Api_IntMaintenance_apihistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apiName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `api_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `textInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_fun_id_eafc0836_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_page_id_2a5da8a5_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_pid_id_09a23557_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_api_id_6c878737_fk_Api_IntMa`(`api_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_api_id_6c878737_fk_Api_IntMa` FOREIGN KEY (`api_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_fun_id_eafc0836_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_page_id_2a5da8a5_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_IntMaintenance_a_pid_id_09a23557_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 299 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apihistory
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apioperation
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apioperation`;
CREATE TABLE `Api_IntMaintenance_apioperation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `methodsName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dataBaseId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sql` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_b97fbab6_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_b97fbab6_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 98 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apioperation
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apiparams
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apiparams`;
CREATE TABLE `Api_IntMaintenance_apiparams`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_046265cd_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_046265cd_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 286 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apiparams
-- ----------------------------

-- ----------------------------
-- Table structure for Api_IntMaintenance_apivalidate
-- ----------------------------
DROP TABLE IF EXISTS `Api_IntMaintenance_apivalidate`;
CREATE TABLE `Api_IntMaintenance_apivalidate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `checkName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `validateType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `valueType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expectedResults` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_IntMaintenance_a_apiId_id_dab845d1_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  CONSTRAINT `Api_IntMaintenance_a_apiId_id_dab845d1_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 130 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_IntMaintenance_apivalidate
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_apiqueue
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_apiqueue`;
CREATE TABLE `Api_TestReport_apiqueue`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskId` int(11) NOT NULL,
  `queueStatus` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `taskType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fun_id` int(11) NULL DEFAULT NULL,
  `page_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_apiqueue_uid_id_0771d08f_fk_login_usertable_id`(`uid_id`) USING BTREE,
  INDEX `Api_TestReport_apiqu_testReport_id_f9af0083_fk_Api_TestR`(`testReport_id`) USING BTREE,
  INDEX `Api_TestReport_apiqu_pid_id_3d2f4664_fk_ProjectMa`(`pid_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_apiqu_pid_id_3d2f4664_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_apiqu_testReport_id_f9af0083_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_apiqueue_uid_id_0771d08f_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 487 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_apiqueue
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_apireport
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_apireport`;
CREATE TABLE `Api_TestReport_apireport`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requestUrl` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `requestType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `requestHeaders` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `requestData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `reportStatus` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `statusCode` int(11) NULL DEFAULT NULL,
  `responseHeaders` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `responseInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `requestExtract` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `requestValidate` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `responseValidate` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `errorInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `runningTime` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `reportItem_id` int(11) NOT NULL,
  `preOperationInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `rearOperationInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_apire_reportItem_id_aed3c2b2_fk_Api_TestR`(`reportItem_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_apire_reportItem_id_aed3c2b2_fk_Api_TestR` FOREIGN KEY (`reportItem_id`) REFERENCES `Api_TestReport_apireportitem` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1201 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_apireport
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_apireportitem
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_apireportitem`;
CREATE TABLE `Api_TestReport_apireportitem`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apiName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `case_id` int(11) NULL DEFAULT NULL,
  `runningTime` double NULL DEFAULT NULL,
  `successTotal` int(11) NOT NULL,
  `failTotal` int(11) NOT NULL,
  `errorTotal` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `apiId_id` int(11) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  `batchItem_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_apire_apiId_id_49f86e5b_fk_Api_IntMa`(`apiId_id`) USING BTREE,
  INDEX `Api_TestReport_apire_testReport_id_1cee8dff_fk_Api_TestR`(`testReport_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_apire_apiId_id_49f86e5b_fk_Api_IntMa` FOREIGN KEY (`apiId_id`) REFERENCES `Api_IntMaintenance_apibasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_apire_testReport_id_1cee8dff_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1320 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_apireportitem
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_apireporttaskitem
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_apireporttaskitem`;
CREATE TABLE `Api_TestReport_apireporttaskitem`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `runningTime` double NULL DEFAULT NULL,
  `successTotal` int(11) NOT NULL,
  `failTotal` int(11) NOT NULL,
  `errorTotal` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_apire_task_id_88082242_fk_Api_Timin`(`task_id`) USING BTREE,
  INDEX `Api_TestReport_apire_testReport_id_843bd374_fk_Api_TestR`(`testReport_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_apire_task_id_88082242_fk_Api_Timin` FOREIGN KEY (`task_id`) REFERENCES `Api_TimingTask_apitimingtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_apire_testReport_id_843bd374_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_apireporttaskitem
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_apitestreport
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_apitestreport`;
CREATE TABLE `Api_TestReport_apitestreport`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reportName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reportType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `taskId` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `apiTotal` int(11) NOT NULL,
  `reportStatus` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `runningTime` double NULL DEFAULT NULL,
  `createTime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_apite_pid_id_712c402f_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_TestReport_apite_uid_id_6844d1e5_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_apite_pid_id_712c402f_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_apite_uid_id_6844d1e5_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 510 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_apitestreport
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_tempextractdata
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_tempextractdata`;
CREATE TABLE `Api_TestReport_tempextractdata`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `keys` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `values` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `valueType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `createTime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1313 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_tempextractdata
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TestReport_warninginfo
-- ----------------------------
DROP TABLE IF EXISTS `Api_TestReport_warninginfo`;
CREATE TABLE `Api_TestReport_warninginfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `triggerType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `taskId` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `taskName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `info` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `updateTime` datetime(6) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TestReport_warni_testReport_id_a909ebb3_fk_Api_TestR`(`testReport_id`) USING BTREE,
  INDEX `Api_TestReport_warninginfo_uid_id_82dc5cdc_fk_login_usertable_id`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_TestReport_warni_testReport_id_a909ebb3_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TestReport_warninginfo_uid_id_82dc5cdc_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TestReport_warninginfo
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TimingTask_apitimingtask
-- ----------------------------
DROP TABLE IF EXISTS `Api_TimingTask_apitimingtask`;
CREATE TABLE `Api_TimingTask_apitimingtask`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `timingConfig` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `priority` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pushTo` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `taskStatus` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `environment_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `periodicTask_id` int(11) NULL DEFAULT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_environment_id_bcda1949_fk_PageEnvir`(`environment_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_pid_id_89b1283e_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_uid_id_fb9e2876_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_TimingTask_apiti_environment_id_bcda1949_fk_PageEnvir` FOREIGN KEY (`environment_id`) REFERENCES `PageEnvironment_pageenvironment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_pid_id_89b1283e_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_uid_id_fb9e2876_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TimingTask_apitimingtask
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TimingTask_apitimingtaskhistory
-- ----------------------------
DROP TABLE IF EXISTS `Api_TimingTask_apitimingtaskhistory`;
CREATE TABLE `Api_TimingTask_apitimingtaskhistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `timingTask_id` int(11) NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `taskName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_timingTask_id_e95fe08c_fk_Api_Timin`(`timingTask_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_uid_id_6ce5a4c6_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Api_TimingTask_apiti_timingTask_id_e95fe08c_fk_Api_Timin` FOREIGN KEY (`timingTask_id`) REFERENCES `Api_TimingTask_apitimingtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_uid_id_6ce5a4c6_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 87 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TimingTask_apitimingtaskhistory
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TimingTask_apitimingtaskrunlog
-- ----------------------------
DROP TABLE IF EXISTS `Api_TimingTask_apitimingtaskrunlog`;
CREATE TABLE `Api_TimingTask_apitimingtaskrunlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `runType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `timingTask_id` int(11) NOT NULL,
  `testReport_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `taskName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_testReport_id_d70d2af6_fk_Api_TestR`(`testReport_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_uid_id_b8a78fb6_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_timingTask_id_4ed96a72_fk_Api_Timin`(`timingTask_id`) USING BTREE,
  CONSTRAINT `Api_TimingTask_apiti_testReport_id_d70d2af6_fk_Api_TestR` FOREIGN KEY (`testReport_id`) REFERENCES `Api_TestReport_apitestreport` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_timingTask_id_4ed96a72_fk_Api_Timin` FOREIGN KEY (`timingTask_id`) REFERENCES `Api_TimingTask_apitimingtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_uid_id_b8a78fb6_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TimingTask_apitimingtaskrunlog
-- ----------------------------

-- ----------------------------
-- Table structure for Api_TimingTask_apitimingtasktestset
-- ----------------------------
DROP TABLE IF EXISTS `Api_TimingTask_apitimingtasktestset`;
CREATE TABLE `Api_TimingTask_apitimingtasktestset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `timingTask_id` int(11) NOT NULL,
  `case_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_case_id_790ed1bf_fk_Api_CaseM`(`case_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_uid_id_2c5bcbde_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `Api_TimingTask_apiti_timingTask_id_0139edd3_fk_Api_Timin`(`timingTask_id`) USING BTREE,
  CONSTRAINT `Api_TimingTask_apiti_case_id_790ed1bf_fk_Api_CaseM` FOREIGN KEY (`case_id`) REFERENCES `Api_CaseMaintenance_casebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_timingTask_id_0139edd3_fk_Api_Timin` FOREIGN KEY (`timingTask_id`) REFERENCES `Api_TimingTask_apitimingtask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Api_TimingTask_apiti_uid_id_2c5bcbde_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 106 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Api_TimingTask_apitimingtasktestset
-- ----------------------------

-- ----------------------------
-- Table structure for DataBaseEnvironment_database
-- ----------------------------
DROP TABLE IF EXISTS `DataBaseEnvironment_database`;
CREATE TABLE `DataBaseEnvironment_database`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dbType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dataBaseIp` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `port` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `userName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `passWord` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `DataBaseEnvironment__uid_id_d8b6ddf6_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `DataBaseEnvironment__uid_id_d8b6ddf6_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of DataBaseEnvironment_database
-- ----------------------------

-- ----------------------------
-- Table structure for DebugTalk_debugtalk
-- ----------------------------
DROP TABLE IF EXISTS `DebugTalk_debugtalk`;
CREATE TABLE `DebugTalk_debugtalk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codeInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `updateTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `DebugTalk_debugtalk_uid_id_f0172e92_fk_login_usertable_id`(`uid_id`) USING BTREE,
  CONSTRAINT `DebugTalk_debugtalk_uid_id_f0172e92_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of DebugTalk_debugtalk
-- ----------------------------

-- ----------------------------
-- Table structure for FunManagement_funhistory
-- ----------------------------
DROP TABLE IF EXISTS `FunManagement_funhistory`;
CREATE TABLE `FunManagement_funhistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `funName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FunManagement_funhis_page_id_a2a8525f_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `FunManagement_funhis_pid_id_e463436b_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `FunManagement_funhis_fun_id_5a1adb0e_fk_FunManage`(`fun_id`) USING BTREE,
  CONSTRAINT `FunManagement_funhis_fun_id_5a1adb0e_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FunManagement_funhis_page_id_a2a8525f_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FunManagement_funhis_pid_id_e463436b_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of FunManagement_funhistory
-- ----------------------------
INSERT INTO `FunManagement_funhistory` VALUES (36, '测试功能', 'K8f31b27-tDa8s9Lo-489B56k2-F98Gu064', 'Add', '{\'sysType\': \'API\', \'proId\': \'133\', \'pageId\': \'28\', \'funName\': \'测试功能\', \'remarks\': \'\', \'updateTime\': \'2022-02-09 15:25:58\', \'createTime\': \'2022-02-09 15:25:58\', \'uid_id\': 3, \'cuid\': 3, \'onlyCode\': \'K8f31b27-tDa8s9Lo-489B56k2-F98Gu064\'}', '2022-02-09 15:25:58.277629', 28, 133, 17, 3);

-- ----------------------------
-- Table structure for FunManagement_funmanagement
-- ----------------------------
DROP TABLE IF EXISTS `FunManagement_funmanagement`;
CREATE TABLE `FunManagement_funmanagement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `funName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FunManagement_funman_page_id_df3ec0dd_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `FunManagement_funman_pid_id_20e8a54b_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `FunManagement_funman_uid_id_3150b7bf_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `FunManagement_funman_page_id_df3ec0dd_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FunManagement_funman_pid_id_20e8a54b_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FunManagement_funman_uid_id_3150b7bf_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of FunManagement_funmanagement
-- ----------------------------
INSERT INTO `FunManagement_funmanagement` VALUES (17, '测试功能', '', '2022-02-09 15:25:58.266632', '2022-02-09 15:25:58.266685', 3, 0, 28, 133, 3, 'API', 'K8f31b27-tDa8s9Lo-489B56k2-F98Gu064');

-- ----------------------------
-- Table structure for GlobalVariable_globalvariable
-- ----------------------------
DROP TABLE IF EXISTS `GlobalVariable_globalvariable`;
CREATE TABLE `GlobalVariable_globalvariable`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `globalType` int(11) NOT NULL,
  `globalName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `globalValue` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `GlobalVariable_globa_uid_id_4cd25a8b_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `GlobalVariable_globa_pid_id_5e11f04d_fk_ProjectMa`(`pid_id`) USING BTREE,
  CONSTRAINT `GlobalVariable_globa_pid_id_5e11f04d_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `GlobalVariable_globa_uid_id_4cd25a8b_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of GlobalVariable_globalvariable
-- ----------------------------

-- ----------------------------
-- Table structure for Notice_noticeinfo
-- ----------------------------
DROP TABLE IF EXISTS `Notice_noticeinfo`;
CREATE TABLE `Notice_noticeinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `abstract` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Notice_noticeinfo_uid_id_7aab5bcd_fk_login_usertable_id`(`uid_id`) USING BTREE,
  CONSTRAINT `Notice_noticeinfo_uid_id_7aab5bcd_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Notice_noticeinfo
-- ----------------------------
INSERT INTO `Notice_noticeinfo` VALUES (7, '测试公告', '我是测试公告哦！', 1, '2022-02-09 15:24:56.738916', '2022-02-09 15:24:56.738953', 3, 0, 3);

-- ----------------------------
-- Table structure for PageEnvironment_pageenvironment
-- ----------------------------
DROP TABLE IF EXISTS `PageEnvironment_pageenvironment`;
CREATE TABLE `PageEnvironment_pageenvironment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `environmentName` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `environmentUrl` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `PageEnvironment_page_pid_id_33e6d93a_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `PageEnvironment_page_uid_id_f409878e_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `PageEnvironment_page_pid_id_33e6d93a_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `PageEnvironment_page_uid_id_f409878e_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of PageEnvironment_pageenvironment
-- ----------------------------

-- ----------------------------
-- Table structure for PageManagement_pagehistory
-- ----------------------------
DROP TABLE IF EXISTS `PageManagement_pagehistory`;
CREATE TABLE `PageManagement_pagehistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pageName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `PageManagement_pageh_page_id_1c33dfe7_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `PageManagement_pageh_pid_id_623be95f_fk_ProjectMa`(`pid_id`) USING BTREE,
  CONSTRAINT `PageManagement_pageh_page_id_1c33dfe7_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `PageManagement_pageh_pid_id_623be95f_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of PageManagement_pagehistory
-- ----------------------------
INSERT INTO `PageManagement_pagehistory` VALUES (49, '测试页面', 'plYt2aPL-8sn960Wm-oCF7KJ23-Sh6C3819', 'Add', '{\'sysType\': \'API\', \'proId\': \'133\', \'pageName\': \'测试页面\', \'remarks\': \'\', \'updateTime\': \'2022-02-09 15:25:52\', \'createTime\': \'2022-02-09 15:25:52\', \'uid_id\': 3, \'cuid\': 3, \'onlyCode\': \'BWNE6LGl-y379564T-314WH86f-Qe7t61w9\'}', '2022-02-09 15:25:52.576872', 28, 133, 3);

-- ----------------------------
-- Table structure for PageManagement_pagemanagement
-- ----------------------------
DROP TABLE IF EXISTS `PageManagement_pagemanagement`;
CREATE TABLE `PageManagement_pagemanagement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pageName` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remarks` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `PageManagement_pagem_pid_id_0f344251_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `PageManagement_pagem_uid_id_b8e07ed1_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `PageManagement_pagem_pid_id_0f344251_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `PageManagement_pagem_uid_id_b8e07ed1_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of PageManagement_pagemanagement
-- ----------------------------
INSERT INTO `PageManagement_pagemanagement` VALUES (28, '测试页面', '', '2022-02-09 15:25:52.573080', '2022-02-09 15:25:52.573106', 3, 0, 133, 3, 'API', 'BWNE6LGl-y379564T-314WH86f-Qe7t61w9');

-- ----------------------------
-- Table structure for ProjectManagement_probindmembers
-- ----------------------------
DROP TABLE IF EXISTS `ProjectManagement_probindmembers`;
CREATE TABLE `ProjectManagement_probindmembers`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updateTime` datetime(6) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ProjectManagement_pr_pid_id_5c3510a5_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `ProjectManagement_pr_uid_id_6eddd0b0_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `ProjectManagement_pr_role_id_bc036e0a_fk_role_basi`(`role_id`) USING BTREE,
  CONSTRAINT `ProjectManagement_pr_pid_id_5c3510a5_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ProjectManagement_pr_role_id_bc036e0a_fk_role_basi` FOREIGN KEY (`role_id`) REFERENCES `role_basicrole` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ProjectManagement_pr_uid_id_6eddd0b0_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 138 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ProjectManagement_probindmembers
-- ----------------------------
INSERT INTO `ProjectManagement_probindmembers` VALUES (137, '2022-02-09 15:25:14.305663', '2022-02-09 15:25:14.305685', 0, 133, 3, 1);

-- ----------------------------
-- Table structure for ProjectManagement_prohistory
-- ----------------------------
DROP TABLE IF EXISTS `ProjectManagement_prohistory`;
CREATE TABLE `ProjectManagement_prohistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `proName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 232 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ProjectManagement_prohistory
-- ----------------------------
INSERT INTO `ProjectManagement_prohistory` VALUES (231, '0wZU8TkP-39O0YjW1-29UAim15-568cK734', 'Add', '{\'sysType\': \'API\', \'proName\': \'测试项目\', \'remarks\': \'\', \'updateTime\': \'2022-02-09 15:25:14\', \'createTime\': \'2022-02-09 15:25:14\', \'uid_id\': 3, \'cuid\': 3, \'onlyCode\': \'0wZU8TkP-39O0YjW1-29UAim15-568cK734\'}', '2022-02-09 15:25:14.307059', '测试项目', 133, 3);

-- ----------------------------
-- Table structure for ProjectManagement_promanagement
-- ----------------------------
DROP TABLE IF EXISTS `ProjectManagement_promanagement`;
CREATE TABLE `ProjectManagement_promanagement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `proName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `updateTime` datetime(6) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `cuid` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ProjectManagement_pr_uid_id_4fa2c551_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `ProjectManagement_pr_uid_id_4fa2c551_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 134 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ProjectManagement_promanagement
-- ----------------------------
INSERT INTO `ProjectManagement_promanagement` VALUES (133, 'API', '测试项目', '', '2022-02-09 15:25:14.297164', '2022-02-09 15:25:14.297191', 0, 3, 3, '0wZU8TkP-39O0YjW1-29UAim15-568cK734');

-- ----------------------------
-- Table structure for SystemParams_systemparams
-- ----------------------------
DROP TABLE IF EXISTS `SystemParams_systemparams`;
CREATE TABLE `SystemParams_systemparams`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `keyName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `valueType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `remarks` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `label` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `SystemParams_systemparams_uid_id_2a59cb4c_fk_login_usertable_id`(`uid_id`) USING BTREE,
  CONSTRAINT `SystemParams_systemparams_uid_id_2a59cb4c_fk_login_usertable_id` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of SystemParams_systemparams
-- ----------------------------
INSERT INTO `SystemParams_systemparams` VALUES (1, 'API', 'RequestTimeOut', '10', 'Input', '2022-01-13 17:11:35.000000', 3, '核心接口请求超时时间', 'Request');
INSERT INTO `SystemParams_systemparams` VALUES (2, 'API', 'EmailUser', 'lipenglo@163.com', 'Input', '2022-01-13 17:42:12.000000', 3, '推送邮件用户', 'Email');
INSERT INTO `SystemParams_systemparams` VALUES (3, 'API', 'EmailPwd', 'li123123', 'Input', '2022-01-13 17:42:34.000000', 3, '推送邮件密码', 'Email');
INSERT INTO `SystemParams_systemparams` VALUES (4, 'API', 'SmtpServer', 'smtp.163.com', 'Input', '2022-01-13 17:50:35.000000', 3, 'smtp', 'Email');

-- ----------------------------
-- Table structure for Ui_CaseMaintenance_uiassociatedpage
-- ----------------------------
DROP TABLE IF EXISTS `Ui_CaseMaintenance_uiassociatedpage`;
CREATE TABLE `Ui_CaseMaintenance_uiassociatedpage`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `case_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_case_id_768c0870_fk_Ui_CaseMa`(`case_id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_page_id_e0002c8f_fk_PageManag`(`page_id`) USING BTREE,
  CONSTRAINT `Ui_CaseMaintenance_u_case_id_768c0870_fk_Ui_CaseMa` FOREIGN KEY (`case_id`) REFERENCES `Ui_CaseMaintenance_uicasebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_CaseMaintenance_u_page_id_e0002c8f_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_CaseMaintenance_uiassociatedpage
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_CaseMaintenance_uicasebasedata
-- ----------------------------
DROP TABLE IF EXISTS `Ui_CaseMaintenance_uicasebasedata`;
CREATE TABLE `Ui_CaseMaintenance_uicasebasedata`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `priority` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `caseName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `caseState` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `environmentId_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_environmentId_id_00f0eadb_fk_PageEnvir`(`environmentId_id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_fun_id_61ec9605_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_page_id_715d61c0_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_pid_id_deab937c_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_uid_id_3e0c7ef8_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Ui_CaseMaintenance_u_environmentId_id_00f0eadb_fk_PageEnvir` FOREIGN KEY (`environmentId_id`) REFERENCES `PageEnvironment_pageenvironment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_CaseMaintenance_u_fun_id_61ec9605_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_CaseMaintenance_u_page_id_715d61c0_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_CaseMaintenance_u_pid_id_deab937c_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_CaseMaintenance_u_uid_id_3e0c7ef8_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_CaseMaintenance_uicasebasedata
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_CaseMaintenance_uioperationset
-- ----------------------------
DROP TABLE IF EXISTS `Ui_CaseMaintenance_uioperationset`;
CREATE TABLE `Ui_CaseMaintenance_uioperationset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `methodsName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `dataBaseId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `caseId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `case_id` int(11) NOT NULL,
  `sql` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_case_id_c254e9eb_fk_Ui_CaseMa`(`case_id`) USING BTREE,
  CONSTRAINT `Ui_CaseMaintenance_u_case_id_c254e9eb_fk_Ui_CaseMa` FOREIGN KEY (`case_id`) REFERENCES `Ui_CaseMaintenance_uicasebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_CaseMaintenance_uioperationset
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_CaseMaintenance_uitestset
-- ----------------------------
DROP TABLE IF EXISTS `Ui_CaseMaintenance_uitestset`;
CREATE TABLE `Ui_CaseMaintenance_uitestset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `eventName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `elementId` int(11) NULL DEFAULT NULL,
  `elementType` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `inputData` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `assertType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `assertValueType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `assertValue` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `case_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_CaseMaintenance_u_case_id_1832b4f0_fk_Ui_CaseMa`(`case_id`) USING BTREE,
  CONSTRAINT `Ui_CaseMaintenance_u_case_id_1832b4f0_fk_Ui_CaseMa` FOREIGN KEY (`case_id`) REFERENCES `Ui_CaseMaintenance_uicasebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_CaseMaintenance_uitestset
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementEvent_elementevent
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementEvent_elementevent`;
CREATE TABLE `Ui_ElementEvent_elementevent`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eventName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `updateTime` datetime(6) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `eventLogo` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `index` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementEvent_elem_uid_id_6e2d463f_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Ui_ElementEvent_elem_uid_id_6e2d463f_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementEvent_elementevent
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementEvent_elementeventcomponent
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementEvent_elementeventcomponent`;
CREATE TABLE `Ui_ElementEvent_elementeventcomponent`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `label` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `event_id` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementEvent_elem_event_id_ee895710_fk_Ui_Elemen`(`event_id`) USING BTREE,
  CONSTRAINT `Ui_ElementEvent_elem_event_id_ee895710_fk_Ui_Elemen` FOREIGN KEY (`event_id`) REFERENCES `Ui_ElementEvent_elementevent` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementEvent_elementeventcomponent
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementMaintenance_elementbasedata
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementMaintenance_elementbasedata`;
CREATE TABLE `Ui_ElementMaintenance_elementbasedata`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `elementName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cuid` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `is_del` int(11) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `elementType` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `elementState` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_fun_id_08c4ec53_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_page_id_5222d10b_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_pid_id_b5010b32_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_uid_id_5366483a_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Ui_ElementMaintenanc_fun_id_08c4ec53_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_page_id_5222d10b_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_pid_id_b5010b32_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_uid_id_5366483a_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementMaintenance_elementbasedata
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementMaintenance_elementdynamic
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementMaintenance_elementdynamic`;
CREATE TABLE `Ui_ElementMaintenance_elementdynamic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_read` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `case_id` int(11) NOT NULL,
  `element_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_case_id_acf03d4a_fk_Ui_CaseMa`(`case_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_element_id_272adb0a_fk_Ui_Elemen`(`element_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_uid_id_3edeacad_fk_login_use`(`uid_id`) USING BTREE,
  CONSTRAINT `Ui_ElementMaintenanc_case_id_acf03d4a_fk_Ui_CaseMa` FOREIGN KEY (`case_id`) REFERENCES `Ui_CaseMaintenance_uicasebasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_element_id_272adb0a_fk_Ui_Elemen` FOREIGN KEY (`element_id`) REFERENCES `Ui_ElementMaintenance_elementbasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_uid_id_3edeacad_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementMaintenance_elementdynamic
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementMaintenance_elementhistory
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementMaintenance_elementhistory`;
CREATE TABLE `Ui_ElementMaintenance_elementhistory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `elementName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `restoreData` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `element_id` int(11) NOT NULL,
  `textInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_fun_id_89c8feed_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_page_id_c46f8a6a_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_pid_id_74450e04_fk_ProjectMa`(`pid_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_uid_id_4eac6adb_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_element_id_c9005ba6_fk_Ui_Elemen`(`element_id`) USING BTREE,
  CONSTRAINT `Ui_ElementMaintenanc_element_id_c9005ba6_fk_Ui_Elemen` FOREIGN KEY (`element_id`) REFERENCES `Ui_ElementMaintenance_elementbasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_fun_id_89c8feed_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_page_id_c46f8a6a_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_pid_id_74450e04_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `Ui_ElementMaintenanc_uid_id_4eac6adb_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementMaintenance_elementhistory
-- ----------------------------

-- ----------------------------
-- Table structure for Ui_ElementMaintenance_elementlocation
-- ----------------------------
DROP TABLE IF EXISTS `Ui_ElementMaintenance_elementlocation`;
CREATE TABLE `Ui_ElementMaintenance_elementlocation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `targetingType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `targetingPath` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `remarks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `state` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `onlyCode` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `element_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `Ui_ElementMaintenanc_element_id_a99eeb98_fk_Ui_Elemen`(`element_id`) USING BTREE,
  CONSTRAINT `Ui_ElementMaintenanc_element_id_a99eeb98_fk_Ui_Elemen` FOREIGN KEY (`element_id`) REFERENCES `Ui_ElementMaintenance_elementbasedata` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of Ui_ElementMaintenance_elementlocation
-- ----------------------------

-- ----------------------------
-- Table structure for WorkorderManagement_historyinfo
-- ----------------------------
DROP TABLE IF EXISTS `WorkorderManagement_historyinfo`;
CREATE TABLE `WorkorderManagement_historyinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `WorkorderManagement__uid_id_78491892_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `WorkorderManagement__work_id_7ddd33d2_fk_Workorder`(`work_id`) USING BTREE,
  CONSTRAINT `WorkorderManagement__uid_id_78491892_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__work_id_7ddd33d2_fk_Workorder` FOREIGN KEY (`work_id`) REFERENCES `WorkorderManagement_workordermanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 75 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of WorkorderManagement_historyinfo
-- ----------------------------

-- ----------------------------
-- Table structure for WorkorderManagement_workbindpushtousers
-- ----------------------------
DROP TABLE IF EXISTS `WorkorderManagement_workbindpushtousers`;
CREATE TABLE `WorkorderManagement_workbindpushtousers`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_del` int(11) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `WorkorderManagement__uid_id_ff8aa248_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `WorkorderManagement__work_id_411f6a3f_fk_Workorder`(`work_id`) USING BTREE,
  CONSTRAINT `WorkorderManagement__uid_id_ff8aa248_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__work_id_411f6a3f_fk_Workorder` FOREIGN KEY (`work_id`) REFERENCES `WorkorderManagement_workordermanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 279 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of WorkorderManagement_workbindpushtousers
-- ----------------------------

-- ----------------------------
-- Table structure for WorkorderManagement_worklifecycle
-- ----------------------------
DROP TABLE IF EXISTS `WorkorderManagement_worklifecycle`;
CREATE TABLE `WorkorderManagement_worklifecycle`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operationInfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `updateTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  `operationType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workState` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `WorkorderManagement__uid_id_095d37ba_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `WorkorderManagement__work_id_04313ee7_fk_Workorder`(`work_id`) USING BTREE,
  CONSTRAINT `WorkorderManagement__uid_id_095d37ba_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__work_id_04313ee7_fk_Workorder` FOREIGN KEY (`work_id`) REFERENCES `WorkorderManagement_workordermanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 215 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of WorkorderManagement_worklifecycle
-- ----------------------------

-- ----------------------------
-- Table structure for WorkorderManagement_workordermanagement
-- ----------------------------
DROP TABLE IF EXISTS `WorkorderManagement_workordermanagement`;
CREATE TABLE `WorkorderManagement_workordermanagement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workState` int(11) NOT NULL,
  `workName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `cuid` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `fun_id` int(11) NOT NULL,
  `page_id` int(11) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `workSource` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `WorkorderManagement__uid_id_5d4e860b_fk_login_use`(`uid_id`) USING BTREE,
  INDEX `WorkorderManagement__fun_id_1cb6cdbb_fk_FunManage`(`fun_id`) USING BTREE,
  INDEX `WorkorderManagement__page_id_054b1817_fk_PageManag`(`page_id`) USING BTREE,
  INDEX `WorkorderManagement__pid_id_4d406c8d_fk_ProjectMa`(`pid_id`) USING BTREE,
  CONSTRAINT `WorkorderManagement__fun_id_1cb6cdbb_fk_FunManage` FOREIGN KEY (`fun_id`) REFERENCES `FunManagement_funmanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__page_id_054b1817_fk_PageManag` FOREIGN KEY (`page_id`) REFERENCES `PageManagement_pagemanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__pid_id_4d406c8d_fk_ProjectMa` FOREIGN KEY (`pid_id`) REFERENCES `ProjectManagement_promanagement` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `WorkorderManagement__uid_id_5d4e860b_fk_login_use` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 129 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of WorkorderManagement_workordermanagement
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 365 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add Token', 7, 'add_token');
INSERT INTO `auth_permission` VALUES (26, 'Can change Token', 7, 'change_token');
INSERT INTO `auth_permission` VALUES (27, 'Can delete Token', 7, 'delete_token');
INSERT INTO `auth_permission` VALUES (28, 'Can view Token', 7, 'view_token');
INSERT INTO `auth_permission` VALUES (29, 'Can add token', 8, 'add_tokenproxy');
INSERT INTO `auth_permission` VALUES (30, 'Can change token', 8, 'change_tokenproxy');
INSERT INTO `auth_permission` VALUES (31, 'Can delete token', 8, 'delete_tokenproxy');
INSERT INTO `auth_permission` VALUES (32, 'Can view token', 8, 'view_tokenproxy');
INSERT INTO `auth_permission` VALUES (33, 'Can add user table', 9, 'add_usertable');
INSERT INTO `auth_permission` VALUES (34, 'Can change user table', 9, 'change_usertable');
INSERT INTO `auth_permission` VALUES (35, 'Can delete user table', 9, 'delete_usertable');
INSERT INTO `auth_permission` VALUES (36, 'Can view user table', 9, 'view_usertable');
INSERT INTO `auth_permission` VALUES (37, 'Can add error msg', 10, 'add_errormsg');
INSERT INTO `auth_permission` VALUES (38, 'Can change error msg', 10, 'change_errormsg');
INSERT INTO `auth_permission` VALUES (39, 'Can delete error msg', 10, 'delete_errormsg');
INSERT INTO `auth_permission` VALUES (40, 'Can view error msg', 10, 'view_errormsg');
INSERT INTO `auth_permission` VALUES (41, 'Can add error msg', 11, 'add_errormsg');
INSERT INTO `auth_permission` VALUES (42, 'Can change error msg', 11, 'change_errormsg');
INSERT INTO `auth_permission` VALUES (43, 'Can delete error msg', 11, 'delete_errormsg');
INSERT INTO `auth_permission` VALUES (44, 'Can view error msg', 11, 'view_errormsg');
INSERT INTO `auth_permission` VALUES (45, 'Can add error info', 11, 'add_errorinfo');
INSERT INTO `auth_permission` VALUES (46, 'Can change error info', 11, 'change_errorinfo');
INSERT INTO `auth_permission` VALUES (47, 'Can delete error info', 11, 'delete_errorinfo');
INSERT INTO `auth_permission` VALUES (48, 'Can view error info', 11, 'view_errorinfo');
INSERT INTO `auth_permission` VALUES (49, 'Can add operate info', 12, 'add_operateinfo');
INSERT INTO `auth_permission` VALUES (50, 'Can change operate info', 12, 'change_operateinfo');
INSERT INTO `auth_permission` VALUES (51, 'Can delete operate info', 12, 'delete_operateinfo');
INSERT INTO `auth_permission` VALUES (52, 'Can view operate info', 12, 'view_operateinfo');
INSERT INTO `auth_permission` VALUES (53, 'Can add router', 13, 'add_router');
INSERT INTO `auth_permission` VALUES (54, 'Can change router', 13, 'change_router');
INSERT INTO `auth_permission` VALUES (55, 'Can delete router', 13, 'delete_router');
INSERT INTO `auth_permission` VALUES (56, 'Can view router', 13, 'view_router');
INSERT INTO `auth_permission` VALUES (57, 'Can add basic role', 14, 'add_basicrole');
INSERT INTO `auth_permission` VALUES (58, 'Can change basic role', 14, 'change_basicrole');
INSERT INTO `auth_permission` VALUES (59, 'Can delete basic role', 14, 'delete_basicrole');
INSERT INTO `auth_permission` VALUES (60, 'Can view basic role', 14, 'view_basicrole');
INSERT INTO `auth_permission` VALUES (61, 'Can add role bind menu', 15, 'add_rolebindmenu');
INSERT INTO `auth_permission` VALUES (62, 'Can change role bind menu', 15, 'change_rolebindmenu');
INSERT INTO `auth_permission` VALUES (63, 'Can delete role bind menu', 15, 'delete_rolebindmenu');
INSERT INTO `auth_permission` VALUES (64, 'Can view role bind menu', 15, 'view_rolebindmenu');
INSERT INTO `auth_permission` VALUES (65, 'Can add user bind role', 16, 'add_userbindrole');
INSERT INTO `auth_permission` VALUES (66, 'Can change user bind role', 16, 'change_userbindrole');
INSERT INTO `auth_permission` VALUES (67, 'Can delete user bind role', 16, 'delete_userbindrole');
INSERT INTO `auth_permission` VALUES (68, 'Can view user bind role', 16, 'view_userbindrole');
INSERT INTO `auth_permission` VALUES (69, 'Can add push info', 17, 'add_pushinfo');
INSERT INTO `auth_permission` VALUES (70, 'Can change push info', 17, 'change_pushinfo');
INSERT INTO `auth_permission` VALUES (71, 'Can delete push info', 17, 'delete_pushinfo');
INSERT INTO `auth_permission` VALUES (72, 'Can view push info', 17, 'view_pushinfo');
INSERT INTO `auth_permission` VALUES (73, 'Can add pro management', 18, 'add_promanagement');
INSERT INTO `auth_permission` VALUES (74, 'Can change pro management', 18, 'change_promanagement');
INSERT INTO `auth_permission` VALUES (75, 'Can delete pro management', 18, 'delete_promanagement');
INSERT INTO `auth_permission` VALUES (76, 'Can view pro management', 18, 'view_promanagement');
INSERT INTO `auth_permission` VALUES (77, 'Can add pro bind members', 19, 'add_probindmembers');
INSERT INTO `auth_permission` VALUES (78, 'Can change pro bind members', 19, 'change_probindmembers');
INSERT INTO `auth_permission` VALUES (79, 'Can delete pro bind members', 19, 'delete_probindmembers');
INSERT INTO `auth_permission` VALUES (80, 'Can view pro bind members', 19, 'view_probindmembers');
INSERT INTO `auth_permission` VALUES (81, 'Can add page management', 20, 'add_pagemanagement');
INSERT INTO `auth_permission` VALUES (82, 'Can change page management', 20, 'change_pagemanagement');
INSERT INTO `auth_permission` VALUES (83, 'Can delete page management', 20, 'delete_pagemanagement');
INSERT INTO `auth_permission` VALUES (84, 'Can view page management', 20, 'view_pagemanagement');
INSERT INTO `auth_permission` VALUES (85, 'Can add fun management', 21, 'add_funmanagement');
INSERT INTO `auth_permission` VALUES (86, 'Can change fun management', 21, 'change_funmanagement');
INSERT INTO `auth_permission` VALUES (87, 'Can delete fun management', 21, 'delete_funmanagement');
INSERT INTO `auth_permission` VALUES (88, 'Can view fun management', 21, 'view_funmanagement');
INSERT INTO `auth_permission` VALUES (89, 'Can add workorder management', 22, 'add_workordermanagement');
INSERT INTO `auth_permission` VALUES (90, 'Can change workorder management', 22, 'change_workordermanagement');
INSERT INTO `auth_permission` VALUES (91, 'Can delete workorder management', 22, 'delete_workordermanagement');
INSERT INTO `auth_permission` VALUES (92, 'Can view workorder management', 22, 'view_workordermanagement');
INSERT INTO `auth_permission` VALUES (93, 'Can add work bind push to users', 23, 'add_workbindpushtousers');
INSERT INTO `auth_permission` VALUES (94, 'Can change work bind push to users', 23, 'change_workbindpushtousers');
INSERT INTO `auth_permission` VALUES (95, 'Can delete work bind push to users', 23, 'delete_workbindpushtousers');
INSERT INTO `auth_permission` VALUES (96, 'Can view work bind push to users', 23, 'view_workbindpushtousers');
INSERT INTO `auth_permission` VALUES (97, 'Can add work life cycle', 24, 'add_worklifecycle');
INSERT INTO `auth_permission` VALUES (98, 'Can change work life cycle', 24, 'change_worklifecycle');
INSERT INTO `auth_permission` VALUES (99, 'Can delete work life cycle', 24, 'delete_worklifecycle');
INSERT INTO `auth_permission` VALUES (100, 'Can view work life cycle', 24, 'view_worklifecycle');
INSERT INTO `auth_permission` VALUES (101, 'Can add page environment', 25, 'add_pageenvironment');
INSERT INTO `auth_permission` VALUES (102, 'Can change page environment', 25, 'change_pageenvironment');
INSERT INTO `auth_permission` VALUES (103, 'Can delete page environment', 25, 'delete_pageenvironment');
INSERT INTO `auth_permission` VALUES (104, 'Can view page environment', 25, 'view_pageenvironment');
INSERT INTO `auth_permission` VALUES (105, 'Can add api base data', 26, 'add_apibasedata');
INSERT INTO `auth_permission` VALUES (106, 'Can change api base data', 26, 'change_apibasedata');
INSERT INTO `auth_permission` VALUES (107, 'Can delete api base data', 26, 'delete_apibasedata');
INSERT INTO `auth_permission` VALUES (108, 'Can view api base data', 26, 'view_apibasedata');
INSERT INTO `auth_permission` VALUES (109, 'Can add history', 27, 'add_history');
INSERT INTO `auth_permission` VALUES (110, 'Can change history', 27, 'change_history');
INSERT INTO `auth_permission` VALUES (111, 'Can delete history', 27, 'delete_history');
INSERT INTO `auth_permission` VALUES (112, 'Can view history', 27, 'view_history');
INSERT INTO `auth_permission` VALUES (113, 'Can add api headers', 28, 'add_apiheaders');
INSERT INTO `auth_permission` VALUES (114, 'Can change api headers', 28, 'change_apiheaders');
INSERT INTO `auth_permission` VALUES (115, 'Can delete api headers', 28, 'delete_apiheaders');
INSERT INTO `auth_permission` VALUES (116, 'Can view api headers', 28, 'view_apiheaders');
INSERT INTO `auth_permission` VALUES (117, 'Can add api params', 29, 'add_apiparams');
INSERT INTO `auth_permission` VALUES (118, 'Can change api params', 29, 'change_apiparams');
INSERT INTO `auth_permission` VALUES (119, 'Can delete api params', 29, 'delete_apiparams');
INSERT INTO `auth_permission` VALUES (120, 'Can view api params', 29, 'view_apiparams');
INSERT INTO `auth_permission` VALUES (121, 'Can add api body', 30, 'add_apibody');
INSERT INTO `auth_permission` VALUES (122, 'Can change api body', 30, 'change_apibody');
INSERT INTO `auth_permission` VALUES (123, 'Can delete api body', 30, 'delete_apibody');
INSERT INTO `auth_permission` VALUES (124, 'Can view api body', 30, 'view_apibody');
INSERT INTO `auth_permission` VALUES (125, 'Can add api extract', 31, 'add_apiextract');
INSERT INTO `auth_permission` VALUES (126, 'Can change api extract', 31, 'change_apiextract');
INSERT INTO `auth_permission` VALUES (127, 'Can delete api extract', 31, 'delete_apiextract');
INSERT INTO `auth_permission` VALUES (128, 'Can view api extract', 31, 'view_apiextract');
INSERT INTO `auth_permission` VALUES (129, 'Can add api validate', 32, 'add_apivalidate');
INSERT INTO `auth_permission` VALUES (130, 'Can change api validate', 32, 'change_apivalidate');
INSERT INTO `auth_permission` VALUES (131, 'Can delete api validate', 32, 'delete_apivalidate');
INSERT INTO `auth_permission` VALUES (132, 'Can view api validate', 32, 'view_apivalidate');
INSERT INTO `auth_permission` VALUES (133, 'Can add api operation', 33, 'add_apioperation');
INSERT INTO `auth_permission` VALUES (134, 'Can change api operation', 33, 'change_apioperation');
INSERT INTO `auth_permission` VALUES (135, 'Can delete api operation', 33, 'delete_apioperation');
INSERT INTO `auth_permission` VALUES (136, 'Can view api operation', 33, 'view_apioperation');
INSERT INTO `auth_permission` VALUES (137, 'Can add temp extract data', 34, 'add_tempextractdata');
INSERT INTO `auth_permission` VALUES (138, 'Can change temp extract data', 34, 'change_tempextractdata');
INSERT INTO `auth_permission` VALUES (139, 'Can delete temp extract data', 34, 'delete_tempextractdata');
INSERT INTO `auth_permission` VALUES (140, 'Can view temp extract data', 34, 'view_tempextractdata');
INSERT INTO `auth_permission` VALUES (141, 'Can add global variable', 35, 'add_globalvariable');
INSERT INTO `auth_permission` VALUES (142, 'Can change global variable', 35, 'change_globalvariable');
INSERT INTO `auth_permission` VALUES (143, 'Can delete global variable', 35, 'delete_globalvariable');
INSERT INTO `auth_permission` VALUES (144, 'Can view global variable', 35, 'view_globalvariable');
INSERT INTO `auth_permission` VALUES (145, 'Can add api associated user', 36, 'add_apiassociateduser');
INSERT INTO `auth_permission` VALUES (146, 'Can change api associated user', 36, 'change_apiassociateduser');
INSERT INTO `auth_permission` VALUES (147, 'Can delete api associated user', 36, 'delete_apiassociateduser');
INSERT INTO `auth_permission` VALUES (148, 'Can view api associated user', 36, 'view_apiassociateduser');
INSERT INTO `auth_permission` VALUES (149, 'Can add history', 37, 'add_history');
INSERT INTO `auth_permission` VALUES (150, 'Can change history', 37, 'change_history');
INSERT INTO `auth_permission` VALUES (151, 'Can delete history', 37, 'delete_history');
INSERT INTO `auth_permission` VALUES (152, 'Can view history', 37, 'view_history');
INSERT INTO `auth_permission` VALUES (153, 'Can add pro history', 27, 'add_prohistory');
INSERT INTO `auth_permission` VALUES (154, 'Can change pro history', 27, 'change_prohistory');
INSERT INTO `auth_permission` VALUES (155, 'Can delete pro history', 27, 'delete_prohistory');
INSERT INTO `auth_permission` VALUES (156, 'Can view pro history', 27, 'view_prohistory');
INSERT INTO `auth_permission` VALUES (157, 'Can add page history', 38, 'add_pagehistory');
INSERT INTO `auth_permission` VALUES (158, 'Can change page history', 38, 'change_pagehistory');
INSERT INTO `auth_permission` VALUES (159, 'Can delete page history', 38, 'delete_pagehistory');
INSERT INTO `auth_permission` VALUES (160, 'Can view page history', 38, 'view_pagehistory');
INSERT INTO `auth_permission` VALUES (161, 'Can add fun history', 39, 'add_funhistory');
INSERT INTO `auth_permission` VALUES (162, 'Can change fun history', 39, 'change_funhistory');
INSERT INTO `auth_permission` VALUES (163, 'Can delete fun history', 39, 'delete_funhistory');
INSERT INTO `auth_permission` VALUES (164, 'Can view fun history', 39, 'view_funhistory');
INSERT INTO `auth_permission` VALUES (165, 'Can add api history', 40, 'add_apihistory');
INSERT INTO `auth_permission` VALUES (166, 'Can change api history', 40, 'change_apihistory');
INSERT INTO `auth_permission` VALUES (167, 'Can delete api history', 40, 'delete_apihistory');
INSERT INTO `auth_permission` VALUES (168, 'Can view api history', 40, 'view_apihistory');
INSERT INTO `auth_permission` VALUES (169, 'Can add api test report', 41, 'add_apitestreport');
INSERT INTO `auth_permission` VALUES (170, 'Can change api test report', 41, 'change_apitestreport');
INSERT INTO `auth_permission` VALUES (171, 'Can delete api test report', 41, 'delete_apitestreport');
INSERT INTO `auth_permission` VALUES (172, 'Can view api test report', 41, 'view_apitestreport');
INSERT INTO `auth_permission` VALUES (173, 'Can add api report item', 42, 'add_apireportitem');
INSERT INTO `auth_permission` VALUES (174, 'Can change api report item', 42, 'change_apireportitem');
INSERT INTO `auth_permission` VALUES (175, 'Can delete api report item', 42, 'delete_apireportitem');
INSERT INTO `auth_permission` VALUES (176, 'Can view api report item', 42, 'view_apireportitem');
INSERT INTO `auth_permission` VALUES (177, 'Can add api report', 43, 'add_apireport');
INSERT INTO `auth_permission` VALUES (178, 'Can change api report', 43, 'change_apireport');
INSERT INTO `auth_permission` VALUES (179, 'Can delete api report', 43, 'delete_apireport');
INSERT INTO `auth_permission` VALUES (180, 'Can view api report', 43, 'view_apireport');
INSERT INTO `auth_permission` VALUES (181, 'Can add api queue', 44, 'add_apiqueue');
INSERT INTO `auth_permission` VALUES (182, 'Can change api queue', 44, 'change_apiqueue');
INSERT INTO `auth_permission` VALUES (183, 'Can delete api queue', 44, 'delete_apiqueue');
INSERT INTO `auth_permission` VALUES (184, 'Can view api queue', 44, 'view_apiqueue');
INSERT INTO `auth_permission` VALUES (185, 'Can add periodic task', 45, 'add_periodictask');
INSERT INTO `auth_permission` VALUES (186, 'Can change periodic task', 45, 'change_periodictask');
INSERT INTO `auth_permission` VALUES (187, 'Can delete periodic task', 45, 'delete_periodictask');
INSERT INTO `auth_permission` VALUES (188, 'Can view periodic task', 45, 'view_periodictask');
INSERT INTO `auth_permission` VALUES (189, 'Can add interval', 46, 'add_intervalschedule');
INSERT INTO `auth_permission` VALUES (190, 'Can change interval', 46, 'change_intervalschedule');
INSERT INTO `auth_permission` VALUES (191, 'Can delete interval', 46, 'delete_intervalschedule');
INSERT INTO `auth_permission` VALUES (192, 'Can view interval', 46, 'view_intervalschedule');
INSERT INTO `auth_permission` VALUES (193, 'Can add crontab', 47, 'add_crontabschedule');
INSERT INTO `auth_permission` VALUES (194, 'Can change crontab', 47, 'change_crontabschedule');
INSERT INTO `auth_permission` VALUES (195, 'Can delete crontab', 47, 'delete_crontabschedule');
INSERT INTO `auth_permission` VALUES (196, 'Can view crontab', 47, 'view_crontabschedule');
INSERT INTO `auth_permission` VALUES (197, 'Can add periodic tasks', 48, 'add_periodictasks');
INSERT INTO `auth_permission` VALUES (198, 'Can change periodic tasks', 48, 'change_periodictasks');
INSERT INTO `auth_permission` VALUES (199, 'Can delete periodic tasks', 48, 'delete_periodictasks');
INSERT INTO `auth_permission` VALUES (200, 'Can view periodic tasks', 48, 'view_periodictasks');
INSERT INTO `auth_permission` VALUES (201, 'Can add task state', 49, 'add_taskmeta');
INSERT INTO `auth_permission` VALUES (202, 'Can change task state', 49, 'change_taskmeta');
INSERT INTO `auth_permission` VALUES (203, 'Can delete task state', 49, 'delete_taskmeta');
INSERT INTO `auth_permission` VALUES (204, 'Can view task state', 49, 'view_taskmeta');
INSERT INTO `auth_permission` VALUES (205, 'Can add saved group result', 50, 'add_tasksetmeta');
INSERT INTO `auth_permission` VALUES (206, 'Can change saved group result', 50, 'change_tasksetmeta');
INSERT INTO `auth_permission` VALUES (207, 'Can delete saved group result', 50, 'delete_tasksetmeta');
INSERT INTO `auth_permission` VALUES (208, 'Can view saved group result', 50, 'view_tasksetmeta');
INSERT INTO `auth_permission` VALUES (209, 'Can add worker', 51, 'add_workerstate');
INSERT INTO `auth_permission` VALUES (210, 'Can change worker', 51, 'change_workerstate');
INSERT INTO `auth_permission` VALUES (211, 'Can delete worker', 51, 'delete_workerstate');
INSERT INTO `auth_permission` VALUES (212, 'Can view worker', 51, 'view_workerstate');
INSERT INTO `auth_permission` VALUES (213, 'Can add task', 52, 'add_taskstate');
INSERT INTO `auth_permission` VALUES (214, 'Can change task', 52, 'change_taskstate');
INSERT INTO `auth_permission` VALUES (215, 'Can delete task', 52, 'delete_taskstate');
INSERT INTO `auth_permission` VALUES (216, 'Can view task', 52, 'view_taskstate');
INSERT INTO `auth_permission` VALUES (217, 'Can add case base data', 53, 'add_casebasedata');
INSERT INTO `auth_permission` VALUES (218, 'Can change case base data', 53, 'change_casebasedata');
INSERT INTO `auth_permission` VALUES (219, 'Can delete case base data', 53, 'delete_casebasedata');
INSERT INTO `auth_permission` VALUES (220, 'Can view case base data', 53, 'view_casebasedata');
INSERT INTO `auth_permission` VALUES (221, 'Can add case api validate', 54, 'add_caseapivalidate');
INSERT INTO `auth_permission` VALUES (222, 'Can change case api validate', 54, 'change_caseapivalidate');
INSERT INTO `auth_permission` VALUES (223, 'Can delete case api validate', 54, 'delete_caseapivalidate');
INSERT INTO `auth_permission` VALUES (224, 'Can view case api validate', 54, 'view_caseapivalidate');
INSERT INTO `auth_permission` VALUES (225, 'Can add case api body', 55, 'add_caseapibody');
INSERT INTO `auth_permission` VALUES (226, 'Can change case api body', 55, 'change_caseapibody');
INSERT INTO `auth_permission` VALUES (227, 'Can delete case api body', 55, 'delete_caseapibody');
INSERT INTO `auth_permission` VALUES (228, 'Can view case api body', 55, 'view_caseapibody');
INSERT INTO `auth_permission` VALUES (229, 'Can add case api params', 56, 'add_caseapiparams');
INSERT INTO `auth_permission` VALUES (230, 'Can change case api params', 56, 'change_caseapiparams');
INSERT INTO `auth_permission` VALUES (231, 'Can delete case api params', 56, 'delete_caseapiparams');
INSERT INTO `auth_permission` VALUES (232, 'Can view case api params', 56, 'view_caseapiparams');
INSERT INTO `auth_permission` VALUES (233, 'Can add case api headers', 57, 'add_caseapiheaders');
INSERT INTO `auth_permission` VALUES (234, 'Can change case api headers', 57, 'change_caseapiheaders');
INSERT INTO `auth_permission` VALUES (235, 'Can delete case api headers', 57, 'delete_caseapiheaders');
INSERT INTO `auth_permission` VALUES (236, 'Can view case api headers', 57, 'view_caseapiheaders');
INSERT INTO `auth_permission` VALUES (237, 'Can add case test set', 58, 'add_casetestset');
INSERT INTO `auth_permission` VALUES (238, 'Can change case test set', 58, 'change_casetestset');
INSERT INTO `auth_permission` VALUES (239, 'Can delete case test set', 58, 'delete_casetestset');
INSERT INTO `auth_permission` VALUES (240, 'Can view case test set', 58, 'view_casetestset');
INSERT INTO `auth_permission` VALUES (241, 'Can add case api operation', 59, 'add_caseapioperation');
INSERT INTO `auth_permission` VALUES (242, 'Can change case api operation', 59, 'change_caseapioperation');
INSERT INTO `auth_permission` VALUES (243, 'Can delete case api operation', 59, 'delete_caseapioperation');
INSERT INTO `auth_permission` VALUES (244, 'Can view case api operation', 59, 'view_caseapioperation');
INSERT INTO `auth_permission` VALUES (245, 'Can add case api extract', 60, 'add_caseapiextract');
INSERT INTO `auth_permission` VALUES (246, 'Can change case api extract', 60, 'change_caseapiextract');
INSERT INTO `auth_permission` VALUES (247, 'Can delete case api extract', 60, 'delete_caseapiextract');
INSERT INTO `auth_permission` VALUES (248, 'Can view case api extract', 60, 'view_caseapiextract');
INSERT INTO `auth_permission` VALUES (249, 'Can add case api base', 61, 'add_caseapibase');
INSERT INTO `auth_permission` VALUES (250, 'Can change case api base', 61, 'change_caseapibase');
INSERT INTO `auth_permission` VALUES (251, 'Can delete case api base', 61, 'delete_caseapibase');
INSERT INTO `auth_permission` VALUES (252, 'Can view case api base', 61, 'view_caseapibase');
INSERT INTO `auth_permission` VALUES (253, 'Can add case api dynamic', 62, 'add_caseapidynamic');
INSERT INTO `auth_permission` VALUES (254, 'Can change case api dynamic', 62, 'change_caseapidynamic');
INSERT INTO `auth_permission` VALUES (255, 'Can delete case api dynamic', 62, 'delete_caseapidynamic');
INSERT INTO `auth_permission` VALUES (256, 'Can view case api dynamic', 62, 'view_caseapidynamic');
INSERT INTO `auth_permission` VALUES (257, 'Can add api dynamic', 62, 'add_apidynamic');
INSERT INTO `auth_permission` VALUES (258, 'Can change api dynamic', 62, 'change_apidynamic');
INSERT INTO `auth_permission` VALUES (259, 'Can delete api dynamic', 62, 'delete_apidynamic');
INSERT INTO `auth_permission` VALUES (260, 'Can view api dynamic', 62, 'view_apidynamic');
INSERT INTO `auth_permission` VALUES (261, 'Can add history info', 63, 'add_historyinfo');
INSERT INTO `auth_permission` VALUES (262, 'Can change history info', 63, 'change_historyinfo');
INSERT INTO `auth_permission` VALUES (263, 'Can delete history info', 63, 'delete_historyinfo');
INSERT INTO `auth_permission` VALUES (264, 'Can view history info', 63, 'view_historyinfo');
INSERT INTO `auth_permission` VALUES (265, 'Can add debug talk', 64, 'add_debugtalk');
INSERT INTO `auth_permission` VALUES (266, 'Can change debug talk', 64, 'change_debugtalk');
INSERT INTO `auth_permission` VALUES (267, 'Can delete debug talk', 64, 'delete_debugtalk');
INSERT INTO `auth_permission` VALUES (268, 'Can view debug talk', 64, 'view_debugtalk');
INSERT INTO `auth_permission` VALUES (269, 'Can add api timing task test set', 65, 'add_apitimingtasktestset');
INSERT INTO `auth_permission` VALUES (270, 'Can change api timing task test set', 65, 'change_apitimingtasktestset');
INSERT INTO `auth_permission` VALUES (271, 'Can delete api timing task test set', 65, 'delete_apitimingtasktestset');
INSERT INTO `auth_permission` VALUES (272, 'Can view api timing task test set', 65, 'view_apitimingtasktestset');
INSERT INTO `auth_permission` VALUES (273, 'Can add api timing task', 66, 'add_apitimingtask');
INSERT INTO `auth_permission` VALUES (274, 'Can change api timing task', 66, 'change_apitimingtask');
INSERT INTO `auth_permission` VALUES (275, 'Can delete api timing task', 66, 'delete_apitimingtask');
INSERT INTO `auth_permission` VALUES (276, 'Can view api timing task', 66, 'view_apitimingtask');
INSERT INTO `auth_permission` VALUES (277, 'Can add api timing task run log', 67, 'add_apitimingtaskrunlog');
INSERT INTO `auth_permission` VALUES (278, 'Can change api timing task run log', 67, 'change_apitimingtaskrunlog');
INSERT INTO `auth_permission` VALUES (279, 'Can delete api timing task run log', 67, 'delete_apitimingtaskrunlog');
INSERT INTO `auth_permission` VALUES (280, 'Can view api timing task run log', 67, 'view_apitimingtaskrunlog');
INSERT INTO `auth_permission` VALUES (281, 'Can add api timing task history', 68, 'add_apitimingtaskhistory');
INSERT INTO `auth_permission` VALUES (282, 'Can change api timing task history', 68, 'change_apitimingtaskhistory');
INSERT INTO `auth_permission` VALUES (283, 'Can delete api timing task history', 68, 'delete_apitimingtaskhistory');
INSERT INTO `auth_permission` VALUES (284, 'Can view api timing task history', 68, 'view_apitimingtaskhistory');
INSERT INTO `auth_permission` VALUES (285, 'Can add api batch task', 69, 'add_apibatchtask');
INSERT INTO `auth_permission` VALUES (286, 'Can change api batch task', 69, 'change_apibatchtask');
INSERT INTO `auth_permission` VALUES (287, 'Can delete api batch task', 69, 'delete_apibatchtask');
INSERT INTO `auth_permission` VALUES (288, 'Can view api batch task', 69, 'view_apibatchtask');
INSERT INTO `auth_permission` VALUES (289, 'Can add api batch task test set', 70, 'add_apibatchtasktestset');
INSERT INTO `auth_permission` VALUES (290, 'Can change api batch task test set', 70, 'change_apibatchtasktestset');
INSERT INTO `auth_permission` VALUES (291, 'Can delete api batch task test set', 70, 'delete_apibatchtasktestset');
INSERT INTO `auth_permission` VALUES (292, 'Can view api batch task test set', 70, 'view_apibatchtasktestset');
INSERT INTO `auth_permission` VALUES (293, 'Can add api batch task history', 71, 'add_apibatchtaskhistory');
INSERT INTO `auth_permission` VALUES (294, 'Can change api batch task history', 71, 'change_apibatchtaskhistory');
INSERT INTO `auth_permission` VALUES (295, 'Can delete api batch task history', 71, 'delete_apibatchtaskhistory');
INSERT INTO `auth_permission` VALUES (296, 'Can view api batch task history', 71, 'view_apibatchtaskhistory');
INSERT INTO `auth_permission` VALUES (297, 'Can add api report task item', 72, 'add_apireporttaskitem');
INSERT INTO `auth_permission` VALUES (298, 'Can change api report task item', 72, 'change_apireporttaskitem');
INSERT INTO `auth_permission` VALUES (299, 'Can delete api report task item', 72, 'delete_apireporttaskitem');
INSERT INTO `auth_permission` VALUES (300, 'Can view api report task item', 72, 'view_apireporttaskitem');
INSERT INTO `auth_permission` VALUES (301, 'Can add api batch task run log', 73, 'add_apibatchtaskrunlog');
INSERT INTO `auth_permission` VALUES (302, 'Can change api batch task run log', 73, 'change_apibatchtaskrunlog');
INSERT INTO `auth_permission` VALUES (303, 'Can delete api batch task run log', 73, 'delete_apibatchtaskrunlog');
INSERT INTO `auth_permission` VALUES (304, 'Can view api batch task run log', 73, 'view_apibatchtaskrunlog');
INSERT INTO `auth_permission` VALUES (305, 'Can add api case history', 74, 'add_apicasehistory');
INSERT INTO `auth_permission` VALUES (306, 'Can change api case history', 74, 'change_apicasehistory');
INSERT INTO `auth_permission` VALUES (307, 'Can delete api case history', 74, 'delete_apicasehistory');
INSERT INTO `auth_permission` VALUES (308, 'Can view api case history', 74, 'view_apicasehistory');
INSERT INTO `auth_permission` VALUES (309, 'Can add system params', 75, 'add_systemparams');
INSERT INTO `auth_permission` VALUES (310, 'Can change system params', 75, 'change_systemparams');
INSERT INTO `auth_permission` VALUES (311, 'Can delete system params', 75, 'delete_systemparams');
INSERT INTO `auth_permission` VALUES (312, 'Can view system params', 75, 'view_systemparams');
INSERT INTO `auth_permission` VALUES (313, 'Can add warning info', 76, 'add_warninginfo');
INSERT INTO `auth_permission` VALUES (314, 'Can change warning info', 76, 'change_warninginfo');
INSERT INTO `auth_permission` VALUES (315, 'Can delete warning info', 76, 'delete_warninginfo');
INSERT INTO `auth_permission` VALUES (316, 'Can view warning info', 76, 'view_warninginfo');
INSERT INTO `auth_permission` VALUES (317, 'Can add notice info', 77, 'add_noticeinfo');
INSERT INTO `auth_permission` VALUES (318, 'Can change notice info', 77, 'change_noticeinfo');
INSERT INTO `auth_permission` VALUES (319, 'Can delete notice info', 77, 'delete_noticeinfo');
INSERT INTO `auth_permission` VALUES (320, 'Can view notice info', 77, 'view_noticeinfo');
INSERT INTO `auth_permission` VALUES (321, 'Can add data base', 78, 'add_database');
INSERT INTO `auth_permission` VALUES (322, 'Can change data base', 78, 'change_database');
INSERT INTO `auth_permission` VALUES (323, 'Can delete data base', 78, 'delete_database');
INSERT INTO `auth_permission` VALUES (324, 'Can view data base', 78, 'view_database');
INSERT INTO `auth_permission` VALUES (325, 'Can add element location', 79, 'add_elementlocation');
INSERT INTO `auth_permission` VALUES (326, 'Can change element location', 79, 'change_elementlocation');
INSERT INTO `auth_permission` VALUES (327, 'Can delete element location', 79, 'delete_elementlocation');
INSERT INTO `auth_permission` VALUES (328, 'Can view element location', 79, 'view_elementlocation');
INSERT INTO `auth_permission` VALUES (329, 'Can add element base data', 80, 'add_elementbasedata');
INSERT INTO `auth_permission` VALUES (330, 'Can change element base data', 80, 'change_elementbasedata');
INSERT INTO `auth_permission` VALUES (331, 'Can delete element base data', 80, 'delete_elementbasedata');
INSERT INTO `auth_permission` VALUES (332, 'Can view element base data', 80, 'view_elementbasedata');
INSERT INTO `auth_permission` VALUES (333, 'Can add element history', 81, 'add_elementhistory');
INSERT INTO `auth_permission` VALUES (334, 'Can change element history', 81, 'change_elementhistory');
INSERT INTO `auth_permission` VALUES (335, 'Can delete element history', 81, 'delete_elementhistory');
INSERT INTO `auth_permission` VALUES (336, 'Can view element history', 81, 'view_elementhistory');
INSERT INTO `auth_permission` VALUES (337, 'Can add element event', 82, 'add_elementevent');
INSERT INTO `auth_permission` VALUES (338, 'Can change element event', 82, 'change_elementevent');
INSERT INTO `auth_permission` VALUES (339, 'Can delete element event', 82, 'delete_elementevent');
INSERT INTO `auth_permission` VALUES (340, 'Can view element event', 82, 'view_elementevent');
INSERT INTO `auth_permission` VALUES (341, 'Can add element event component', 83, 'add_elementeventcomponent');
INSERT INTO `auth_permission` VALUES (342, 'Can change element event component', 83, 'change_elementeventcomponent');
INSERT INTO `auth_permission` VALUES (343, 'Can delete element event component', 83, 'delete_elementeventcomponent');
INSERT INTO `auth_permission` VALUES (344, 'Can view element event component', 83, 'view_elementeventcomponent');
INSERT INTO `auth_permission` VALUES (345, 'Can add ui associated page', 84, 'add_uiassociatedpage');
INSERT INTO `auth_permission` VALUES (346, 'Can change ui associated page', 84, 'change_uiassociatedpage');
INSERT INTO `auth_permission` VALUES (347, 'Can delete ui associated page', 84, 'delete_uiassociatedpage');
INSERT INTO `auth_permission` VALUES (348, 'Can view ui associated page', 84, 'view_uiassociatedpage');
INSERT INTO `auth_permission` VALUES (349, 'Can add ui case base data', 85, 'add_uicasebasedata');
INSERT INTO `auth_permission` VALUES (350, 'Can change ui case base data', 85, 'change_uicasebasedata');
INSERT INTO `auth_permission` VALUES (351, 'Can delete ui case base data', 85, 'delete_uicasebasedata');
INSERT INTO `auth_permission` VALUES (352, 'Can view ui case base data', 85, 'view_uicasebasedata');
INSERT INTO `auth_permission` VALUES (353, 'Can add ui test set', 86, 'add_uitestset');
INSERT INTO `auth_permission` VALUES (354, 'Can change ui test set', 86, 'change_uitestset');
INSERT INTO `auth_permission` VALUES (355, 'Can delete ui test set', 86, 'delete_uitestset');
INSERT INTO `auth_permission` VALUES (356, 'Can view ui test set', 86, 'view_uitestset');
INSERT INTO `auth_permission` VALUES (357, 'Can add element dynamic', 87, 'add_elementdynamic');
INSERT INTO `auth_permission` VALUES (358, 'Can change element dynamic', 87, 'change_elementdynamic');
INSERT INTO `auth_permission` VALUES (359, 'Can delete element dynamic', 87, 'delete_elementdynamic');
INSERT INTO `auth_permission` VALUES (360, 'Can view element dynamic', 87, 'view_elementdynamic');
INSERT INTO `auth_permission` VALUES (361, 'Can add ui operation set', 88, 'add_uioperationset');
INSERT INTO `auth_permission` VALUES (362, 'Can change ui operation set', 88, 'change_uioperationset');
INSERT INTO `auth_permission` VALUES (363, 'Can delete ui operation set', 88, 'delete_uioperationset');
INSERT INTO `auth_permission` VALUES (364, 'Can view ui operation set', 88, 'view_uioperationset');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (3, 'pbkdf2_sha256$100000$PjFlecCseGE4$FWlr3q7ywXFfofO/6vbyoY3ysSoEhKEDw0+RXz0/QrY=', NULL, 1, 'admin', '', '', '', 0, 1, '2021-11-04 07:17:06.935097');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token`  (
  `key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of authtoken_token
-- ----------------------------
INSERT INTO `authtoken_token` VALUES ('1da8ae30e34d020fb8aa5e85d475eab97c57d0c6', '2022-02-09 15:23:40.511911', 3);

-- ----------------------------
-- Table structure for celery_taskmeta
-- ----------------------------
DROP TABLE IF EXISTS `celery_taskmeta`;
CREATE TABLE `celery_taskmeta`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `result` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_id`(`task_id`) USING BTREE,
  INDEX `celery_taskmeta_hidden_23fd02dc`(`hidden`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 345 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_taskmeta
-- ----------------------------
INSERT INTO `celery_taskmeta` VALUES (1, 'a791abcc-c293-4a92-aa42-c29831db6c05', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 11:55:40.319514', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (2, '7ec1a266-a1ee-45f0-9f44-3f8dc7c70ade', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABOYW1lRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gkAAAAbmFtZSAnZ2V0UmVxdWVzdERhdGEnIGlzIG5vdCBkZWZpbmVkcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-24 12:08:11.358193', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(caseId,environmentId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 861, in run_case\n    bodyRequestType = item_request[\'bodyRequestType\']\nNameError: name \'getRequestData\' is not defined\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (3, 'c47e814a-2d84-487a-a101-05a333e4e037', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:11:53.466856', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (4, 'e3bf195d-db67-4aa1-91fd-0764f04260c6', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAkAAABjYXNlVGFiZWxxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-24 12:11:58.374639', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(caseId,environmentId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 858, in run_case\n    environmentUrl = getCaseData[\'caseTabel\'][\'environmentUrl\']\nKeyError: \'caseTabel\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (5, '273ab408-0aa0-43df-a5c3-c86b57c0265f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:15:08.845299', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (6, 'ff06a6ea-9baa-4c88-be02-1aeb8ab8a504', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:20:42.893338', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (7, '78f0dbb7-f0b5-44ce-9c32-284759d68f4f', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1hCAAAAcnVuX2Nhc2UoKSBtaXNzaW5nIDEgcmVxdWlyZWQgcG9zaXRpb25hbCBhcmd1bWVudDogJ2Vudmlyb25tZW50SWQncQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-24 12:34:12.662768', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(caseId,environmentId)\nTypeError: run_case() missing 1 required positional argument: \'environmentId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (8, 'db514e5d-f9b2-4500-809a-a583295a5412', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1hCAAAAcnVuX2Nhc2UoKSBtaXNzaW5nIDEgcmVxdWlyZWQgcG9zaXRpb25hbCBhcmd1bWVudDogJ2Vudmlyb25tZW50SWQncQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-24 12:34:32.687832', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(redisKey,caseId,environmentId)\nTypeError: run_case() missing 1 required positional argument: \'environmentId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (9, '876643f3-38a0-4405-aa29-767811733782', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:36:07.016078', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (10, 'd64483f9-36fa-448b-a280-36ab62e2aff3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:37:32.152662', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (11, 'a29ef52a-afcf-4d80-90f5-5757f23a21c1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-24 12:43:29.665214', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (12, 'a9e4d68c-3a37-4beb-a0ab-40b827c25898', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWBAAAABPcGVyYXRpb25hbEVycm9ycQJYCwAAAGV4Y19tZXNzYWdlcQNN1gdYGgAAAE15U1FMIHNlcnZlciBoYXMgZ29uZSBhd2F5cQSGcQVYCgAAAGV4Y19tb2R1bGVxBlgPAAAAZGphbmdvLmRiLnV0aWxzcQd1Lg==', '2021-12-27 10:15:19.425148', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 85, in _execute\n    return self.cursor.execute(sql, params)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/mysql/base.py\", line 71, in execute\n    return self.cursor.execute(query, args)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/cursors.py\", line 206, in execute\n    res = self._query(query)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/cursors.py\", line 319, in _query\n    db.query(q)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/connections.py\", line 259, in query\n    _mysql.connection.query(self, query)\nMySQLdb._exceptions.OperationalError: (2006, \'MySQL server has gone away\')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 480, in trace_task\n    uuid, retval, task_request, publish_result,\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/backends/base.py\", line 158, in mark_as_done\n    self.store_result(task_id, result, state, request=request)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/backends/base.py\", line 443, in store_result\n    request=request, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/djcelery/backends/database.py\", line 33, in _store_result\n    traceback=traceback, children=self.current_task_children(request),\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/djcelery/managers.py\", line 47, in _inner\n    return fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/djcelery/managers.py\", line 189, in store_result\n    \'meta\': {\'children\': children}})\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/djcelery/managers.py\", line 92, in update_or_create\n    return get_queryset(self).update_or_create(**kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/djcelery/managers.py\", line 75, in update_or_create\n    obj, created = self.get_or_create(**kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 487, in get_or_create\n    return self.get(**lookup), False\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 397, in get\n    num = len(clone)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 254, in __len__\n    self._fetch_all()\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 1179, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 53, in __iter__\n    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/compiler.py\", line 1068, in execute_sql\n    cursor.execute(sql, params)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 100, in execute\n    return super().execute(sql, params)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 68, in execute\n    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 77, in _execute_with_wrappers\n    return executor(sql, params, many, context)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 85, in _execute\n    return self.cursor.execute(sql, params)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/utils.py\", line 89, in __exit__\n    raise dj_exc_value.with_traceback(traceback) from exc_value\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/utils.py\", line 85, in _execute\n    return self.cursor.execute(sql, params)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/backends/mysql/base.py\", line 71, in execute\n    return self.cursor.execute(query, args)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/cursors.py\", line 206, in execute\n    res = self._query(query)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/cursors.py\", line 319, in _query\n    db.query(q)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/MySQLdb/connections.py\", line 259, in query\n    _mysql.connection.query(self, query)\ndjango.db.utils.OperationalError: (2006, \'MySQL server has gone away\')\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (13, '2aad44ba-fd45-45fc-ad7c-4383a7639e92', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 10:41:44.727026', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (14, '2d853acb-dd4c-43eb-a836-e93aa534e1d3', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAQAAAB0aWVtcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 10:42:25.172838', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(redisKey,caseId,environmentId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 937, in run_case\n    \'tiem\':itemResults[\'tiem\'],\nKeyError: \'tiem\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (15, '41724fb7-cdfc-4aaf-9b8d-a75069e2b539', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 10:45:53.429982', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (16, 'a377fe92-6cff-42e7-8a3f-672507beefc8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 10:47:16.574781', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (17, '68b55fca-d30c-48b8-92d4-565c34957c2d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 10:47:39.289273', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (18, '94c07ead-612b-471d-ac3f-0603a8f8b6df', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWA4AAABBdHRyaWJ1dGVFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWDsAAAAnUmVkaXNIYW5kbGUnIG9iamVjdCBoYXMgbm8gYXR0cmlidXRlICd3aXRlcl90eXBlX2xpc3RkaWN0J3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-27 11:00:58.316509', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 29, in api_asynchronous_run_case\n    cls_RequstOperation.run_case(redisKey,caseId,environmentId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 945, in run_case\n    cls_RedisHandle.witer_type_listdict(redisKey,redisData)\nAttributeError: \'RedisHandle\' object has no attribute \'witer_type_listdict\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (19, 'ab0dd7b3-c5c0-4829-947a-939fdab1da50', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:01:45.884580', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (20, '787760ae-93a0-4f74-9f16-a5e569976988', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:03:00.524327', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (21, '2cca0fa1-a9a7-4a97-837f-ec5a1e55f7bf', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:03:29.364798', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (22, 'cbd67d05-7871-4b4f-8138-7534d3fc7122', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:03:55.532098', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (23, '7fc0d5bd-fb26-4dd5-b8ef-44600e63f10a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:04:23.813718', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (24, '568328ae-573e-48ee-a156-7a61117b634e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:07:35.319110', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (25, 'ed5ee78a-a560-4dba-9ec3-bdd21f41795c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:15:15.895247', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (26, '89c90c18-2189-411f-ab2c-dfa6773bcc4a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:18:15.580555', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (27, '5019d393-973f-469f-aedd-e5f7066dbade', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:24:13.119062', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (28, 'ecd79de3-8242-4d2e-baec-dba5a812a252', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:25:14.755828', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (29, '412d9d36-54c0-455e-bb34-b5d7da6a19f3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:28:05.060218', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (30, 'c2022011-9403-4dc9-9db9-38f28202dbba', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:29:24.005329', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (31, '26beec37-079f-47eb-85d5-142e2f92b96b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:35:17.629770', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (32, 'faa39743-6c0c-403d-b8e0-28d16e08361e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:36:03.613095', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (33, '1fadafd8-dec1-4f06-9d4d-9a46442bb89c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:36:33.415083', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (34, '277e465f-922f-4669-848f-a51af2e401b8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:52:41.151435', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (35, '7feae3ab-9c3c-4dc1-b0ba-95710a8f30bc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:53:13.698089', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (36, 'ce14c875-167d-49a1-b949-f4cb8e421809', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:55:07.823220', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (37, '56b2e570-cf1b-47c9-918c-7d560a52b59f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:55:30.155463', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (38, '28d6914e-3f33-4119-95d2-4c2d1e45e3a7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:56:07.673167', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (39, '441085bb-09cf-447d-982f-50bcc0c3f03b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:56:54.750634', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (40, '2cf54c89-1508-4f2a-b3e3-d81e517a0ef9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:57:40.602101', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (41, 'b2a07935-a617-416f-a512-0d98bfac6af6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:58:05.824645', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (42, '09fe3649-f480-4206-bc00-b1962b84d011', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 11:58:53.983655', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (43, '436180dc-a68c-4fe6-9fc7-89526be92544', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAcAAAByZXF1ZXN0cQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 15:28:01.577781', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1130, in execute_case\n    results[\'request\'][\'environmentUrl\'] = environmentUrl\nKeyError: \'request\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (44, '59148abb-1b78-4c0d-8ea8-b890fad5dfb6', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABOYW1lRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gkAAAAbmFtZSAnZ2V0UmVxdWVzdERhdGEnIGlzIG5vdCBkZWZpbmVkcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 15:30:05.229020', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1132, in execute_case\n    itemResults[\'request\'][\'headersList\'] = item_request[\'headersData\']\nNameError: name \'getRequestData\' is not defined\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (45, '417e4d94-cd77-4d16-8ccf-44aa6929b3f2', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAUAAABwcm9JZHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-27 15:30:13.201320', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1136, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(getCaseData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 133, in conversion_data_to_request_data\n    proId = getRequestData[\'proId\']\nKeyError: \'proId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (46, '1f9ef9c3-b6df-4e6f-bd9a-52476211d24d', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAYAAABhcGlVcmxxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 15:33:09.475698', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1131, in execute_case\n    itemResults[\'request\'][\'apiUrl\'] = item_request[\'apiUrl\']\nKeyError: \'apiUrl\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (47, '9050b0cc-f7eb-4a81-9677-6ce65bbc3f88', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAcAAAByZXF1ZXN0cQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 15:33:14.312675', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1142, in execute_case\n    results[\'request\'][\'requestUrl\'] = conversionRequestUrl\nKeyError: \'request\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (48, '3bb5752d-849d-4ae7-b985-3a8670dc9ec2', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAYAAABhcGlVcmxxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 15:34:47.730747', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1131, in execute_case\n    itemResults[\'request\'][\'apiUrl\'] = item_request[\'apiUrl\']\nKeyError: \'apiUrl\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (49, '3a6c8430-4fda-4a74-ab7e-16798012ded0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 15:38:07.144299', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (50, 'eb9a3a65-fdc6-4955-be31-5a00ab7001a4', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAwAAAByZXNwb25zZUNvZGVxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 15:40:13.027006', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1181, in execute_case\n    \'code\': itemResults[\'responseCode\'],\nKeyError: \'responseCode\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (51, 'e95e4588-5256-49da-8d6f-644b6502036a', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAwAAAByZXNwb25zZUNvZGVxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 15:41:59.884039', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1181, in execute_case\n    \'code\': resultOfExecution[\'responseCode\'],\nKeyError: \'responseCode\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (52, 'dd798ff4-90ee-4906-a7ba-01168d2448d0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 15:46:33.194363', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (53, '3cf352c1-cc34-4852-ae29-ce90336afdac', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1g/AAAAZXhlY3V0ZV9jYXNlKCkgbWlzc2luZyAxIHJlcXVpcmVkIHBvc2l0aW9uYWwgYXJndW1lbnQ6ICd1c2VySWQncQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 15:50:54.749356', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 31, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey,caseId,environmentId,userId)\nTypeError: execute_case() missing 1 required positional argument: \'userId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (54, 'e4af621c-f029-4a24-aa40-d97d077d44c9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:00:51.100385', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (55, 'baec276c-67fc-4686-997a-e9534e08815e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:04:38.110529', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (56, '3095aaac-398b-448d-aa4e-98c647c16f08', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:05:26.300631', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (57, 'a180d32b-30d1-4b51-9754-21725c652232', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:05:54.225051', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (58, '4e0aca93-9628-4772-a27f-0925ef5584e9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:06:30.125507', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (59, 'c75b1993-9730-4858-8fdf-d823ed71723b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:06:56.867811', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (60, '42327c3e-7415-4f17-855b-c3c6dead7e9a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:07:27.952680', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (61, 'a7d0c8dd-f884-49a5-b640-b103e0eecad0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:21:04.855839', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (62, 'b58dd276-6812-4809-8f02-06d4965d27de', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:21:47.427732', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (63, 'bfb9b7b6-194a-4467-8f69-c8aadde2af77', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:22:21.927641', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (64, '573f7f31-4edb-4c66-b805-bf1da14f8767', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:22:53.140160', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (65, '096160ba-d197-4c77-93d2-70f6cfd32d04', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWBEAAABaZXJvRGl2aXNpb25FcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWBYAAABmbG9hdCBkaXZpc2lvbiBieSB6ZXJvcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 16:31:48.035573', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1177, in execute_case\n    getLiftData = cls_ApiReport.get_report_top_data(testReportId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/TestReport.py\", line 223, in get_report_top_data\n    passRate = passTotal / allTotal * 100\nZeroDivisionError: float division by zero\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (66, '1f76d1da-f4b0-4109-94a1-e0f00d5f0bcf', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAkAAABwYXNzVG90YWxxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 16:34:05.791165', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1181, in execute_case\n    passTotal = getLiftData[\'passTotal\']\nKeyError: \'passTotal\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (67, '47e606da-71d8-464d-bf0e-68b7056633ab', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:37:15.443629', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (68, 'ddedd46e-ad15-4d98-ac71-f9d41aa401f6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:37:43.390124', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (69, 'd320fe7b-fd69-40ec-9f70-a108ada73405', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:37:54.027443', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (70, '2da9af69-b5ea-4ca1-8ea6-623cd3f72eb3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:39:07.865892', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (71, '4204c128-695b-497e-8813-defa9849eab5', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:39:26.552538', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (72, '59194b7f-a831-4081-997c-b565c4c22be1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:40:18.215651', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (73, '0a451284-9f2c-4bc9-a608-da34a5152558', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:41:49.544787', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (74, '4906ec8e-9a96-42c0-a925-3b853e0709c0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:43:04.349828', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (75, '6e0fe26e-ce62-493e-8fac-cfb81b030e14', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:45:44.209038', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (76, 'ad97a672-ed05-461d-8e27-1106a1ee2a6c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:48:09.381006', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (77, '93236a42-bafd-4a3c-93fa-df3c49cb7b00', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:50:22.937743', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (78, 'a90ae5b0-0735-4dd5-9d91-cf9e008f385b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:52:29.118306', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (79, '3278b71e-d066-42b2-800c-684f8b4a0470', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:54:04.553076', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (80, 'c2342635-9d93-43d6-b949-d5be612d8ba3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 16:57:11.122715', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (81, '4759d820-86d6-46a6-86e0-7adb96ae3a06', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:08:51.804462', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (82, 'f4b0900c-7542-47fe-bd9d-97c5038ae1fe', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:11:08.449531', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (83, 'e497a8e6-1934-42de-82ff-95ef1f1a41d8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:18:46.593421', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (84, '9f545076-71aa-4f17-ade9-eb336f8d65d7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:19:00.850452', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (85, 'dfae125e-d32e-4d7c-9577-a59a17302bfb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:19:34.512513', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (86, '1a98c38a-1daa-458c-8c15-a38bd603f65a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:20:45.088286', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (87, 'a8dee47a-d7a8-4e70-b043-170bdba7ca4e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:21:39.305101', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (88, '47d5d03e-d49f-4efc-b2af-ecae37c71ff4', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:22:29.822597', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (89, 'e527c571-f684-4fc0-892c-da71a5f56e4c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:23:15.878483', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (90, 'e6ec728d-ee58-47ce-a8e0-b9a62bb2059d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:23:53.839675', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (91, '1ad5778d-4957-4611-bb6d-582d16824e19', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:23:58.999199', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (92, '17603f75-09e1-48de-920e-3c27b04f37b2', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:36:36.121513', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (93, '1931bfc4-dca3-44c5-9a21-9807469c2824', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:36:45.648775', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (94, 'da8eea79-e753-49ee-adf1-70a7c149e5b9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:40:30.743911', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (95, 'e497fad4-b3e0-4dd2-a612-5c64a4168092', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:40:52.343183', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (96, '8b91f80c-0a5f-45c5-bb24-a01b7953e9b0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:41:32.082471', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (97, 'c4209076-779b-4a6c-b7c1-8598705cc0dc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:42:20.751402', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (98, 'dfc8e1af-8c82-4f19-9f01-9dde4cbf46a8', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gmAAAAJ05vbmVUeXBlJyBvYmplY3QgaXMgbm90IHN1YnNjcmlwdGFibGVxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 17:44:10.029404', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1160, in execute_case\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 847, in request_operation_extract_validate\n    is_del=0, testSet_id=item_testSet.id, key=item_body.key)\nTypeError: \'NoneType\' object is not subscriptable\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (99, '2719ebd6-6eb3-48fe-addb-c1fff22f8019', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:44:27.790701', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (100, '7f55d487-9126-457b-9270-bfac70371132', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:46:10.745221', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (101, '01bb0734-f214-40e5-b9cd-91546af60b39', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:47:06.369641', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (102, '72bb0952-aeb0-4ca8-b218-872414278176', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:48:20.744702', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (103, '211108b0-433f-4858-b284-bae9e2246637', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:49:06.808918', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (104, '434c4947-b9b0-456a-8d38-00f7c74fbd6b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:49:36.310184', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (105, 'e5374e99-7cca-4da6-a540-09ef41dac462', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:49:54.605814', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (106, '7a7c0d63-1a68-4013-8461-c4ca994de632', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAkAAABmYWlsVG90YWxxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-27 17:56:51.865804', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1029, in execute_case\n    assertionsFailTotal= getLiftData[\'topData\'][\'assertions\'][\'failTotal\']\nKeyError: \'failTotal\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (107, '54395f9f-5f52-4987-a3a8-0fcf5d5ef4da', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWBEAAABVbmJvdW5kTG9jYWxFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWEEAAABsb2NhbCB2YXJpYWJsZSAnYXNzZXJ0aW9uc0ZhaWxUb3RhbCcgcmVmZXJlbmNlZCBiZWZvcmUgYXNzaWdubWVudHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-27 17:57:13.062209', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1051, in execute_case\n    \'assertionsFailTotal\':assertionsFailTotal,\nUnboundLocalError: local variable \'assertionsFailTotal\' referenced before assignment\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (108, 'd1b0b07e-f8ec-40b7-aba9-54efb2688df6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:57:41.910429', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (109, '719d3be4-1ea7-44c6-a969-ce09095123b2', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 17:58:27.447221', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (110, '80d1cfe5-f1ea-4793-9e06-3fa4dd67dc08', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWBMAAABhc3NlcnRpb25zUGFzc1RvdGFscQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 18:04:22.462782', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1028, in execute_case\n    assertionsPassTotal = getLiftData[\'topData\'][\'assertionsPassTotal\']\nKeyError: \'assertionsPassTotal\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (111, '7d69ff54-6c3b-4e85-9081-4d2cb0ab8f52', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:09:25.074893', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (112, '712e6b83-94a8-4dc3-8213-556a87c070bc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:10:49.794027', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (113, 'e3b3afdb-1fed-4c3c-b0eb-66ac872d6fb7', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAcAAAByZXN1bHRzcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-27 18:16:41.474840', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1019, in execute_case\n    getLiftData = cls_ApiReport.get_report_top_data(testReportId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/TestReport.py\", line 230, in get_report_top_data\n    if item_pre[\'results\']:\nKeyError: \'results\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (114, 'b165214b-38b3-4039-923a-da8742a4e5d8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:17:16.316777', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (115, '02475b6d-b50f-4ea3-89e5-e77847ec44d8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:22:55.350891', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (116, '99ec3c13-8bf3-4d9a-bc74-3a15130b5a99', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:24:47.363370', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (117, '88364387-5dcd-4578-806c-7bfee5536263', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:26:31.245822', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (118, 'e8aa9b7a-32f5-4984-8b41-161c58e60102', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:27:59.285700', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (119, 'f69f69af-9e54-47fa-9cfa-53009cdf6cfe', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:28:06.553869', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (120, 'a395b105-b6b2-45b1-bedc-827bf705ea7e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:28:29.760374', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (121, '9b66b498-89d3-491f-86f7-66fdd145bfb6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:29:26.253509', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (122, '8b90eeca-ff5b-4c2c-b052-6ef8e6cd8bce', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:31:04.791385', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (123, '388d6322-6d3d-4549-9457-83e2836d5ca0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:34:01.950851', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (124, '0b081bfa-c454-4acd-9adc-a11247f8024d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-27 18:36:32.849328', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (125, '41bc15b7-f57d-4243-bf6c-a7fabd4e6e37', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:11:09.623260', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (126, '08f5d983-3ba6-43d5-9e6d-5693ee7a280c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:11:40.722021', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (127, 'bedec2eb-a55b-4ab5-adf2-73aff3e7769f', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1g8AAAAZXhlY3V0ZV9jYXNlKCkgdGFrZXMgNiBwb3NpdGlvbmFsIGFyZ3VtZW50cyBidXQgNyB3ZXJlIGdpdmVucQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-28 10:13:42.213540', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, queueId, caseId, environmentId, userId)\nTypeError: execute_case() takes 6 positional arguments but 7 were given\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (128, '2e7d2aab-8ce3-4f40-ac42-afb5f252dcb7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:14:00.012025', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (129, '29945381-8457-4632-bcfd-a76483d9ea17', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:14:48.531175', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (130, 'ff284a21-e9fd-49d6-825c-a609580f9c2c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:15:24.399685', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (131, 'e2bfdf2f-44b6-4132-b294-58b2560fff8f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:15:43.320197', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (132, '539da9a8-dc13-4dd7-b5bc-f8cf50a9fc43', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:26:33.393223', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (133, '7e3700ff-1a68-4699-bab4-dcdf3fa3e02c', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWBIAAABhc3NlcnRpb25UYWJsZURhdGFxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-28 10:26:46.467330', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1081, in execute_case\n    \'assertionTableData\':resultOfExecution[\'assertionTableData\'],\nKeyError: \'assertionTableData\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (134, '43560a3a-8e94-4625-a8c8-51d669c13d2b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:27:52.081367', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (135, '433f6762-a481-41d8-b4c0-481ee0de164a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:28:02.443181', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (136, '97dc05ad-c8d7-4e82-a7c9-ba68ff34468c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:29:10.836395', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (137, '98202d3b-b761-4059-b805-cb7b19b21983', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:32:32.829895', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (138, 'd20725a1-449e-4fd8-980a-80fc26b46661', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:33:55.616921', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (139, '97f58ec4-d270-4fc0-8499-473ff5427268', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:34:42.992628', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (140, 'b9f2f5e8-e863-431f-906b-7b5a958b1fa0', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:35:30.208933', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (141, 'aa99373c-8576-45fc-a6b3-c95e99026501', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:38:18.591074', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (142, '9dda9b65-f276-431a-b2b8-585601496cf3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:39:14.922322', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (143, '2e65675f-673d-4727-a214-b42a48e5fb4f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:39:42.678232', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (144, 'f40c49ff-2154-4d3b-b19f-4a96d5f749f7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:41:50.546470', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (145, '081d027c-5c79-4cfa-a4bb-1f320aebc459', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:44:06.749812', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (146, '89a24770-05b0-47e7-8f78-35fe41dd7869', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:45:51.015699', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (147, 'f5a33415-3df6-4aaf-afaf-b649937d3eaa', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:46:08.514380', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (148, 'a912b878-fb62-40eb-a70c-185005a284bb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:47:13.633948', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (149, '577e34fe-40f7-4300-ac29-32d8648e0401', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:50:14.208003', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (150, 'd8375f42-963e-4456-b0d0-84a101ff69ef', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:52:08.482456', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (151, '9ca72342-2009-42dc-ae41-8053d8a520bd', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:52:21.276043', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (152, '8907e3db-6643-4924-b93b-6a285a1589f4', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:54:35.096414', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (153, '846c70c3-3a0d-4508-a148-4004fa4efb5f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:55:23.488954', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (154, '0aa1cfad-ff1c-409d-863a-f34d616a167c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:57:32.413511', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (155, 'be9bf100-8411-4778-b007-c5107937e628', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 10:58:20.269919', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (156, '308b15e6-b5a7-40bd-b6c4-2b8cc61c2c95', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAoAAABGaWVsZEVycm9ycQJYCwAAAGV4Y19tZXNzYWdlcQNYZwAAAENhbm5vdCByZXNvbHZlIGtleXdvcmQgJ2tleScgaW50byBmaWVsZC4gQ2hvaWNlcyBhcmU6IGNyZWF0ZVRpbWUsIGlkLCBrZXlzLCBvbmx5Q29kZSwgdmFsdWVUeXBlLCB2YWx1ZXNxBIVxBVgKAAAAZXhjX21vZHVsZXEGWBYAAABkamFuZ28uY29yZS5leGNlcHRpb25zcQd1Lg==', '2021-12-28 11:02:50.235594', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 992, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey,item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    proId, requestUrl, requestHeaders, requestData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 76, in conversion_params_import_data\n    obj_db_TempExtractData = db_TempExtractData.objects.filter(onlyCode=onlyCode,key=globalName)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/manager.py\", line 82, in manager_method\n    return getattr(self.get_queryset(), name)(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 836, in filter\n    return self._filter_or_exclude(False, *args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/query.py\", line 854, in _filter_or_exclude\n    clone.query.add_q(Q(*args, **kwargs))\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/query.py\", line 1253, in add_q\n    clause, _ = self._add_q(q_object, self.used_aliases)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/query.py\", line 1277, in _add_q\n    split_subq=split_subq,\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/query.py\", line 1153, in build_filter\n    lookups, parts, reffed_expression = self.solve_lookup_type(arg)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/query.py\", line 1015, in solve_lookup_type\n    _, field, _, lookup_parts = self.names_to_path(lookup_splitted, self.get_meta())\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/django/db/models/sql/query.py\", line 1379, in names_to_path\n    \"Choices are: %s\" % (name, \", \".join(available)))\ndjango.core.exceptions.FieldError: Cannot resolve keyword \'key\' into field. Choices are: createTime, id, keys, onlyCode, valueType, values\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (157, '8af17435-dad1-48bb-ac70-0f62227c7df1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:03:33.213735', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (158, 'c4b5dac1-8476-475d-bdf0-0e14a832fb13', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:05:12.545131', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (159, '1c093cc9-a744-437d-8cfe-13809be520e3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:07:22.762696', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (160, '2f5f1f0d-267e-43fb-9552-cf1f2549250d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:07:48.790055', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (161, 'c86cfaad-9723-4f77-8f7c-86e296991315', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:08:14.954690', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (162, '747584ad-194e-4a39-a078-93ca3fc67239', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:09:07.084193', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (163, '8d4a88e7-0e31-422c-aafa-23834ba59aa9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:11:27.852111', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (164, '10c13512-d136-4fa7-855a-3b303dc1886d', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gfAAAAc3RyaW5nIGluZGljZXMgbXVzdCBiZSBpbnRlZ2Vyc3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-28 11:13:03.915474', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 997, in execute_case\n    kvToDict = cls_Common.conversion_kv_to_dict(self,conversionHeadersData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Common.py\", line 130, in conversion_kv_to_dict\n    dicts[item[\'key\']] = item[\'value\']\nTypeError: string indices must be integers\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (165, 'dca1e232-7c1f-4245-9dd0-05b9174c5d71', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWA4AAABBdHRyaWJ1dGVFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWD0AAAB0eXBlIG9iamVjdCAnQ29tbW9uJyBoYXMgbm8gYXR0cmlidXRlICdjb252ZXJzaW9uX2RpY3RfdG9fa3YncQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2021-12-28 11:16:59.139938', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 998, in execute_case\n    dictToKv = cls_Common.conversion_dict_to_kv(self,conversionHeadersData)\nAttributeError: type object \'Common\' has no attribute \'conversion_dict_to_kv\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (166, '3f54e231-f070-4ed5-a42e-76675254da23', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:17:31.286702', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (167, '7e9fff54-f5a3-43cd-9584-6d30768aa69e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:17:52.044600', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (168, '1c892cbc-86af-45c2-aed1-01da22d2e45c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:30:54.177128', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (169, '1b36d086-7d21-4114-8d5c-b6068ac9acb5', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:34:11.437149', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (170, '240091b1-dd9a-4461-9142-255884f162fd', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:56:25.214433', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (171, 'fc3048c0-75c6-439a-aa8c-e17a6e3ba9d9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:58:03.270390', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (172, '6313b387-db11-4b99-9037-df214da93015', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:58:10.241317', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (173, 'f56b9ac3-919a-4fcc-a607-27b61d545a14', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 11:58:30.385543', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (174, '84a96ac4-95cc-4053-bc61-ed61fc002778', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:07:58.656490', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (175, '267b3db5-fd01-4d46-8aec-59df56dc49f7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:08:27.112605', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (176, '2f0c3761-bedd-4883-ae52-be6720026ae3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:08:35.578664', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (177, 'e8fa74d3-10ea-4f06-a024-266357677269', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:10:21.517467', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (178, 'e2e93c5d-3ea3-444c-8625-6e422c9a82b8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:10:51.794536', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (179, '6a5a7ed6-41da-4f3a-b899-a3e4757e6fb8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:11:33.018053', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (180, '9fa20a27-9455-419f-ba98-403af414a9cb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:12:27.693922', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (181, '1afe57c9-10cc-480b-8644-476b3a88e5d6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:13:20.992326', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (182, '8093bc6b-dc00-415e-91c1-6cbfdbc8c29e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:13:55.602206', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (183, 'e06922b9-623e-4010-ae66-010c74357e89', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:15:13.684863', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (184, 'ea02d2c0-f981-4804-8357-753f2b381e85', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:16:20.765611', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (185, '42087620-4ae1-49de-b304-813d7a346799', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWA4AAABlcnJvckluZm9UYWJsZXEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-28 12:26:50.972904', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1013, in execute_case\n    userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 710, in request_operation_extract_validate\n    for i in performExtractAndValidate[\'errorInfoTable\']:\nKeyError: \'errorInfoTable\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (186, 'b90b55e0-92b0-4612-bd16-03055ee9912f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:27:39.594586', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (187, 'caabffd8-2d5d-40a4-9092-9372c65b5908', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:39:08.779102', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (188, 'b346a84a-568e-49d5-ab82-844067339ad2', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:40:06.227969', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (189, 'ad62b925-e61c-478b-a3dc-17fdbecb04c7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 12:41:00.289578', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (190, 'd96d6657-06eb-4b8e-8cad-43a09f59c546', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1hJAAAAYXBpX2FzeW5jaHJvbm91c19ydW5fY2FzZSgpIHRha2VzIDYgcG9zaXRpb25hbCBhcmd1bWVudHMgYnV0IDcgd2VyZSBnaXZlbnEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2021-12-28 14:44:51.056077', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\nTypeError: api_asynchronous_run_case() takes 6 positional arguments but 7 were given\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (191, 'ada3d4f3-e8ec-4602-99bc-3e9a3d10bb7f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 14:45:09.715464', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (192, '39e1c5c2-f60b-44ee-a347-8ea451052651', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 14:56:34.498067', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (193, '4278577b-9326-4639-bc06-715a3b174ced', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 14:57:15.416365', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (194, '308d2f24-894e-47aa-aeba-2e43393b6431', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gmAAAAJ05vbmVUeXBlJyBvYmplY3QgaXMgbm90IHN1YnNjcmlwdGFibGVxBIVxBVgKAAAAZXhjX21vZHVsZXEGWAgAAABidWlsdGluc3EHdS4=', '2021-12-28 15:26:38.551384', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1040, in execute_case\n    itemResults[\'request\'][\'headersDict\'] = conversionHeadersData\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 723, in request_operation_extract_validate\n    requestType, requestParamsType, bodyRequestType,\nTypeError: \'NoneType\' object is not subscriptable\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (195, 'a7c552a9-7edd-4c29-8293-4466b411c692', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:27:49.260070', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (196, 'e2229a97-1a0c-4b8b-ac4a-fedcafe90fbf', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:30:06.356897', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (197, '01c99e34-6f7d-49ba-965c-09c0fe8e60bc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:32:00.882184', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (198, 'f3a5305d-e21b-48c8-af9e-aba79aee4db2', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:32:44.073488', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (199, '70b40542-c595-444a-acd5-a775120cefbb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:36:03.100729', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (200, '3c3d8e7c-efb7-48c9-afa2-c175cfd550e7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-28 15:50:34.737424', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (201, '76937028-b10e-44a1-9045-1ec81430217c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 14:31:20.830430', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (202, 'c5ecac6f-de37-4962-a58d-cf1ad6b7106b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:53:46.638839', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (203, 'ff99575a-ff32-4543-869c-3533b09f7680', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:53:57.984642', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (204, 'c7a8ef1a-7e57-44cf-827d-7084542eea01', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:54:06.712993', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (205, 'aab44d81-2450-4983-b108-13ff2839126a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:54:08.753903', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (206, '63928ffe-4bea-48e4-978b-4d64d9b985d3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:54:13.373686', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (207, '02918e47-3fbd-4e3f-9588-c63311bb7010', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:54:14.699851', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (208, '779a9dd3-c9d2-40a4-9f98-c253c34908d8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:57:29.325731', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (209, '5c153bde-76f8-49e2-93df-59679ec268b7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:57:49.287320', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (210, '0043a477-6a13-4eb1-9e38-e6205ff47cb9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:58:55.269092', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (211, '2ae5dcb6-ce70-41e4-a38e-0f4d9fe14456', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 16:59:18.317237', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (212, 'de03f69f-0bc8-4952-a67a-0c511838003b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:51:40.385080', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (213, '387503e4-afd1-4f4c-9f37-487ebf7db7d8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:52:24.016855', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (214, '98f620ba-98be-46fd-979d-8415c469e177', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:53:12.303578', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (215, 'dc321fb7-ed64-416c-8005-f5e1512c8f0f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:56:45.416848', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (216, 'b27a1918-aabd-47c1-a51b-b9f05b284dd5', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:57:21.947641', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (217, 'e793335d-4f59-4211-8b64-09dde463fbe1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:58:10.931979', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (218, '88a0a8e1-5224-45b2-a5f9-19bc832ce2be', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 17:58:25.265316', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (219, '03be4275-47b5-4777-94c9-0fdbce059a70', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:00:18.738258', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (220, 'da15a2b0-62d8-4cb9-a01e-becf5b99b9b3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:01:19.568343', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (221, 'f53271ff-6997-4d2f-b4e9-654289de7828', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:02:29.815658', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (222, 'e97096b0-f3c3-40f1-9685-cd6de7174ff5', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:04:46.277432', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (223, '572d816a-9952-4c33-90c7-74f50ba8bc7c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:06:40.033289', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (224, '34aaac24-7e38-4a46-8b92-f93b23bba98e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:07:15.563057', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (225, '4e15f7c4-8b28-419e-b514-47430d8a842f', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:07:37.393461', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (226, '8f253776-ef10-4e98-933d-cc15d4539ddb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:09:07.861001', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (227, 'de77cbeb-6952-4198-aba3-6b6945581e8e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:09:17.745366', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (228, 'dc4eed29-e411-4edc-8697-7fdeabeab9d7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:09:55.348521', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (229, 'e2f582ea-b10c-4bfb-998f-4f43b518d095', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2021-12-29 18:10:20.682748', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (230, '319d9c97-4c9f-4d8f-9bff-a74244d5c330', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:19:36.696951', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1058, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (231, '388c3aac-a579-4903-81d2-a29635e38f51', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:21:12.577198', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1058, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (232, '2a246eec-53ad-4cfa-9cc2-87ec7c7c3724', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:22:33.325393', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1058, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (233, 'cc70901d-856b-4337-9cda-c2a04ae800ab', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:25:01.291563', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1058, in execute_case\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (234, 'f5b55b1c-fb9b-4b0e-9137-3791f6819664', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1hVAAAAcmVxdWVzdF9vcGVyYXRpb25fZXh0cmFjdF92YWxpZGF0ZSgpIG1pc3NpbmcgMSByZXF1aXJlZCBwb3NpdGlvbmFsIGFyZ3VtZW50OiAndXNlcklkJ3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:25:30.746892', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1074, in execute_case\n    userId)\nTypeError: request_operation_extract_validate() missing 1 required positional argument: \'userId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (235, 'c9acc2e2-e272-4129-846b-e639cc8bc17b', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABUeXBlRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1hVAAAAcmVxdWVzdF9vcGVyYXRpb25fZXh0cmFjdF92YWxpZGF0ZSgpIG1pc3NpbmcgMSByZXF1aXJlZCBwb3NpdGlvbmFsIGFyZ3VtZW50OiAndXNlcklkJ3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:29:32.390411', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1075, in execute_case\n    requestFile,\nTypeError: request_operation_extract_validate() missing 1 required positional argument: \'userId\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (236, '2d7c0dfd-a0f2-4a4e-aac7-fa6b6aae0bca', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 16:29:45.090047', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (237, '9e38631a-c602-4e03-a6a8-ee0ad24e0e25', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:30:43.732906', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1060, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (238, '42602e5b-fa57-4574-aaa1-64358a851a23', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:31:02.558507', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1060, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (239, '90e857e9-b230-4b62-a2b5-8f0b878e06a2', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:31:32.194601', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1060, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (240, '47210dbc-0505-4b1f-97cb-5efb38dcbbaa', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABmaWxlTGlzdHEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-04 16:33:59.773212', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 32, in api_asynchronous_run_case\n    cls_RequstOperation.execute_case(remindLabel,redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1060, in execute_case\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 164, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 132, in conversion_params_to_json\n    if item_body[\'fileList\']:\nKeyError: \'fileList\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (241, '4dc9f33c-833a-4286-954f-95153862d1f8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 16:34:13.091490', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (242, '3e3dcdb1-3f35-44ba-a9f8-3925bc443eea', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 16:34:23.226628', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (243, '6cfa2cd8-b2ed-4cd0-a9a9-6dc73e7659d1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 16:34:28.485688', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (244, 'bdca9815-9083-4b3d-851f-a4c6c3535ae1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 17:45:43.236296', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (245, '91b3c8d8-9824-43d8-a76c-06187f0257c1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 17:59:31.709398', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (246, '586a3bb7-cf11-4b49-964e-76db8c738bd8', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 18:05:48.868039', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (247, '070067af-b0c5-4072-b93b-3aca8895fa1a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 18:06:36.632200', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (248, 'ab99d426-1b8a-44fc-9457-09045e2475e9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-04 18:12:29.241898', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (249, 'b5ca5e2b-5a78-45dc-a793-278e7921af06', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-05 17:13:22.484171', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (250, '5db21576-97da-43f0-87f3-41833fb66076', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 17:20:31.128519', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (251, 'ab43ba44-73ac-4f89-a7ac-70fd22284857', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 17:31:01.253703', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (252, '5a8c6531-3551-463b-b7f6-4f5787cd493a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 17:31:33.068912', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (253, '463f0be6-cca3-4044-81bf-522bb9e2e726', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 17:55:19.846383', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (254, 'c8c482ce-daaf-4b21-b629-f338a84976fd', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 18:46:05.788054', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (255, '6278cf71-6269-4d1c-b8b2-e9d14ee98854', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 18:49:48.995090', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (256, '619776b2-59b0-4591-a1db-fd087d6718ec', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 18:50:38.154653', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (257, 'e52bc251-3c22-4e12-831c-eaf0fd22f95d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 18:51:08.524171', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (258, '2e6fb923-4fca-4f85-af83-c8a5342035f3', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-07 18:52:22.577182', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (259, 'c580948c-eb41-4895-8c52-9eec1dab9420', 'SUCCESS', 'gAJYCQAAAOaXtumXtOWIsHEALg==', '2022-01-10 12:10:00.054188', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (260, 'a65e66be-9a39-430b-8c5d-09e6471f1cc9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-10 14:06:54.196788', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (261, '6371348d-1ebe-4601-8746-64708c2b0ded', 'SUCCESS', 'gAJ9cQBYCwAAAGl0ZW1SZXN1bHRzcQFdcQJ9cQMoWAYAAAB0YXNrSWRxBEsRWAwAAAB0aW1pbmdDb25maWdxBVgLAAAAMDYgMTQgKiAqICpxBlgIAAAAcmVkaXNLZXlxB1gjAAAANTYzSzgyMW4tODkweVI0NjcteW9wckRFbDYtRmt1N213MWdxCHVhcy4=', '2022-01-10 14:07:11.146756', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZIpQAYokmpmmmpklpepaJhpb6poYGyTpWiSbpugaWKaamZgbphkmJ1sWMvu1FbIAMWtisR4AAhcUYg==');
INSERT INTO `celery_taskmeta` VALUES (262, 'ac57edd0-6407-4f76-ab7d-d574a43818b0', 'SUCCESS', 'gAJ9cQBYCwAAAGl0ZW1SZXN1bHRzcQFdcQJ9cQMoWAYAAAB0YXNrSWRxBEsRWAwAAAB0aW1pbmdDb25maWdxBVgLAAAAMDkgMTQgKiAqICpxBlgIAAAAcmVkaXNLZXlxB1gjAAAAS2pyMXk1ZVctOWMybzZLNTMtZzFDOTMwMlYtYm80RzB4NmdxCHVhcy4=', '2022-01-10 14:09:00.075399', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZIpQAYpYJiVbpBobG+kmmqQY6ZpYGKfoJiUaWugapJmbpJoaGqaaGBgVMvu1FbIAMWtisR4A/j0UGg==');
INSERT INTO `celery_taskmeta` VALUES (263, '9bc8e332-a4d2-483d-ba18-0f74e511e402', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-10 14:09:00.888353', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (264, 'e7e6df9a-9897-4a31-8525-75810c5fa17b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-10 15:26:36.021806', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (265, 'e3bf90df-f6d2-49e4-8ea3-ece9c2ebe875', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-10 15:46:19.020657', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (266, 'a4452cb6-8551-4cd7-88a1-69c1b285ef4a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-10 17:11:45.104401', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (267, '57964ddb-4242-4a00-b731-7e3db268c126', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 12:22:41.318898', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (268, 'ed747b89-1f5d-497c-a2d1-c1fea5820e38', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 14:43:02.190687', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (269, '4f312f2f-af29-494e-a0fe-d3962cae13b1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 14:43:34.967177', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (270, '81fc9c56-ffcf-4a6b-9053-65bc97698d96', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 14:56:19.728947', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (271, 'f7a8ea50-d197-4d5a-b5c3-6884719dc430', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 15:14:17.127069', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (272, '3fbf4609-4ded-4790-a3a5-5633e1490a06', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 16:29:15.486772', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (273, 'b9e95a76-c8e2-4a3b-86bb-c767907ebeb9', 'SUCCESS', 'gAJ9cQBYCwAAAGl0ZW1SZXN1bHRzcQFdcQJ9cQMoWAYAAAB0YXNrSWRxBEsRWAwAAAB0aW1pbmdDb25maWdxBVgLAAAAMzIgMTYgKiAqICpxBlgMAAAAY2VsZXJ5VGFza0lkcQdYJAAAAGE0OGY2ZTY5LWQxZTctNDJiMi05MDg3LTkyOTgxN2VhY2JhMXEIdWFzLg==', '2022-01-11 16:32:00.139995', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZIpQAYokmlikmaWaWeqmGKaa65oYJRnpWhpYmOtaGllaGJqnJiYnJRoWMvu1FbIAMWtisR4A+wkUNg==');
INSERT INTO `celery_taskmeta` VALUES (274, 'a48f6e69-d1e7-42b2-9087-929817eacba1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-11 16:32:01.928468', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (275, '453eeba0-1722-43d7-bc92-70dce676d897', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 10:25:02.053908', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (276, 'be912377-3465-4535-a7f2-be42a48ada32', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 10:25:09.980122', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (277, 'ab11881d-54c4-431e-8642-cded5f04dfbe', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 10:49:14.366867', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (278, '9e843718-545f-44c4-aeac-6877e21f41ff', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 10:52:19.959192', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (279, '7d7cdc09-389c-4a87-be69-641cc897b9b9', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 11:01:51.407750', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (280, '03ea26cd-a4f3-4f73-9555-0d8419eeb326', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 14:39:17.958813', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (281, 'db7477bd-4e17-4b09-a713-3b1c5a0904a6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-12 14:49:26.416246', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (282, 'e991cd59-5ce9-4e2b-973f-93e3c101ff32', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:33:48.418623', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (283, '9ffcb37a-5617-4b2f-aebe-bd0b3005cd4e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:36:03.414609', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (284, '3fe49d44-7383-4086-b1f0-97c5dbfd4490', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:38:03.016444', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (285, 'a61b77a2-bb5a-4d7d-818f-af5f95c4e006', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:44:05.295624', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (286, '05759fdf-c4e6-4498-a094-970168bd2380', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:44:50.123832', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (287, 'e8f36309-b74e-46e4-9bfa-aa6f1e7ad524', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:45:01.820875', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (288, '308ae642-6364-431c-a3af-dac59fcda5f1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5om56YeP5Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 16:45:38.023195', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (289, '9dbcc7b4-a2da-4335-9f8f-ca4f635498d1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 17:58:25.505397', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (290, '306df6b7-f704-4c46-b061-32e413f62181', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-13 18:01:29.270460', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (291, 'f6e8a9fe-e2ec-4523-b51f-dad069fb61db', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-17 17:29:24.499904', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (292, 'e4610cae-9b31-4708-bce8-538b7d3b99bc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-17 18:03:19.083117', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (293, '622c832f-fc68-4eaa-a09a-b94ba5bd8592', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABlcnJvck1zZ3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-17 18:05:48.332325', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1119, in execute_case\n    if itemResults[\'errorMsg\']:\nKeyError: \'errorMsg\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (294, '29e60732-2e43-4aa3-af78-9cf970710680', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABlcnJvck1zZ3EEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-17 18:06:13.458215', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1119, in execute_case\n    if itemResults[\'errorMsg\']:\nKeyError: \'errorMsg\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (295, 'a56a1d41-f882-41b9-87e4-e3f3ec0fc02a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-17 18:06:53.798831', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (296, '50c5ae39-6f08-49a3-ae3b-8c371d9ee361', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-17 18:09:23.827252', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (297, 'ed11c9f4-736e-4fc3-9d5e-d53241847509', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-18 14:32:07.297247', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (298, 'e3b04b89-504d-45ea-83d4-7988864e9779', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABkYXRhQmFzZXEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-19 14:42:39.070314', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1196, in execute_case\n    userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 765, in request_operation_extract_validate\n    if type(item_pre[\'dataBase\']) == list:\nKeyError: \'dataBase\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (299, '460995a5-59e1-4dde-8435-fa69615ce236', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAgAAABkYXRhQmFzZXEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-19 14:43:11.498573', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1196, in execute_case\n    userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 765, in request_operation_extract_validate\n    if type(item_pre[\'dataBase\']) == list:\nKeyError: \'dataBase\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (300, '822a21d8-308b-4e4c-a405-3e3f189dd1f7', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:45:43.859811', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (301, 'a4a15134-e383-4850-8a3c-e8fe42bf11eb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:45:59.416795', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (302, '0d5af0e0-aa5b-4355-bbbc-adddd8e7e86a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:51:23.661253', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (303, '67f46211-0056-4fc1-ac47-01407c08666b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:55:50.675157', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (304, 'f4c5ea3c-0ffb-44df-828b-53dee8514e49', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:59:12.538086', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (305, '401adfb9-f109-4670-ad4c-7e30660bf8ba', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 14:59:59.381647', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (306, 'b000c380-43c5-4200-93e7-5d29c466d669', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:00:36.024867', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (307, '410eed1c-ce9b-48be-8bba-422f4d3f2304', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:02:36.515227', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (308, 'b488b950-fe1e-45e8-bd12-e98ef091eb95', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:03:22.933326', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (309, '1087cf85-df91-49ea-9cf7-400a4c84dc76', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:06:41.697475', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (310, '674e1d76-36dc-4701-9d9c-b18a94aa5b86', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:07:45.971528', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (311, '0c938d04-986f-4879-a83c-2fd8b56be8ad', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:08:49.813459', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (312, 'd357fcfa-b6e7-4d66-bd05-77d156c0b13d', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:09:10.096023', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (313, 'ce25dfa4-6c5c-4abe-bbac-f9871d7c0247', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:09:27.366377', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (314, 'baeae041-b5d6-4e69-b586-75a24156bd66', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:10:35.580320', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (315, '9c8d4be1-0dca-4b98-b9a6-5f79997da7eb', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:11:21.570761', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (316, '6277cdb2-1dd3-4d08-9ae1-8cd52f183e8b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 15:56:12.411400', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (317, '5fe002b7-e647-4735-83d8-2203f0169327', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:08:35.739065', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (318, 'ace1fac8-2b0d-4e86-9850-036b4ad6e313', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:09:31.398735', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (319, 'b8e4e866-af9c-4f33-8e9d-70bec143693c', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:11:42.087999', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (320, '07cedb98-b59b-4ddf-8455-e33a727ceb4a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:11:55.131931', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (321, 'f34a0ca7-a0bf-46ea-af24-a236c9ee30d6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:12:31.570494', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (322, '34f9ae36-63d9-4563-9ffe-402fafb3a92e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:13:14.120533', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (323, '1ead9e6e-5cf0-4274-90ec-c632d8ad4866', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:14:56.497405', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (324, '39fc98e1-fe88-498d-9912-a1b8bc78c22b', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:17:54.650170', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (325, '46651168-33c6-4174-9b7e-8194d1fe2cac', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:18:17.744505', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (326, '92987099-a2e1-401a-882b-7e1c22b40f94', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:18:26.266600', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (327, 'a2cf18e4-6042-48ec-a58e-7cf66782926a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:18:44.098002', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (328, '2956cbee-60fe-4937-99f2-cdff9bf1e944', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:20:27.091003', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (329, '65d2aa3d-eab4-4c7f-917d-65d2dca0da66', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:32:38.427622', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (330, '58a628d0-004a-4a95-bbbb-5122c0b97338', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAUAAABzdGF0ZXEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-19 16:43:35.636777', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1176, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 173, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 140, in conversion_params_to_json\n    if item_body[\'state\']:\nKeyError: \'state\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (331, 'd0d6c026-9b7a-4314-8b5e-d5267e382219', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAgAAABLZXlFcnJvcnECWAsAAABleGNfbWVzc2FnZXEDWAUAAABzdGF0ZXEEhXEFWAoAAABleGNfbW9kdWxlcQZYCAAAAGJ1aWx0aW5zcQd1Lg==', '2022-01-19 16:44:47.105306', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1176, in execute_case\n    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 173, in conversion_data_to_request_data\n    headersData, paramsData, bodyRequestType, bodyData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 140, in conversion_params_to_json\n    if item_body[\'state\']:\nKeyError: \'state\'\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (332, 'f797a1be-6413-4fd6-8f9f-4673a7280e37', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:47:50.558531', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (333, 'be4729dd-103d-4994-8f8f-e9fa8c2bd9e6', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:52:14.525825', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (334, '592de512-ec20-44c2-81d4-4a7489db219a', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:54:45.872543', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (335, '3da61285-12fb-496b-b58f-3b3221daf931', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:57:49.734539', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (336, '35aa7f1b-28cc-4dda-ba95-02ad8ec9fbbc', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:58:15.271593', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (337, '53729100-ce71-4e18-bada-f4af3ab6244e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 16:59:04.749203', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (338, '7adb397f-4edd-47e1-b31f-6776d5a8ed17', 'FAILURE', 'gAJ9cQAoWAgAAABleGNfdHlwZXEBWAkAAABOYW1lRXJyb3JxAlgLAAAAZXhjX21lc3NhZ2VxA1gbAAAAbmFtZSAnaW5kZXgnIGlzIG5vdCBkZWZpbmVkcQSFcQVYCgAAAGV4Y19tb2R1bGVxBlgIAAAAYnVpbHRpbnNxB3Uu', '2022-01-19 17:01:51.199113', 'Traceback (most recent call last):\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 412, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/home/.virtualenvs/TAP3-PY3.7/lib/python3.7/site-packages/celery/app/trace.py\", line 704, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/Task/tasks.py\", line 52, in api_asynchronous_run_case\n    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 1194, in execute_case\n    userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 828, in request_operation_extract_validate\n    labelName, onlyCode, extractData, validateData, requestsApi, userId)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 398, in perform_extract_and_validate\n    extractData)\n  File \"/home/lipenglo/WorkProject/Dev/TAP3/BackService/ClassData/Request.py\", line 287, in request_extract\n    onlyCode=onlyCode, keys=f\"{extractKey}-{index}\", values=retValue, valueType=retValueType\nNameError: name \'index\' is not defined\n', 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (339, '0a0a1b94-b504-4c99-ab0b-29e32a60bbc1', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 17:02:21.798558', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (340, '7507f707-ed6f-436f-ae57-3ea86b7a496e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 17:03:02.384764', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (341, 'dd357839-a190-4655-a5c1-b3ebf6b9658e', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-19 17:03:49.357044', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (342, 'd45c7449-2fb8-4d24-b2d2-6e17550a3087', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5rWL6K+V55So5L6L6L+Q6KGM5a6M5oiQcQAu', '2022-01-20 15:37:11.363609', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (343, '82b87f26-a381-4840-b4d2-f911c0a8dc86', 'SUCCESS', 'gAJYMgAAAGludF9hc3luY2hyb25vdXNfcnVuX2Nhc2Ut5a6a5pe25Lu75Yqh6L+Q6KGM5a6M5oiQcQAu', '2022-01-20 15:37:22.227807', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');
INSERT INTO `celery_taskmeta` VALUES (344, '7517d555-da7c-4792-841a-521a5f976061', 'SUCCESS', 'gAJ9cQBYCwAAAGl0ZW1SZXN1bHRzcQFdcQJzLg==', '2022-02-09 15:19:04.225841', NULL, 0, 'eJxrYKotZIjgYGBgSM7IzEkpSs0rZIwtZCrWAwBWnQb9');

-- ----------------------------
-- Table structure for celery_tasksetmeta
-- ----------------------------
DROP TABLE IF EXISTS `celery_tasksetmeta`;
CREATE TABLE `celery_tasksetmeta`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `result` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `taskset_id`(`taskset_id`) USING BTREE,
  INDEX `celery_tasksetmeta_hidden_593cfc24`(`hidden`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_tasksetmeta
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 89 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (69, 'Api_BatchTask', 'apibatchtask');
INSERT INTO `django_content_type` VALUES (71, 'Api_BatchTask', 'apibatchtaskhistory');
INSERT INTO `django_content_type` VALUES (73, 'Api_BatchTask', 'apibatchtaskrunlog');
INSERT INTO `django_content_type` VALUES (70, 'Api_BatchTask', 'apibatchtasktestset');
INSERT INTO `django_content_type` VALUES (74, 'Api_CaseMaintenance', 'apicasehistory');
INSERT INTO `django_content_type` VALUES (61, 'Api_CaseMaintenance', 'caseapibase');
INSERT INTO `django_content_type` VALUES (55, 'Api_CaseMaintenance', 'caseapibody');
INSERT INTO `django_content_type` VALUES (60, 'Api_CaseMaintenance', 'caseapiextract');
INSERT INTO `django_content_type` VALUES (57, 'Api_CaseMaintenance', 'caseapiheaders');
INSERT INTO `django_content_type` VALUES (59, 'Api_CaseMaintenance', 'caseapioperation');
INSERT INTO `django_content_type` VALUES (56, 'Api_CaseMaintenance', 'caseapiparams');
INSERT INTO `django_content_type` VALUES (54, 'Api_CaseMaintenance', 'caseapivalidate');
INSERT INTO `django_content_type` VALUES (53, 'Api_CaseMaintenance', 'casebasedata');
INSERT INTO `django_content_type` VALUES (58, 'Api_CaseMaintenance', 'casetestset');
INSERT INTO `django_content_type` VALUES (36, 'Api_IntMaintenance', 'apiassociateduser');
INSERT INTO `django_content_type` VALUES (26, 'Api_IntMaintenance', 'apibasedata');
INSERT INTO `django_content_type` VALUES (30, 'Api_IntMaintenance', 'apibody');
INSERT INTO `django_content_type` VALUES (62, 'Api_IntMaintenance', 'apidynamic');
INSERT INTO `django_content_type` VALUES (31, 'Api_IntMaintenance', 'apiextract');
INSERT INTO `django_content_type` VALUES (28, 'Api_IntMaintenance', 'apiheaders');
INSERT INTO `django_content_type` VALUES (40, 'Api_IntMaintenance', 'apihistory');
INSERT INTO `django_content_type` VALUES (33, 'Api_IntMaintenance', 'apioperation');
INSERT INTO `django_content_type` VALUES (29, 'Api_IntMaintenance', 'apiparams');
INSERT INTO `django_content_type` VALUES (32, 'Api_IntMaintenance', 'apivalidate');
INSERT INTO `django_content_type` VALUES (44, 'Api_TestReport', 'apiqueue');
INSERT INTO `django_content_type` VALUES (43, 'Api_TestReport', 'apireport');
INSERT INTO `django_content_type` VALUES (42, 'Api_TestReport', 'apireportitem');
INSERT INTO `django_content_type` VALUES (72, 'Api_TestReport', 'apireporttaskitem');
INSERT INTO `django_content_type` VALUES (41, 'Api_TestReport', 'apitestreport');
INSERT INTO `django_content_type` VALUES (34, 'Api_TestReport', 'tempextractdata');
INSERT INTO `django_content_type` VALUES (76, 'Api_TestReport', 'warninginfo');
INSERT INTO `django_content_type` VALUES (66, 'Api_TimingTask', 'apitimingtask');
INSERT INTO `django_content_type` VALUES (68, 'Api_TimingTask', 'apitimingtaskhistory');
INSERT INTO `django_content_type` VALUES (67, 'Api_TimingTask', 'apitimingtaskrunlog');
INSERT INTO `django_content_type` VALUES (65, 'Api_TimingTask', 'apitimingtasktestset');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (7, 'authtoken', 'token');
INSERT INTO `django_content_type` VALUES (8, 'authtoken', 'tokenproxy');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (78, 'DataBaseEnvironment', 'database');
INSERT INTO `django_content_type` VALUES (64, 'DebugTalk', 'debugtalk');
INSERT INTO `django_content_type` VALUES (47, 'djcelery', 'crontabschedule');
INSERT INTO `django_content_type` VALUES (46, 'djcelery', 'intervalschedule');
INSERT INTO `django_content_type` VALUES (45, 'djcelery', 'periodictask');
INSERT INTO `django_content_type` VALUES (48, 'djcelery', 'periodictasks');
INSERT INTO `django_content_type` VALUES (49, 'djcelery', 'taskmeta');
INSERT INTO `django_content_type` VALUES (50, 'djcelery', 'tasksetmeta');
INSERT INTO `django_content_type` VALUES (52, 'djcelery', 'taskstate');
INSERT INTO `django_content_type` VALUES (51, 'djcelery', 'workerstate');
INSERT INTO `django_content_type` VALUES (39, 'FunManagement', 'funhistory');
INSERT INTO `django_content_type` VALUES (21, 'FunManagement', 'funmanagement');
INSERT INTO `django_content_type` VALUES (35, 'GlobalVariable', 'globalvariable');
INSERT INTO `django_content_type` VALUES (11, 'info', 'errorinfo');
INSERT INTO `django_content_type` VALUES (12, 'info', 'operateinfo');
INSERT INTO `django_content_type` VALUES (17, 'info', 'pushinfo');
INSERT INTO `django_content_type` VALUES (10, 'login', 'errormsg');
INSERT INTO `django_content_type` VALUES (16, 'login', 'userbindrole');
INSERT INTO `django_content_type` VALUES (9, 'login', 'usertable');
INSERT INTO `django_content_type` VALUES (77, 'Notice', 'noticeinfo');
INSERT INTO `django_content_type` VALUES (25, 'PageEnvironment', 'pageenvironment');
INSERT INTO `django_content_type` VALUES (37, 'PageManagement', 'history');
INSERT INTO `django_content_type` VALUES (38, 'PageManagement', 'pagehistory');
INSERT INTO `django_content_type` VALUES (20, 'PageManagement', 'pagemanagement');
INSERT INTO `django_content_type` VALUES (19, 'ProjectManagement', 'probindmembers');
INSERT INTO `django_content_type` VALUES (27, 'ProjectManagement', 'prohistory');
INSERT INTO `django_content_type` VALUES (18, 'ProjectManagement', 'promanagement');
INSERT INTO `django_content_type` VALUES (14, 'role', 'basicrole');
INSERT INTO `django_content_type` VALUES (15, 'role', 'rolebindmenu');
INSERT INTO `django_content_type` VALUES (13, 'routerPar', 'router');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (75, 'SystemParams', 'systemparams');
INSERT INTO `django_content_type` VALUES (84, 'Ui_CaseMaintenance', 'uiassociatedpage');
INSERT INTO `django_content_type` VALUES (85, 'Ui_CaseMaintenance', 'uicasebasedata');
INSERT INTO `django_content_type` VALUES (88, 'Ui_CaseMaintenance', 'uioperationset');
INSERT INTO `django_content_type` VALUES (86, 'Ui_CaseMaintenance', 'uitestset');
INSERT INTO `django_content_type` VALUES (82, 'Ui_ElementEvent', 'elementevent');
INSERT INTO `django_content_type` VALUES (83, 'Ui_ElementEvent', 'elementeventcomponent');
INSERT INTO `django_content_type` VALUES (80, 'Ui_ElementMaintenance', 'elementbasedata');
INSERT INTO `django_content_type` VALUES (87, 'Ui_ElementMaintenance', 'elementdynamic');
INSERT INTO `django_content_type` VALUES (81, 'Ui_ElementMaintenance', 'elementhistory');
INSERT INTO `django_content_type` VALUES (79, 'Ui_ElementMaintenance', 'elementlocation');
INSERT INTO `django_content_type` VALUES (63, 'WorkorderManagement', 'historyinfo');
INSERT INTO `django_content_type` VALUES (23, 'WorkorderManagement', 'workbindpushtousers');
INSERT INTO `django_content_type` VALUES (24, 'WorkorderManagement', 'worklifecycle');
INSERT INTO `django_content_type` VALUES (22, 'WorkorderManagement', 'workordermanagement');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 231 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2021-11-04 05:55:35.415509');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2021-11-04 05:55:35.606294');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2021-11-04 05:55:35.638827');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2021-11-04 05:55:35.646294');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2021-11-04 05:55:35.653760');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2021-11-04 05:55:35.682027');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2021-11-04 05:55:35.705493');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2021-11-04 05:55:35.720960');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2021-11-04 05:55:35.730026');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2021-11-04 05:55:35.744427');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2021-11-04 05:55:35.747628');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2021-11-04 05:55:35.755627');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2021-11-04 05:55:35.771627');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2021-11-04 05:55:35.787093');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2021-11-04 05:55:35.803093');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2021-11-04 05:55:35.811654');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2021-11-04 05:55:35.827635');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2021-11-04 05:55:35.840960');
INSERT INTO `django_migrations` VALUES (19, 'authtoken', '0001_initial', '2021-11-04 06:48:58.344430');
INSERT INTO `django_migrations` VALUES (20, 'authtoken', '0002_auto_20160226_1747', '2021-11-04 06:48:58.365373');
INSERT INTO `django_migrations` VALUES (21, 'authtoken', '0003_tokenproxy', '2021-11-04 06:48:58.370360');
INSERT INTO `django_migrations` VALUES (22, 'login', '0001_initial', '2021-11-04 06:48:58.383325');
INSERT INTO `django_migrations` VALUES (23, 'login', '0002_errormsg', '2021-11-04 06:58:33.159859');
INSERT INTO `django_migrations` VALUES (24, 'login', '0003_auto_20211104_1509', '2021-11-04 07:09:04.257642');
INSERT INTO `django_migrations` VALUES (25, 'login', '0004_delete_errormsg', '2021-11-22 03:40:39.390177');
INSERT INTO `django_migrations` VALUES (26, 'info', '0001_initial', '2021-11-22 03:42:30.128070');
INSERT INTO `django_migrations` VALUES (27, 'info', '0002_rename_errormsg_errorinfo', '2021-11-22 03:48:29.281652');
INSERT INTO `django_migrations` VALUES (28, 'info', '0003_auto_20211122_1152', '2021-11-22 03:52:50.045619');
INSERT INTO `django_migrations` VALUES (29, 'info', '0004_rename_sys_errorinfo_systype', '2021-11-22 03:55:55.953568');
INSERT INTO `django_migrations` VALUES (30, 'info', '0005_auto_20211123_1432', '2021-11-23 06:32:57.827578');
INSERT INTO `django_migrations` VALUES (31, 'login', '0005_alter_usertable_userimg', '2021-11-23 06:32:58.051670');
INSERT INTO `django_migrations` VALUES (32, 'login', '0006_auto_20211123_1457', '2021-11-23 06:57:33.823994');
INSERT INTO `django_migrations` VALUES (33, 'routerPar', '0001_initial', '2021-11-23 06:57:33.857904');
INSERT INTO `django_migrations` VALUES (34, 'routerPar', '0002_router_updatetime', '2021-11-23 06:57:48.090708');
INSERT INTO `django_migrations` VALUES (35, 'routerPar', '0003_auto_20211123_1558', '2021-11-23 07:58:43.703331');
INSERT INTO `django_migrations` VALUES (36, 'info', '0006_alter_errorinfo_systype', '2021-11-23 09:02:24.077352');
INSERT INTO `django_migrations` VALUES (37, 'routerPar', '0004_remove_router_index', '2021-11-23 09:02:24.162288');
INSERT INTO `django_migrations` VALUES (38, 'routerPar', '0005_router_index', '2021-11-23 09:03:29.070570');
INSERT INTO `django_migrations` VALUES (39, 'routerPar', '0006_alter_router_sortnum', '2021-11-23 09:21:04.862751');
INSERT INTO `django_migrations` VALUES (40, 'role', '0001_initial', '2021-11-24 03:25:39.494056');
INSERT INTO `django_migrations` VALUES (41, 'role', '0002_auto_20211124_1442', '2021-11-24 06:42:20.004175');
INSERT INTO `django_migrations` VALUES (42, 'login', '0007_userbindrole', '2021-11-24 07:14:11.536462');
INSERT INTO `django_migrations` VALUES (43, 'info', '0007_rename_uid_operateinfo_cuid', '2021-11-25 02:22:01.742044');
INSERT INTO `django_migrations` VALUES (44, 'info', '0008_rename_cuid_operateinfo_uid', '2021-11-25 02:27:33.425588');
INSERT INTO `django_migrations` VALUES (45, 'routerPar', '0007_router_icon', '2021-11-25 03:27:59.028048');
INSERT INTO `django_migrations` VALUES (46, 'info', '0009_auto_20211125_1419', '2021-11-25 06:19:06.946317');
INSERT INTO `django_migrations` VALUES (47, 'info', '0010_auto_20211125_1437', '2021-11-25 06:37:25.773527');
INSERT INTO `django_migrations` VALUES (48, 'info', '0011_auto_20211125_1439', '2021-11-25 06:39:04.613236');
INSERT INTO `django_migrations` VALUES (49, 'info', '0012_alter_operateinfo_level', '2021-11-25 06:52:25.124134');
INSERT INTO `django_migrations` VALUES (50, 'info', '0013_alter_operateinfo_remindtype', '2021-11-25 06:57:55.563105');
INSERT INTO `django_migrations` VALUES (51, 'info', '0014_auto_20211125_1530', '2021-11-25 07:30:47.046700');
INSERT INTO `django_migrations` VALUES (52, 'info', '0015_auto_20211125_1621', '2021-11-25 08:21:59.980697');
INSERT INTO `django_migrations` VALUES (53, 'info', '0016_auto_20211125_1657', '2021-11-25 08:57:58.831607');
INSERT INTO `django_migrations` VALUES (54, 'info', '0017_remove_pushinfo_received', '2021-11-26 10:06:00.201948');
INSERT INTO `django_migrations` VALUES (55, 'login', '0008_auto_20211129_1528', '2021-11-29 15:29:18.288223');
INSERT INTO `django_migrations` VALUES (56, 'ProjectManagement', '0001_initial', '2021-11-29 15:29:18.480249');
INSERT INTO `django_migrations` VALUES (57, 'info', '0018_auto_20211129_1528', '2021-11-29 15:29:19.425210');
INSERT INTO `django_migrations` VALUES (58, 'role', '0003_auto_20211129_1528', '2021-11-29 15:29:20.803268');
INSERT INTO `django_migrations` VALUES (59, 'routerPar', '0008_auto_20211129_1528', '2021-11-29 15:29:21.888169');
INSERT INTO `django_migrations` VALUES (60, 'ProjectManagement', '0002_auto_20211129_1554', '2021-11-29 15:54:45.771650');
INSERT INTO `django_migrations` VALUES (61, 'ProjectManagement', '0003_promanagement_cuid', '2021-11-29 16:13:48.969017');
INSERT INTO `django_migrations` VALUES (62, 'ProjectManagement', '0004_auto_20211130_1052', '2021-11-30 10:52:23.766117');
INSERT INTO `django_migrations` VALUES (63, 'ProjectManagement', '0005_probindmembers_role', '2021-11-30 10:57:39.557412');
INSERT INTO `django_migrations` VALUES (64, 'role', '0004_basicrole_is_admin', '2021-11-30 14:46:34.825699');
INSERT INTO `django_migrations` VALUES (65, 'PageManagement', '0001_initial', '2021-11-30 17:16:30.810554');
INSERT INTO `django_migrations` VALUES (66, 'PageManagement', '0002_pagemanagement_systype', '2021-11-30 17:21:20.682043');
INSERT INTO `django_migrations` VALUES (67, 'FunManagement', '0001_initial', '2021-12-01 10:38:53.090253');
INSERT INTO `django_migrations` VALUES (68, 'FunManagement', '0002_funmanagement_systype', '2021-12-01 10:40:01.705694');
INSERT INTO `django_migrations` VALUES (69, 'WorkorderManagement', '0001_initial', '2021-12-01 15:41:44.378938');
INSERT INTO `django_migrations` VALUES (70, 'WorkorderManagement', '0002_auto_20211201_1610', '2021-12-01 16:10:22.670465');
INSERT INTO `django_migrations` VALUES (71, 'WorkorderManagement', '0003_workordermanagement_worksource', '2021-12-01 16:23:43.160015');
INSERT INTO `django_migrations` VALUES (72, 'info', '0019_auto_20211201_1815', '2021-12-01 18:16:00.577579');
INSERT INTO `django_migrations` VALUES (73, 'info', '0020_auto_20211202_1005', '2021-12-02 10:15:35.529972');
INSERT INTO `django_migrations` VALUES (74, 'info', '0021_auto_20211202_1017', '2021-12-02 10:17:21.931565');
INSERT INTO `django_migrations` VALUES (75, 'info', '0022_auto_20211202_1018', '2021-12-02 10:18:27.114045');
INSERT INTO `django_migrations` VALUES (76, 'WorkorderManagement', '0004_worklifecycle', '2021-12-02 10:46:30.611134');
INSERT INTO `django_migrations` VALUES (77, 'WorkorderManagement', '0005_auto_20211202_1047', '2021-12-02 10:47:45.661555');
INSERT INTO `django_migrations` VALUES (78, 'WorkorderManagement', '0006_auto_20211202_1405', '2021-12-02 14:05:24.890493');
INSERT INTO `django_migrations` VALUES (79, 'info', '0023_pushinfo_is_read', '2021-12-02 14:05:24.974238');
INSERT INTO `django_migrations` VALUES (80, 'info', '0024_auto_20211202_1408', '2021-12-02 14:08:24.990761');
INSERT INTO `django_migrations` VALUES (81, 'PageEnvironment', '0001_initial', '2021-12-02 16:33:49.689941');
INSERT INTO `django_migrations` VALUES (82, 'info', '0025_auto_20211202_1633', '2021-12-02 16:33:49.799642');
INSERT INTO `django_migrations` VALUES (83, 'Api_IntMaintenance', '0001_initial', '2021-12-03 17:44:29.756770');
INSERT INTO `django_migrations` VALUES (84, 'ProjectManagement', '0006_history', '2021-12-06 11:00:54.239786');
INSERT INTO `django_migrations` VALUES (85, 'ProjectManagement', '0007_auto_20211206_1113', '2021-12-06 11:14:00.662005');
INSERT INTO `django_migrations` VALUES (86, 'ProjectManagement', '0008_history_restoredata', '2021-12-06 11:59:31.283106');
INSERT INTO `django_migrations` VALUES (87, 'ProjectManagement', '0009_delete_history', '2021-12-06 12:04:29.172872');
INSERT INTO `django_migrations` VALUES (88, 'Api_IntMaintenance', '0002_apiheaders', '2021-12-06 12:08:41.675014');
INSERT INTO `django_migrations` VALUES (89, 'Api_IntMaintenance', '0003_auto_20211206_1411', '2021-12-06 14:11:59.415196');
INSERT INTO `django_migrations` VALUES (90, 'Api_IntMaintenance', '0004_auto_20211206_1436', '2021-12-06 14:36:04.233938');
INSERT INTO `django_migrations` VALUES (91, 'Api_IntMaintenance', '0005_apibody', '2021-12-06 14:42:28.822596');
INSERT INTO `django_migrations` VALUES (92, 'Api_IntMaintenance', '0006_apiextract', '2021-12-06 14:49:34.330295');
INSERT INTO `django_migrations` VALUES (93, 'Api_IntMaintenance', '0007_apivalidate', '2021-12-06 14:54:42.674247');
INSERT INTO `django_migrations` VALUES (94, 'Api_IntMaintenance', '0008_apioperation', '2021-12-06 15:04:54.762864');
INSERT INTO `django_migrations` VALUES (95, 'Api_IntMaintenance', '0009_auto_20211206_1523', '2021-12-06 15:23:48.665151');
INSERT INTO `django_migrations` VALUES (96, 'info', '0026_operateinfo_is_read', '2021-12-06 17:46:41.145167');
INSERT INTO `django_migrations` VALUES (97, 'Api_TestReport', '0001_initial', '2021-12-07 15:42:00.795217');
INSERT INTO `django_migrations` VALUES (98, 'GlobalVariable', '0001_initial', '2021-12-08 11:46:32.154411');
INSERT INTO `django_migrations` VALUES (99, 'PageEnvironment', '0002_auto_20211208_1146', '2021-12-08 11:46:32.232810');
INSERT INTO `django_migrations` VALUES (100, 'GlobalVariable', '0002_globalvariable_pid', '2021-12-08 12:01:07.598809');
INSERT INTO `django_migrations` VALUES (101, 'Api_IntMaintenance', '0010_apiassociateduser', '2021-12-09 15:45:10.143381');
INSERT INTO `django_migrations` VALUES (102, 'GlobalVariable', '0003_auto_20211209_1545', '2021-12-09 15:45:10.414524');
INSERT INTO `django_migrations` VALUES (103, 'WorkorderManagement', '0007_auto_20211209_1621', '2021-12-09 16:21:15.734354');
INSERT INTO `django_migrations` VALUES (104, 'WorkorderManagement', '0008_worklifecycle_is_del', '2021-12-09 17:05:04.932977');
INSERT INTO `django_migrations` VALUES (105, 'ProjectManagement', '0010_history', '2021-12-10 15:18:28.567450');
INSERT INTO `django_migrations` VALUES (106, 'ProjectManagement', '0011_auto_20211210_1606', '2021-12-10 16:06:07.883624');
INSERT INTO `django_migrations` VALUES (107, 'ProjectManagement', '0012_history_pid', '2021-12-10 16:07:49.652881');
INSERT INTO `django_migrations` VALUES (108, 'PageManagement', '0003_history', '2021-12-13 10:42:25.346681');
INSERT INTO `django_migrations` VALUES (109, 'PageManagement', '0004_delete_history', '2021-12-13 10:47:44.125794');
INSERT INTO `django_migrations` VALUES (110, 'ProjectManagement', '0013_auto_20211213_1048', '2021-12-13 10:48:17.847841');
INSERT INTO `django_migrations` VALUES (111, 'PageManagement', '0005_pagehistory', '2021-12-13 10:49:45.471020');
INSERT INTO `django_migrations` VALUES (112, 'FunManagement', '0003_funhistory', '2021-12-13 11:44:03.963336');
INSERT INTO `django_migrations` VALUES (113, 'FunManagement', '0004_funhistory_fun', '2021-12-13 12:12:06.307165');
INSERT INTO `django_migrations` VALUES (114, 'Api_IntMaintenance', '0011_apihistory', '2021-12-13 14:31:05.582285');
INSERT INTO `django_migrations` VALUES (115, 'Api_IntMaintenance', '0012_apihistory_api', '2021-12-13 14:31:38.106170');
INSERT INTO `django_migrations` VALUES (116, 'Api_IntMaintenance', '0013_auto_20211213_1552', '2021-12-13 15:52:29.974182');
INSERT INTO `django_migrations` VALUES (117, 'Api_IntMaintenance', '0014_remove_apiassociateduser_historyid', '2021-12-13 15:55:43.831342');
INSERT INTO `django_migrations` VALUES (118, 'Api_IntMaintenance', '0015_auto_20211213_1620', '2021-12-13 16:20:47.380281');
INSERT INTO `django_migrations` VALUES (119, 'Api_TestReport', '0002_apireport_apireportitem_apitestreport', '2021-12-14 10:25:55.763894');
INSERT INTO `django_migrations` VALUES (120, 'info', '0027_auto_20211214_1025', '2021-12-14 10:25:55.873497');
INSERT INTO `django_migrations` VALUES (121, 'Api_TestReport', '0003_auto_20211214_1026', '2021-12-14 10:26:18.706517');
INSERT INTO `django_migrations` VALUES (122, 'Api_TestReport', '0004_auto_20211214_1448', '2021-12-14 14:48:30.567637');
INSERT INTO `django_migrations` VALUES (123, 'Api_TestReport', '0005_apitestreport_runningtime', '2021-12-14 15:21:23.725816');
INSERT INTO `django_migrations` VALUES (124, 'Api_TestReport', '0006_apiqueue', '2021-12-14 15:29:12.865110');
INSERT INTO `django_migrations` VALUES (125, 'Api_TestReport', '0007_auto_20211214_1530', '2021-12-14 15:30:19.884573');
INSERT INTO `django_migrations` VALUES (126, 'Api_TestReport', '0008_apiqueue_pid', '2021-12-15 11:13:15.106423');
INSERT INTO `django_migrations` VALUES (127, 'Api_TestReport', '0009_apiqueue_tasktype', '2021-12-15 11:16:24.903398');
INSERT INTO `django_migrations` VALUES (128, 'Api_TestReport', '0010_apiqueue_page', '2021-12-15 11:17:04.524968');
INSERT INTO `django_migrations` VALUES (129, 'Api_TestReport', '0011_apiqueue_fun', '2021-12-15 11:17:25.219883');
INSERT INTO `django_migrations` VALUES (130, 'Api_TestReport', '0012_auto_20211216_1442', '2021-12-16 14:42:33.110612');
INSERT INTO `django_migrations` VALUES (131, 'djcelery', '0001_initial', '2021-12-16 18:40:13.499628');
INSERT INTO `django_migrations` VALUES (132, 'Api_IntMaintenance', '0016_apibasedata_requesturlradio', '2021-12-20 14:22:29.091045');
INSERT INTO `django_migrations` VALUES (133, 'Api_CaseMaintenance', '0001_initial', '2021-12-20 16:03:55.090491');
INSERT INTO `django_migrations` VALUES (134, 'Api_CaseMaintenance', '0002_caseapibase_caseapibody_caseapiextract_caseapiheaders_caseapioperation_caseapiparams_caseapivalidate', '2021-12-20 16:16:05.254849');
INSERT INTO `django_migrations` VALUES (135, 'Api_IntMaintenance', '0017_caseapidynamic', '2021-12-22 15:23:17.751777');
INSERT INTO `django_migrations` VALUES (136, 'Api_IntMaintenance', '0018_auto_20211222_1523', '2021-12-22 15:23:44.218779');
INSERT INTO `django_migrations` VALUES (137, 'Api_TestReport', '0013_auto_20211228_1510', '2021-12-28 15:10:29.200931');
INSERT INTO `django_migrations` VALUES (138, 'Api_IntMaintenance', '0019_apihistory_textinfo', '2021-12-29 11:33:59.844268');
INSERT INTO `django_migrations` VALUES (139, 'Api_IntMaintenance', '0020_apibasedata_assignedtouser', '2021-12-29 12:18:05.410521');
INSERT INTO `django_migrations` VALUES (140, 'Api_IntMaintenance', '0021_auto_20211231_1409', '2021-12-31 14:09:35.870168');
INSERT INTO `django_migrations` VALUES (141, 'Api_IntMaintenance', '0022_auto_20211231_1639', '2021-12-31 16:39:47.427891');
INSERT INTO `django_migrations` VALUES (142, 'Api_IntMaintenance', '0023_auto_20211231_1750', '2021-12-31 17:50:29.144713');
INSERT INTO `django_migrations` VALUES (143, 'Api_IntMaintenance', '0024_auto_20211231_1754', '2021-12-31 17:54:35.243595');
INSERT INTO `django_migrations` VALUES (144, 'Api_CaseMaintenance', '0003_auto_20220104_1432', '2022-01-04 14:32:06.826019');
INSERT INTO `django_migrations` VALUES (145, 'Api_IntMaintenance', '0025_remove_apibody_filemd5', '2022-01-04 14:32:06.890877');
INSERT INTO `django_migrations` VALUES (146, 'WorkorderManagement', '0009_historyinfo', '2022-01-05 12:17:56.216335');
INSERT INTO `django_migrations` VALUES (147, 'WorkorderManagement', '0010_remove_workordermanagement_message', '2022-01-05 12:33:16.816565');
INSERT INTO `django_migrations` VALUES (148, 'DebugTalk', '0001_initial', '2022-01-06 12:24:20.359874');
INSERT INTO `django_migrations` VALUES (149, 'Api_TimingTask', '0001_initial', '2022-01-06 17:33:31.793269');
INSERT INTO `django_migrations` VALUES (150, 'Api_TimingTask', '0002_auto_20220106_1759', '2022-01-06 17:59:56.356528');
INSERT INTO `django_migrations` VALUES (151, 'Api_TimingTask', '0003_apitimingtask_remarks', '2022-01-06 18:08:08.189753');
INSERT INTO `django_migrations` VALUES (152, 'FunManagement', '0005_auto_20220106_1808', '2022-01-06 18:08:08.357527');
INSERT INTO `django_migrations` VALUES (153, 'Api_TimingTask', '0004_apitimingtasktestset_historycode', '2022-01-07 10:43:57.503903');
INSERT INTO `django_migrations` VALUES (154, 'Api_TimingTask', '0005_apitimingtaskhistory', '2022-01-07 10:52:42.189823');
INSERT INTO `django_migrations` VALUES (155, 'Api_TimingTask', '0006_apitimingtask_historycode', '2022-01-07 10:53:43.317865');
INSERT INTO `django_migrations` VALUES (156, 'Api_TimingTask', '0007_auto_20220107_1055', '2022-01-07 10:55:42.241815');
INSERT INTO `django_migrations` VALUES (157, 'Api_TimingTask', '0008_apitimingtask_historycode', '2022-01-07 10:58:30.507262');
INSERT INTO `django_migrations` VALUES (158, 'Api_TimingTask', '0009_auto_20220107_1100', '2022-01-07 11:00:14.014692');
INSERT INTO `django_migrations` VALUES (159, 'Api_TimingTask', '0010_apitimingtaskhistory_uid', '2022-01-07 11:37:13.794456');
INSERT INTO `django_migrations` VALUES (160, 'Api_TimingTask', '0011_remove_apitimingtask_historycode', '2022-01-07 14:42:15.621963');
INSERT INTO `django_migrations` VALUES (161, 'Api_TimingTask', '0012_apitimingtask_historycode', '2022-01-07 14:49:37.027734');
INSERT INTO `django_migrations` VALUES (162, 'Api_TimingTask', '0013_auto_20220107_1534', '2022-01-07 15:34:14.222854');
INSERT INTO `django_migrations` VALUES (163, 'Api_TimingTask', '0014_remove_apitimingtask_historycode', '2022-01-07 15:35:33.337725');
INSERT INTO `django_migrations` VALUES (164, 'Api_TimingTask', '0015_auto_20220107_1539', '2022-01-07 15:39:42.468309');
INSERT INTO `django_migrations` VALUES (165, 'Api_TimingTask', '0016_remove_apitimingtasktestset_historycode', '2022-01-07 15:40:35.768197');
INSERT INTO `django_migrations` VALUES (166, 'Api_TimingTask', '0017_auto_20220107_1545', '2022-01-07 15:45:09.528184');
INSERT INTO `django_migrations` VALUES (167, 'Api_TestReport', '0014_auto_20220107_1622', '2022-01-07 16:22:49.981152');
INSERT INTO `django_migrations` VALUES (168, 'Api_TimingTask', '0018_apitimingtask_periodictask', '2022-01-10 11:13:53.034973');
INSERT INTO `django_migrations` VALUES (169, 'Api_TimingTask', '0019_remove_apitimingtask_periodictask', '2022-01-10 11:56:05.584844');
INSERT INTO `django_migrations` VALUES (170, 'Api_TimingTask', '0020_apitimingtask_periodictask_id', '2022-01-10 11:56:13.573856');
INSERT INTO `django_migrations` VALUES (171, 'Api_BatchTask', '0001_initial', '2022-01-10 17:53:50.592005');
INSERT INTO `django_migrations` VALUES (172, 'Api_BatchTask', '0002_auto_20220111_1106', '2022-01-11 11:06:15.541331');
INSERT INTO `django_migrations` VALUES (173, 'Api_BatchTask', '0003_apibatchtaskhistory', '2022-01-11 11:17:23.632027');
INSERT INTO `django_migrations` VALUES (174, 'Api_BatchTask', '0004_auto_20220111_1123', '2022-01-11 11:23:48.930716');
INSERT INTO `django_migrations` VALUES (175, 'Api_TimingTask', '0021_auto_20220111_1124', '2022-01-11 11:24:26.157831');
INSERT INTO `django_migrations` VALUES (176, 'Api_TestReport', '0015_auto_20220111_1427', '2022-01-11 14:27:41.521701');
INSERT INTO `django_migrations` VALUES (177, 'Api_TimingTask', '0022_auto_20220111_1626', '2022-01-11 16:26:49.726194');
INSERT INTO `django_migrations` VALUES (178, 'Api_BatchTask', '0005_apibatchtaskrunlog', '2022-01-12 10:22:56.331025');
INSERT INTO `django_migrations` VALUES (179, 'Api_BatchTask', '0006_apibatchtaskrunlog_versions', '2022-01-12 10:35:14.066018');
INSERT INTO `django_migrations` VALUES (180, 'Api_BatchTask', '0007_auto_20220112_1525', '2022-01-12 15:25:43.759710');
INSERT INTO `django_migrations` VALUES (181, 'ProjectManagement', '0014_auto_20220112_1525', '2022-01-12 15:25:43.776660');
INSERT INTO `django_migrations` VALUES (182, 'Api_CaseMaintenance', '0004_auto_20220112_1525', '2022-01-12 15:25:44.911837');
INSERT INTO `django_migrations` VALUES (183, 'Api_CaseMaintenance', '0005_remove_apicasehistory_textinfo', '2022-01-12 15:32:20.083055');
INSERT INTO `django_migrations` VALUES (184, 'Api_IntMaintenance', '0026_apibasedata_historycode', '2022-01-12 15:55:19.475992');
INSERT INTO `django_migrations` VALUES (185, 'ProjectManagement', '0015_promanagement_onlycode', '2022-01-12 15:55:19.631021');
INSERT INTO `django_migrations` VALUES (186, 'ProjectManagement', '0016_remove_promanagement_onlycode', '2022-01-12 17:11:17.884732');
INSERT INTO `django_migrations` VALUES (187, 'ProjectManagement', '0017_promanagement_onlycode', '2022-01-12 17:15:02.460983');
INSERT INTO `django_migrations` VALUES (188, 'PageManagement', '0006_pagemanagement_onlycode', '2022-01-12 17:30:34.711391');
INSERT INTO `django_migrations` VALUES (189, 'FunManagement', '0006_funmanagement_onlycode', '2022-01-12 17:56:51.048785');
INSERT INTO `django_migrations` VALUES (190, 'Api_IntMaintenance', '0027_auto_20220112_1838', '2022-01-12 18:38:50.429841');
INSERT INTO `django_migrations` VALUES (191, 'Api_IntMaintenance', '0028_auto_20220112_1840', '2022-01-12 18:40:19.461339');
INSERT INTO `django_migrations` VALUES (192, 'Api_CaseMaintenance', '0006_apicasehistory_uid', '2022-01-13 11:34:44.788923');
INSERT INTO `django_migrations` VALUES (193, 'Api_CaseMaintenance', '0007_casebasedata_onlycode', '2022-01-13 11:35:32.045415');
INSERT INTO `django_migrations` VALUES (194, 'Api_TimingTask', '0023_auto_20220113_1228', '2022-01-13 12:28:59.987469');
INSERT INTO `django_migrations` VALUES (195, 'ProjectManagement', '0018_prohistory_uid', '2022-01-13 14:28:16.395569');
INSERT INTO `django_migrations` VALUES (196, 'PageManagement', '0007_pagehistory_uid', '2022-01-13 14:29:50.039222');
INSERT INTO `django_migrations` VALUES (197, 'FunManagement', '0007_funhistory_uid', '2022-01-13 14:30:48.346874');
INSERT INTO `django_migrations` VALUES (198, 'Api_IntMaintenance', '0029_apihistory_uid', '2022-01-13 14:32:03.741313');
INSERT INTO `django_migrations` VALUES (199, 'Api_TimingTask', '0024_apitimingtaskrunlog_taskname', '2022-01-13 14:35:12.579472');
INSERT INTO `django_migrations` VALUES (200, 'Api_BatchTask', '0008_auto_20220113_1445', '2022-01-13 14:45:47.313224');
INSERT INTO `django_migrations` VALUES (201, 'SystemParams', '0001_initial', '2022-01-13 17:08:23.798331');
INSERT INTO `django_migrations` VALUES (202, 'SystemParams', '0002_auto_20220113_1710', '2022-01-13 17:10:05.813533');
INSERT INTO `django_migrations` VALUES (203, 'SystemParams', '0003_systemparams_label', '2022-01-13 17:49:07.880765');
INSERT INTO `django_migrations` VALUES (204, 'Api_TestReport', '0016_apitestreport_createtime', '2022-01-14 10:38:54.870520');
INSERT INTO `django_migrations` VALUES (205, 'Api_TestReport', '0017_warninginfo', '2022-01-17 17:21:56.815052');
INSERT INTO `django_migrations` VALUES (206, 'Notice', '0001_initial', '2022-01-18 11:59:17.105345');
INSERT INTO `django_migrations` VALUES (207, 'DataBaseEnvironment', '0001_initial', '2022-01-18 16:38:48.182859');
INSERT INTO `django_migrations` VALUES (208, 'Ui_ElementMaintenance', '0001_initial', '2022-01-20 18:30:30.816284');
INSERT INTO `django_migrations` VALUES (209, 'Ui_ElementMaintenance', '0002_elementbasedata_elementtype', '2022-01-21 11:21:34.545885');
INSERT INTO `django_migrations` VALUES (210, 'Ui_ElementMaintenance', '0003_elementhistory', '2022-01-21 12:20:19.506332');
INSERT INTO `django_migrations` VALUES (211, 'Ui_ElementMaintenance', '0004_elementhistory_element', '2022-01-21 12:31:14.948276');
INSERT INTO `django_migrations` VALUES (212, 'Ui_ElementMaintenance', '0005_elementbasedata_elementstate', '2022-01-21 15:04:36.164935');
INSERT INTO `django_migrations` VALUES (213, 'Ui_ElementEvent', '0001_initial', '2022-01-21 16:00:04.036666');
INSERT INTO `django_migrations` VALUES (214, 'Ui_ElementEvent', '0002_remove_elementevent_onlycode', '2022-01-21 16:03:44.571931');
INSERT INTO `django_migrations` VALUES (215, 'Ui_ElementEvent', '0003_elementevent_eventlogo', '2022-01-21 16:20:28.470410');
INSERT INTO `django_migrations` VALUES (216, 'Ui_ElementEvent', '0004_elementeventcomponent', '2022-01-21 17:02:47.323479');
INSERT INTO `django_migrations` VALUES (217, 'Ui_ElementEvent', '0005_auto_20220121_1735', '2022-01-21 17:35:29.375004');
INSERT INTO `django_migrations` VALUES (218, 'Ui_ElementEvent', '0006_auto_20220121_1743', '2022-01-21 17:43:14.587541');
INSERT INTO `django_migrations` VALUES (219, 'Ui_ElementEvent', '0007_auto_20220121_1820', '2022-01-21 18:20:58.409814');
INSERT INTO `django_migrations` VALUES (220, 'Ui_ElementEvent', '0008_auto_20220121_1821', '2022-01-21 18:21:37.325272');
INSERT INTO `django_migrations` VALUES (221, 'Ui_ElementEvent', '0009_elementevent_index', '2022-01-21 18:48:20.629376');
INSERT INTO `django_migrations` VALUES (222, 'Ui_CaseMaintenance', '0001_initial', '2022-01-25 17:50:10.684022');
INSERT INTO `django_migrations` VALUES (223, 'Ui_CaseMaintenance', '0002_uitestset', '2022-01-26 11:55:55.187308');
INSERT INTO `django_migrations` VALUES (224, 'Ui_CaseMaintenance', '0003_auto_20220126_1203', '2022-01-26 12:03:46.621093');
INSERT INTO `django_migrations` VALUES (225, 'Api_IntMaintenance', '0030_auto_20220126_1642', '2022-01-26 16:42:21.523670');
INSERT INTO `django_migrations` VALUES (226, 'Ui_ElementMaintenance', '0006_elementdynamic', '2022-01-26 16:42:21.665503');
INSERT INTO `django_migrations` VALUES (227, 'Ui_CaseMaintenance', '0004_uioperationset', '2022-01-27 15:47:46.203789');
INSERT INTO `django_migrations` VALUES (228, 'DataBaseEnvironment', '0002_remove_database_systype', '2022-01-27 17:57:24.663523');
INSERT INTO `django_migrations` VALUES (229, 'Ui_CaseMaintenance', '0005_uioperationset_sql', '2022-01-28 12:11:17.042820');
INSERT INTO `django_migrations` VALUES (230, 'Ui_ElementMaintenance', '0007_elementhistory_textinfo', '2022-01-28 12:21:26.808658');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for djcelery_crontabschedule
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_crontabschedule`;
CREATE TABLE `djcelery_crontabschedule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hour` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `day_of_week` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `day_of_month` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `month_of_year` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_crontabschedule
-- ----------------------------
INSERT INTO `djcelery_crontabschedule` VALUES (4, '0', '4', '*', '*', '*');

-- ----------------------------
-- Table structure for djcelery_intervalschedule
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_intervalschedule`;
CREATE TABLE `djcelery_intervalschedule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_intervalschedule
-- ----------------------------

-- ----------------------------
-- Table structure for djcelery_periodictask
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictask`;
CREATE TABLE `djcelery_periodictask`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `task` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `args` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `kwargs` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `queue` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `exchange` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `routing_key` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `expires` datetime(6) NULL DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) NULL DEFAULT NULL,
  `total_run_count` int(10) UNSIGNED NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `crontab_id` int(11) NULL DEFAULT NULL,
  `interval_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_`(`crontab_id`) USING BTREE,
  INDEX `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_`(`interval_id`) USING BTREE,
  CONSTRAINT `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_periodictask
-- ----------------------------
INSERT INTO `djcelery_periodictask` VALUES (5, 'celery.backend_cleanup', 'celery.backend_cleanup', '[]', '{}', NULL, NULL, NULL, NULL, 1, NULL, 0, '2022-02-09 15:11:12.309505', '', 4, NULL);

-- ----------------------------
-- Table structure for djcelery_periodictasks
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictasks`;
CREATE TABLE `djcelery_periodictasks`  (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_periodictasks
-- ----------------------------
INSERT INTO `djcelery_periodictasks` VALUES (1, '2022-02-09 15:11:12.292364');

-- ----------------------------
-- Table structure for djcelery_taskstate
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_taskstate`;
CREATE TABLE `djcelery_taskstate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `task_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `tstamp` datetime(6) NOT NULL,
  `args` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `kwargs` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `eta` datetime(6) NULL DEFAULT NULL,
  `expires` datetime(6) NULL DEFAULT NULL,
  `result` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `traceback` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `runtime` double NULL DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `worker_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_id`(`task_id`) USING BTREE,
  INDEX `djcelery_taskstate_state_53543be4`(`state`) USING BTREE,
  INDEX `djcelery_taskstate_name_8af9eded`(`name`) USING BTREE,
  INDEX `djcelery_taskstate_tstamp_4c3f93a1`(`tstamp`) USING BTREE,
  INDEX `djcelery_taskstate_hidden_c3905e57`(`hidden`) USING BTREE,
  INDEX `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id`(`worker_id`) USING BTREE,
  CONSTRAINT `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_taskstate
-- ----------------------------

-- ----------------------------
-- Table structure for djcelery_workerstate
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_workerstate`;
CREATE TABLE `djcelery_workerstate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_heartbeat` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hostname`(`hostname`) USING BTREE,
  INDEX `djcelery_workerstate_last_heartbeat_4539b544`(`last_heartbeat`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of djcelery_workerstate
-- ----------------------------

-- ----------------------------
-- Table structure for info_operateinfo
-- ----------------------------
DROP TABLE IF EXISTS `info_operateinfo`;
CREATE TABLE `info_operateinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `toPage` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `toFun` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `CUFront` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CURear` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `createTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `info` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `level` int(11) NOT NULL,
  `remindType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `toPro` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `triggerType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_read` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `info_operateinfo_uid_id_4b1694b6_fk`(`uid_id`) USING BTREE,
  CONSTRAINT `info_operateinfo_uid_id_4b1694b6_fk` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3587 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of info_operateinfo
-- ----------------------------
INSERT INTO `info_operateinfo` VALUES (3581, 'LOGIN', '登录页', '登录', NULL, NULL, '2022-02-09 15:23:40.513770', 3, NULL, 4, 'Other', '2022-02-09 15:23:40.513785', NULL, '', NULL);
INSERT INTO `info_operateinfo` VALUES (3582, 'HOME', 'info', 'select_operational_info', NULL, NULL, '2022-02-09 15:23:41.341247', 3, '入参错误:\'sysType\'', 1, 'Error', '2022-02-09 15:23:41.341275', NULL, 'System', 0);
INSERT INTO `info_operateinfo` VALUES (3583, 'HOME', 'info', 'select_operational_info', NULL, NULL, '2022-02-09 15:24:27.274483', 3, '入参错误:\'sysType\'', 1, 'Error', '2022-02-09 15:24:27.274513', NULL, 'System', 0);
INSERT INTO `info_operateinfo` VALUES (3584, 'API', NULL, NULL, '{\"sysType\": \"API\", \"proName\": \"\\u6d4b\\u8bd5\\u9879\\u76ee\", \"remarks\": \"\"}', NULL, '2022-02-09 15:25:14.306356', 3, '新增项目', 3, 'Add', '2022-02-09 15:25:14.306369', '测试项目', 'Manual', NULL);
INSERT INTO `info_operateinfo` VALUES (3585, 'API', '测试页面', NULL, '{\"sysType\": \"API\", \"proId\": \"133\", \"pageName\": \"\\u6d4b\\u8bd5\\u9875\\u9762\", \"remarks\": \"\"}', NULL, '2022-02-09 15:25:52.575481', 3, '新增页面', 3, 'Add', '2022-02-09 15:25:52.575504', '测试项目', 'Manual', NULL);
INSERT INTO `info_operateinfo` VALUES (3586, 'API', '测试页面', '测试功能', '{\"sysType\": \"API\", \"proId\": \"133\", \"pageId\": \"28\", \"funName\": \"\\u6d4b\\u8bd5\\u529f\\u80fd\", \"remarks\": \"\"}', NULL, '2022-02-09 15:25:58.273046', 3, '新增功能', 3, 'Add', '2022-02-09 15:25:58.273069', '测试项目', 'Manual', NULL);

-- ----------------------------
-- Table structure for info_pushinfo
-- ----------------------------
DROP TABLE IF EXISTS `info_pushinfo`;
CREATE TABLE `info_pushinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `oinfo_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `is_read` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `info_pushinfo_uid_id_63808297_fk`(`uid_id`) USING BTREE,
  INDEX `info_pushinfo_oinfo_id_e7ac191a_fk`(`oinfo_id`) USING BTREE,
  CONSTRAINT `info_pushinfo_oinfo_id_e7ac191a_fk` FOREIGN KEY (`oinfo_id`) REFERENCES `info_operateinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `info_pushinfo_uid_id_63808297_fk` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 441 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of info_pushinfo
-- ----------------------------

-- ----------------------------
-- Table structure for login_userbindrole
-- ----------------------------
DROP TABLE IF EXISTS `login_userbindrole`;
CREATE TABLE `login_userbindrole`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `login_userbindrole_user_id_19b829ee_fk`(`user_id`) USING BTREE,
  INDEX `login_userbindrole_role_id_28342864_fk`(`role_id`) USING BTREE,
  CONSTRAINT `login_userbindrole_role_id_28342864_fk` FOREIGN KEY (`role_id`) REFERENCES `role_basicrole` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `login_userbindrole_user_id_19b829ee_fk` FOREIGN KEY (`user_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of login_userbindrole
-- ----------------------------
INSERT INTO `login_userbindrole` VALUES (1, 0, '2021-11-24 15:16:53.000000', '2021-11-24 15:16:57.000000', 1, 3);

-- ----------------------------
-- Table structure for login_usertable
-- ----------------------------
DROP TABLE IF EXISTS `login_usertable`;
CREATE TABLE `login_usertable`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `userName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nickName` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `userImg` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `imgMD5` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `emails` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_lock` int(11) NOT NULL,
  `is_activation` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of login_usertable
-- ----------------------------
INSERT INTO `login_usertable` VALUES (3, 3, 'admin', '超级管理员', '', '4c957fed65c3968dd2a06e702d5a8c52', '3332@qq.com', 0, 1, 0, '2021-11-04 07:17:07.081708', '2021-11-29 16:47:53.000000');

-- ----------------------------
-- Table structure for role_basicrole
-- ----------------------------
DROP TABLE IF EXISTS `role_basicrole`;
CREATE TABLE `role_basicrole`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `dataType` int(11) NOT NULL,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `is_admin` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `role_basicrole_uid_id_f019ebd0_fk`(`uid_id`) USING BTREE,
  CONSTRAINT `role_basicrole_uid_id_f019ebd0_fk` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_basicrole
-- ----------------------------
INSERT INTO `role_basicrole` VALUES (1, '超级管理员', 0, 0, '2021-11-24 03:42:17.710831', '2021-11-24 03:42:17.710938', 3, 1);
INSERT INTO `role_basicrole` VALUES (2, '测试人员', 1, 0, '2021-11-24 03:43:05.819698', '2021-11-24 09:49:09.000000', 3, 0);
INSERT INTO `role_basicrole` VALUES (7, '游客', 0, 0, '2021-11-30 14:49:41.152357', '2021-11-30 14:56:46.000000', 3, 0);
INSERT INTO `role_basicrole` VALUES (9, '研发人员', 1, 0, '2021-11-30 15:00:10.587518', '2021-11-30 15:00:10.587557', 3, 0);

-- ----------------------------
-- Table structure for role_rolebindmenu
-- ----------------------------
DROP TABLE IF EXISTS `role_rolebindmenu`;
CREATE TABLE `role_rolebindmenu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `role_id` int(11) NOT NULL,
  `router_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `role_rolebindmenu_uid_id_97aa27e3_fk`(`uid_id`) USING BTREE,
  INDEX `role_rolebindmenu_role_id_ae537369_fk`(`role_id`) USING BTREE,
  INDEX `role_rolebindmenu_router_id_70ac417f_fk`(`router_id`) USING BTREE,
  CONSTRAINT `role_rolebindmenu_role_id_ae537369_fk` FOREIGN KEY (`role_id`) REFERENCES `role_basicrole` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `role_rolebindmenu_router_id_70ac417f_fk` FOREIGN KEY (`router_id`) REFERENCES `routerPar_router` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `role_rolebindmenu_uid_id_97aa27e3_fk` FOREIGN KEY (`uid_id`) REFERENCES `login_usertable` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 682 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_rolebindmenu
-- ----------------------------
INSERT INTO `role_rolebindmenu` VALUES (523, 'Home', 0, '2022-01-20 15:00:39.561028', '2022-01-20 15:00:39.561068', 1, 1, 3);
INSERT INTO `role_rolebindmenu` VALUES (524, 'Home', 0, '2022-01-20 15:00:39.565765', '2022-01-20 15:00:39.565803', 1, 16, 3);
INSERT INTO `role_rolebindmenu` VALUES (525, 'Home', 0, '2022-01-20 15:00:39.570702', '2022-01-20 15:00:39.570829', 1, 14, 3);
INSERT INTO `role_rolebindmenu` VALUES (526, 'Home', 0, '2022-01-20 15:00:39.576285', '2022-01-20 15:00:39.576329', 1, 58, 3);
INSERT INTO `role_rolebindmenu` VALUES (527, 'Home', 0, '2022-01-20 15:00:39.580462', '2022-01-20 15:00:39.580497', 1, 15, 3);
INSERT INTO `role_rolebindmenu` VALUES (574, 'API', 0, '2022-01-20 15:04:44.278049', '2022-01-20 15:04:44.278084', 1, 37, 3);
INSERT INTO `role_rolebindmenu` VALUES (575, 'API', 0, '2022-01-20 15:04:44.284555', '2022-01-20 15:04:44.284594', 1, 52, 3);
INSERT INTO `role_rolebindmenu` VALUES (576, 'API', 0, '2022-01-20 15:04:44.290249', '2022-01-20 15:04:44.290287', 1, 39, 3);
INSERT INTO `role_rolebindmenu` VALUES (577, 'API', 0, '2022-01-20 15:04:44.294610', '2022-01-20 15:04:44.294663', 1, 40, 3);
INSERT INTO `role_rolebindmenu` VALUES (578, 'API', 0, '2022-01-20 15:04:44.303439', '2022-01-20 15:04:44.303482', 1, 45, 3);
INSERT INTO `role_rolebindmenu` VALUES (579, 'API', 0, '2022-01-20 15:04:44.309228', '2022-01-20 15:04:44.309266', 1, 53, 3);
INSERT INTO `role_rolebindmenu` VALUES (580, 'API', 0, '2022-01-20 15:04:44.319062', '2022-01-20 15:04:44.319113', 1, 55, 3);
INSERT INTO `role_rolebindmenu` VALUES (581, 'API', 0, '2022-01-20 15:04:44.325565', '2022-01-20 15:04:44.325614', 1, 56, 3);
INSERT INTO `role_rolebindmenu` VALUES (582, 'API', 0, '2022-01-20 15:04:44.333986', '2022-01-20 15:04:44.334031', 1, 43, 3);
INSERT INTO `role_rolebindmenu` VALUES (583, 'API', 0, '2022-01-20 15:04:44.339339', '2022-01-20 15:04:44.339377', 1, 42, 3);
INSERT INTO `role_rolebindmenu` VALUES (584, 'API', 0, '2022-01-20 15:04:44.344342', '2022-01-20 15:04:44.344385', 1, 48, 3);
INSERT INTO `role_rolebindmenu` VALUES (585, 'API', 0, '2022-01-20 15:04:44.351233', '2022-01-20 15:04:44.351273', 1, 59, 3);
INSERT INTO `role_rolebindmenu` VALUES (586, 'API', 0, '2022-01-20 15:04:44.356405', '2022-01-20 15:04:44.356444', 1, 47, 3);
INSERT INTO `role_rolebindmenu` VALUES (587, 'API', 0, '2022-01-20 15:04:44.361009', '2022-01-20 15:04:44.361053', 1, 50, 3);
INSERT INTO `role_rolebindmenu` VALUES (588, 'API', 0, '2022-01-20 15:04:44.367099', '2022-01-20 15:04:44.367138', 1, 57, 3);
INSERT INTO `role_rolebindmenu` VALUES (601, 'API', 0, '2022-01-20 15:07:27.193345', '2022-01-20 15:07:27.193406', 2, 37, 3);
INSERT INTO `role_rolebindmenu` VALUES (602, 'API', 0, '2022-01-20 15:07:27.198601', '2022-01-20 15:07:27.198644', 2, 52, 3);
INSERT INTO `role_rolebindmenu` VALUES (603, 'API', 0, '2022-01-20 15:07:27.206362', '2022-01-20 15:07:27.206411', 2, 39, 3);
INSERT INTO `role_rolebindmenu` VALUES (604, 'API', 0, '2022-01-20 15:07:27.211797', '2022-01-20 15:07:27.211837', 2, 40, 3);
INSERT INTO `role_rolebindmenu` VALUES (605, 'API', 0, '2022-01-20 15:07:27.216830', '2022-01-20 15:07:27.216907', 2, 45, 3);
INSERT INTO `role_rolebindmenu` VALUES (606, 'API', 0, '2022-01-20 15:07:27.224212', '2022-01-20 15:07:27.224255', 2, 53, 3);
INSERT INTO `role_rolebindmenu` VALUES (607, 'API', 0, '2022-01-20 15:07:27.229286', '2022-01-20 15:07:27.229325', 2, 55, 3);
INSERT INTO `role_rolebindmenu` VALUES (608, 'API', 0, '2022-01-20 15:07:27.233775', '2022-01-20 15:07:27.233862', 2, 56, 3);
INSERT INTO `role_rolebindmenu` VALUES (609, 'API', 0, '2022-01-20 15:07:27.241287', '2022-01-20 15:07:27.241330', 2, 43, 3);
INSERT INTO `role_rolebindmenu` VALUES (610, 'API', 0, '2022-01-20 15:07:27.246353', '2022-01-20 15:07:27.246396', 2, 42, 3);
INSERT INTO `role_rolebindmenu` VALUES (611, 'API', 0, '2022-01-20 15:07:27.252916', '2022-01-20 15:07:27.252972', 2, 47, 3);
INSERT INTO `role_rolebindmenu` VALUES (612, 'API', 0, '2022-01-20 15:07:27.258895', '2022-01-20 15:07:27.258938', 2, 48, 3);
INSERT INTO `role_rolebindmenu` VALUES (613, 'API', 0, '2022-01-20 15:07:27.263628', '2022-01-20 15:07:27.263669', 2, 59, 3);
INSERT INTO `role_rolebindmenu` VALUES (614, 'API', 0, '2022-01-20 15:07:43.413040', '2022-01-20 15:07:43.413079', 9, 37, 3);
INSERT INTO `role_rolebindmenu` VALUES (615, 'API', 0, '2022-01-20 15:07:43.416967', '2022-01-20 15:07:43.417002', 9, 52, 3);
INSERT INTO `role_rolebindmenu` VALUES (616, 'API', 0, '2022-01-20 15:07:43.423041', '2022-01-20 15:07:43.423080', 9, 39, 3);
INSERT INTO `role_rolebindmenu` VALUES (617, 'API', 0, '2022-01-20 15:07:43.427001', '2022-01-20 15:07:43.427035', 9, 40, 3);
INSERT INTO `role_rolebindmenu` VALUES (618, 'API', 0, '2022-01-20 15:07:43.431276', '2022-01-20 15:07:43.431339', 9, 45, 3);
INSERT INTO `role_rolebindmenu` VALUES (619, 'API', 0, '2022-01-20 15:07:43.435618', '2022-01-20 15:07:43.435658', 9, 53, 3);
INSERT INTO `role_rolebindmenu` VALUES (620, 'API', 0, '2022-01-20 15:07:43.442137', '2022-01-20 15:07:43.442176', 9, 55, 3);
INSERT INTO `role_rolebindmenu` VALUES (621, 'API', 0, '2022-01-20 15:07:43.446138', '2022-01-20 15:07:43.446171', 9, 56, 3);
INSERT INTO `role_rolebindmenu` VALUES (622, 'API', 0, '2022-01-20 15:07:43.451433', '2022-01-20 15:07:43.451484', 9, 43, 3);
INSERT INTO `role_rolebindmenu` VALUES (623, 'API', 0, '2022-01-20 15:07:43.457074', '2022-01-20 15:07:43.457111', 9, 42, 3);
INSERT INTO `role_rolebindmenu` VALUES (624, 'API', 0, '2022-01-20 15:07:43.468164', '2022-01-20 15:07:43.468270', 9, 47, 3);
INSERT INTO `role_rolebindmenu` VALUES (625, 'API', 0, '2022-01-20 15:07:43.474119', '2022-01-20 15:07:43.474154', 9, 48, 3);
INSERT INTO `role_rolebindmenu` VALUES (626, 'API', 0, '2022-01-20 15:07:43.485012', '2022-01-20 15:07:43.485091', 9, 59, 3);
INSERT INTO `role_rolebindmenu` VALUES (648, 'UI', 0, '2022-01-24 16:09:23.783010', '2022-01-24 16:09:23.783050', 2, 61, 3);
INSERT INTO `role_rolebindmenu` VALUES (649, 'UI', 0, '2022-01-24 16:09:23.788373', '2022-01-24 16:09:23.788414', 2, 63, 3);
INSERT INTO `role_rolebindmenu` VALUES (650, 'UI', 0, '2022-01-24 16:09:23.792596', '2022-01-24 16:09:23.792633', 2, 69, 3);
INSERT INTO `role_rolebindmenu` VALUES (651, 'UI', 0, '2022-01-24 16:09:23.796654', '2022-01-24 16:09:23.796690', 2, 66, 3);
INSERT INTO `role_rolebindmenu` VALUES (652, 'UI', 0, '2022-01-24 16:09:23.800755', '2022-01-24 16:09:23.800795', 2, 64, 3);
INSERT INTO `role_rolebindmenu` VALUES (653, 'UI', 0, '2022-01-24 16:09:31.743111', '2022-01-24 16:09:31.743150', 9, 61, 3);
INSERT INTO `role_rolebindmenu` VALUES (654, 'UI', 0, '2022-01-24 16:09:31.747087', '2022-01-24 16:09:31.747123', 9, 63, 3);
INSERT INTO `role_rolebindmenu` VALUES (655, 'UI', 0, '2022-01-24 16:09:31.751528', '2022-01-24 16:09:31.751588', 9, 64, 3);
INSERT INTO `role_rolebindmenu` VALUES (656, 'UI', 0, '2022-01-24 16:09:31.757468', '2022-01-24 16:09:31.757507', 9, 69, 3);
INSERT INTO `role_rolebindmenu` VALUES (657, 'UI', 0, '2022-01-24 16:09:31.761580', '2022-01-24 16:09:31.761622', 9, 66, 3);
INSERT INTO `role_rolebindmenu` VALUES (673, 'UI', 0, '2022-01-27 17:55:05.261733', '2022-01-27 17:55:05.261772', 1, 61, 3);
INSERT INTO `role_rolebindmenu` VALUES (674, 'UI', 0, '2022-01-27 17:55:05.265892', '2022-01-27 17:55:05.265951', 1, 63, 3);
INSERT INTO `role_rolebindmenu` VALUES (675, 'UI', 0, '2022-01-27 17:55:05.270021', '2022-01-27 17:55:05.270054', 1, 64, 3);
INSERT INTO `role_rolebindmenu` VALUES (676, 'UI', 0, '2022-01-27 17:55:05.275277', '2022-01-27 17:55:05.275317', 1, 66, 3);
INSERT INTO `role_rolebindmenu` VALUES (677, 'UI', 0, '2022-01-27 17:55:05.280361', '2022-01-27 17:55:05.280395', 1, 68, 3);
INSERT INTO `role_rolebindmenu` VALUES (678, 'UI', 0, '2022-01-27 17:55:05.284307', '2022-01-27 17:55:05.284341', 1, 69, 3);
INSERT INTO `role_rolebindmenu` VALUES (679, 'UI', 0, '2022-01-27 17:55:05.288435', '2022-01-27 17:55:05.288495', 1, 71, 3);
INSERT INTO `role_rolebindmenu` VALUES (680, 'UI', 0, '2022-01-27 17:55:05.295103', '2022-01-27 17:55:05.295142', 1, 72, 3);
INSERT INTO `role_rolebindmenu` VALUES (681, 'UI', 0, '2022-01-27 17:55:05.299126', '2022-01-27 17:55:05.299159', 1, 73, 3);

-- ----------------------------
-- Table structure for routerPar_router
-- ----------------------------
DROP TABLE IF EXISTS `routerPar_router`;
CREATE TABLE `routerPar_router`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sysType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `level` int(11) NOT NULL,
  `menuName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `routerPath` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `belogId` int(11) NULL DEFAULT NULL,
  `is_del` int(11) NOT NULL,
  `createTime` datetime(6) NOT NULL,
  `updateTime` datetime(6) NOT NULL,
  `sortNum` int(11) NULL DEFAULT NULL,
  `index` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `icon` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 74 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of routerPar_router
-- ----------------------------
INSERT INTO `routerPar_router` VALUES (1, 'HOME', 2, '路由管理', '/Setting/Router/Main', 2, 0, '2021-11-23 14:59:11.000000', '2021-11-25 04:28:15.000000', 1, '2-1', NULL);
INSERT INTO `routerPar_router` VALUES (2, 'HOME', 1, 'Setting', '', NULL, 0, '2021-11-23 15:00:12.000000', '2021-11-25 04:28:15.000000', 1, '', 'el-icon-setting');
INSERT INTO `routerPar_router` VALUES (3, 'Home', 1, 'Home', NULL, NULL, 1, '2021-11-23 15:17:33.000000', '2021-11-23 15:17:35.000000', 1, '', NULL);
INSERT INTO `routerPar_router` VALUES (5, 'Home', 1, 'aaaa', '1234', NULL, 1, '2021-11-23 09:21:27.409977', '2021-11-23 10:33:17.000000', 1, '5', NULL);
INSERT INTO `routerPar_router` VALUES (11, 'Home', 2, 'a11', '3211', 5, 1, '2021-11-23 09:27:38.917459', '2021-11-23 10:33:13.000000', 1, '5-1', NULL);
INSERT INTO `routerPar_router` VALUES (12, 'Home', 2, 'a22', '3212', 5, 1, '2021-11-23 09:28:01.343406', '2021-11-23 10:33:10.000000', 2, '5-2', NULL);
INSERT INTO `routerPar_router` VALUES (13, 'Home', 2, 'a3', '2', 5, 1, '2021-11-23 09:42:06.923706', '2021-11-23 10:33:07.000000', 4, '5-4', NULL);
INSERT INTO `routerPar_router` VALUES (14, 'HOME', 2, '角色管理', '/Setting/Role/Main', 2, 0, '2021-11-24 02:48:46.789805', '2021-11-25 04:28:15.000000', 2, '2-2', NULL);
INSERT INTO `routerPar_router` VALUES (15, 'HOME', 2, '用户管理', '/Setting/UserTable/Main', 2, 0, '2021-11-24 07:22:01.339081', '2021-11-25 04:28:15.000000', 3, '2-3', NULL);
INSERT INTO `routerPar_router` VALUES (16, 'HOME', 2, '操作日志', '/Setting/OperationalInfo/Main', 2, 0, '2021-11-24 10:43:22.870747', '2021-11-25 04:28:15.000000', 4, '2-4', NULL);
INSERT INTO `routerPar_router` VALUES (17, 'Home', 1, 'a', '333', NULL, 1, '2021-11-25 03:00:19.591303', '2021-11-25 03:00:56.000000', 4, NULL, NULL);
INSERT INTO `routerPar_router` VALUES (18, 'Home', 1, 'a', '1', NULL, 1, '2021-11-25 03:01:02.310685', '2021-11-25 03:02:03.000000', 4, NULL, NULL);
INSERT INTO `routerPar_router` VALUES (24, 'Home', 1, 'a', '1', NULL, 1, '2021-11-25 03:07:24.561638', '2021-11-25 03:12:49.000000', 3, NULL, NULL);
INSERT INTO `routerPar_router` VALUES (25, 'Home', 2, 'a1', '', 24, 1, '2021-11-25 03:08:40.722928', '2021-11-25 03:12:30.000000', 1, '24-1', NULL);
INSERT INTO `routerPar_router` VALUES (26, 'Home', 1, 'a1', '', NULL, 1, '2021-11-25 03:49:31.757380', '2021-11-25 03:52:20.000000', 2, NULL, '');
INSERT INTO `routerPar_router` VALUES (27, 'Home', 2, 'a111', '', 26, 1, '2021-11-25 03:49:43.024647', '2021-11-25 03:52:19.000000', 1, '26-1', '');
INSERT INTO `routerPar_router` VALUES (28, 'Home', 1, 'aa1', '', NULL, 1, '2021-11-25 03:51:57.791808', '2021-11-25 03:52:18.000000', 3, NULL, '');
INSERT INTO `routerPar_router` VALUES (29, 'Home', 1, 'a', '', NULL, 1, '2021-11-25 03:52:30.152566', '2021-11-25 03:52:41.000000', 2, NULL, '');
INSERT INTO `routerPar_router` VALUES (30, 'Home', 1, 'a', '', NULL, 1, '2021-11-25 03:52:47.686076', '2021-11-25 04:01:29.000000', 3, NULL, '');
INSERT INTO `routerPar_router` VALUES (31, 'Home', 2, 'a1', '', 30, 1, '2021-11-25 03:53:05.646268', '2021-11-25 04:01:12.000000', 1, '30-1', '');
INSERT INTO `routerPar_router` VALUES (32, 'Home', 1, 'a', '', NULL, 1, '2021-11-25 04:01:47.198564', '2021-11-25 04:25:19.000000', 1, NULL, '');
INSERT INTO `routerPar_router` VALUES (33, 'Home', 2, 'a1', '', 32, 1, '2021-11-25 04:01:53.102921', '2021-11-25 04:25:17.000000', 1, '32-1', '');
INSERT INTO `routerPar_router` VALUES (34, 'Home', 1, 'b', '', NULL, 1, '2021-11-25 04:04:27.905444', '2021-11-25 04:05:23.000000', 4, NULL, '');
INSERT INTO `routerPar_router` VALUES (35, 'Home', 1, 'c', '', NULL, 1, '2021-11-25 04:05:07.369662', '2021-11-25 04:05:21.000000', 5, NULL, '');
INSERT INTO `routerPar_router` VALUES (36, 'API', 1, '所属项目', '', NULL, 0, '2021-11-29 10:56:45.029650', '2022-01-06 14:32:33.000000', 1, NULL, 'el-icon-s-order');
INSERT INTO `routerPar_router` VALUES (37, 'API', 2, '项目维护', '/SysType/Api/ProjectManagement/Main', 36, 0, '2021-11-29 10:56:55.316879', '2022-01-06 14:32:33.000000', 1, '36-1', '');
INSERT INTO `routerPar_router` VALUES (38, 'API', 1, '所属管理', '', NULL, 0, '2021-11-30 16:53:31.483721', '2022-01-06 14:32:33.000000', 3, NULL, 'el-icon-s-order');
INSERT INTO `routerPar_router` VALUES (39, 'API', 2, '页面维护', '/SysType/Api/Page/PageManagement/Main', 38, 0, '2021-11-30 16:53:42.596910', '2022-01-06 14:32:33.000000', 1, '38-1', '');
INSERT INTO `routerPar_router` VALUES (40, 'API', 2, '功能维护', '/SysType/Api/Page/FunManagement/Main', 38, 0, '2021-11-30 16:53:52.527640', '2022-01-06 14:32:33.000000', 2, '38-2', '');
INSERT INTO `routerPar_router` VALUES (41, 'API', 1, '工单管理', '', NULL, 0, '2021-12-01 11:53:20.585373', '2022-01-06 14:32:33.000000', 6, NULL, 'el-icon-s-opportunity');
INSERT INTO `routerPar_router` VALUES (42, 'API', 2, '工单维护', '/WorkorderManagement/WorkorderMaintenance/Main', 41, 0, '2021-12-01 11:53:37.580947', '2022-01-06 14:32:33.000000', 2, '41-2', '');
INSERT INTO `routerPar_router` VALUES (43, 'API', 2, '提醒消息', '/WorkorderManagement/RemindInfo/Main', 41, 0, '2021-12-01 11:53:50.773394', '2022-01-06 14:32:33.000000', 1, '41-1', '');
INSERT INTO `routerPar_router` VALUES (44, 'API', 1, '用例管理', '', NULL, 0, '2021-12-02 15:18:14.720396', '2022-01-06 14:32:33.000000', 4, NULL, 'el-icon-s-management');
INSERT INTO `routerPar_router` VALUES (45, 'API', 2, '接口维护', '/SysType/Api/Page/CaseManagement/ApiMaintenance/Main', 44, 0, '2021-12-02 15:18:30.730037', '2022-01-06 14:32:33.000000', 1, '44-1', '');
INSERT INTO `routerPar_router` VALUES (46, 'API', 1, '环境管理', '', NULL, 0, '2021-12-02 16:21:37.270592', '2022-01-06 14:32:33.000000', 7, NULL, 'el-icon-s-operation');
INSERT INTO `routerPar_router` VALUES (47, 'API', 2, '全局变量', '/SysType/Api/Page/EnvironmentalManagement/GlobalVariable/Main', 46, 0, '2021-12-02 16:22:04.984379', '2022-01-06 14:32:33.000000', 1, '46-1', '');
INSERT INTO `routerPar_router` VALUES (48, 'API', 2, '页面环境', '/SysType/Api/Page/EnvironmentalManagement/PageEnvironment/Main', 46, 0, '2021-12-02 16:22:26.887025', '2022-01-06 14:32:33.000000', 2, '46-2', '');
INSERT INTO `routerPar_router` VALUES (49, 'API', 1, '设置', '', NULL, 0, '2021-12-08 11:00:21.537821', '2022-01-06 14:32:33.000000', 8, NULL, 'el-icon-s-tools');
INSERT INTO `routerPar_router` VALUES (50, 'API', 2, 'DebugTalk.py', '/SysType/Api/Page/Setting/DebugTalk/Main', 49, 0, '2021-12-08 11:00:42.724050', '2022-01-06 14:32:33.000000', 1, '49-1', '');
INSERT INTO `routerPar_router` VALUES (51, 'API', 1, '报告管理', '', NULL, 0, '2021-12-14 10:28:51.171589', '2022-01-06 14:32:33.000000', 2, NULL, 'el-icon-s-data');
INSERT INTO `routerPar_router` VALUES (52, 'API', 2, '报告维护', '/SysType/Api/Page/TestReport/Main', 51, 0, '2021-12-14 10:29:12.709735', '2022-01-06 14:32:33.000000', 1, '51-1', '');
INSERT INTO `routerPar_router` VALUES (53, 'API', 2, '用例维护', '/SysType/Api/Page/CaseManagement/CaseMaintenance/Main', 44, 0, '2021-12-17 11:05:20.400135', '2022-01-06 14:32:33.000000', 2, '44-2', '');
INSERT INTO `routerPar_router` VALUES (54, 'API', 1, '任务管理', '', NULL, 0, '2022-01-06 14:31:30.989750', '2022-01-06 14:32:33.000000', 5, NULL, 'el-icon-folder-add');
INSERT INTO `routerPar_router` VALUES (55, 'API', 2, '定时任务', '/SysType/Api/Page/TaskManagement/TimingTask/Main', 54, 0, '2022-01-06 14:31:45.614417', '2022-01-06 14:34:59.000000', 1, '54-1', '');
INSERT INTO `routerPar_router` VALUES (56, 'API', 2, '批量任务', '/SysType/Api/Page/TaskManagement/BatchTask/Main', 54, 0, '2022-01-10 15:47:38.583733', '2022-01-10 16:19:24.000000', 2, '54-2', '');
INSERT INTO `routerPar_router` VALUES (57, 'API', 2, '系统参数', '/SysType/Api/Page/Setting/SystemParams/Main', 49, 0, '2022-01-13 16:54:27.778111', '2022-01-13 16:54:27.778272', 2, '49-2', '');
INSERT INTO `routerPar_router` VALUES (58, 'HOME', 2, '公告管理', '/Setting/Notice/Main', 2, 0, '2022-01-18 11:23:17.035475', '2022-01-18 11:25:27.000000', 5, '2-5', '');
INSERT INTO `routerPar_router` VALUES (59, 'API', 2, '数据库环境', '/SysType/Api/Page/EnvironmentalManagement/DataBase/Main', 46, 0, '2022-01-18 14:36:19.205405', '2022-01-18 14:41:03.000000', 3, '46-3', '');
INSERT INTO `routerPar_router` VALUES (60, 'UI', 1, '所属项目', '', NULL, 0, '2022-01-20 16:02:35.742764', '2022-01-24 17:11:50.000000', 1, NULL, '');
INSERT INTO `routerPar_router` VALUES (61, 'UI', 2, '项目维护', '/SysType/Ui/ProjectManagement/Main', 60, 0, '2022-01-20 16:02:54.866809', '2022-01-24 17:11:50.000000', 1, '60-1', '');
INSERT INTO `routerPar_router` VALUES (62, 'UI', 1, '所属管理', 'el-icon-s-order', NULL, 0, '2022-01-20 16:35:59.723427', '2022-01-24 17:11:50.000000', 2, NULL, '');
INSERT INTO `routerPar_router` VALUES (63, 'UI', 2, '页面维护', '/SysType/Ui/Page/PageManagement/Main', 62, 0, '2022-01-20 16:37:45.211770', '2022-01-24 17:11:50.000000', 1, '62-1', '');
INSERT INTO `routerPar_router` VALUES (64, 'UI', 2, '功能维护', '/SysType/Ui/Page/FunManagement/Main', 62, 0, '2022-01-20 16:42:49.482734', '2022-01-24 17:11:50.000000', 2, '62-2', '');
INSERT INTO `routerPar_router` VALUES (65, 'UI', 1, '用例管理', '', NULL, 0, '2022-01-20 17:13:36.187531', '2022-01-24 17:11:50.000000', 3, NULL, 'el-icon-s-management');
INSERT INTO `routerPar_router` VALUES (66, 'UI', 2, '元素维护', '/SysType/Ui/Page/CaseManagement/ElementMaintenance/Main', 65, 0, '2022-01-20 17:13:59.509825', '2022-01-24 17:11:50.000000', 1, '65-1', '');
INSERT INTO `routerPar_router` VALUES (67, 'UI', 1, '设置', '', NULL, 0, '2022-01-21 15:23:13.262471', '2022-01-24 17:11:50.000000', 5, NULL, 'el-icon-s-tools');
INSERT INTO `routerPar_router` VALUES (68, 'UI', 2, '元素操作参数', '/SysType/Ui/Page/Setting/ElementEvent/Main', 67, 0, '2022-01-21 15:25:51.446458', '2022-01-27 18:23:02.000000', 1, '67-1', '');
INSERT INTO `routerPar_router` VALUES (69, 'UI', 2, '用例维护', '/SysType/Ui/Page/CaseManagement/CaseMaintenance/Main', 65, 0, '2022-01-24 16:08:22.161803', '2022-01-24 17:11:50.000000', 2, '65-2', '');
INSERT INTO `routerPar_router` VALUES (70, 'UI', 1, '环境管理', '', NULL, 0, '2022-01-24 17:11:39.398194', '2022-01-24 17:11:50.000000', 4, NULL, 'el-icon-s-operation');
INSERT INTO `routerPar_router` VALUES (71, 'UI', 2, '页面环境', '/SysType/Ui/Page/EnvironmentalManagement/PageEnvironment/Main', 70, 0, '2022-01-24 17:12:11.884709', '2022-01-24 17:17:29.000000', 1, '70-1', '');
INSERT INTO `routerPar_router` VALUES (72, 'UI', 2, 'DebugTalk.py', '/SysType/Ui/Page/Setting/DebugTalk/Main', 67, 0, '2022-01-27 15:19:03.488529', '2022-01-27 15:19:03.488586', 2, '67-2', '');
INSERT INTO `routerPar_router` VALUES (73, 'UI', 2, '数据库环境', '/SysType/Ui/Page/EnvironmentalManagement/DataBase/Main', 70, 0, '2022-01-27 17:54:58.547202', '2022-01-27 17:54:58.547242', 2, '70-2', '');

SET FOREIGN_KEY_CHECKS = 1;
