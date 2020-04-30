-- --------------------------------------------------------
-- 主机:                           10.126.2.56
-- 服务器版本:                        5.7.26-1+b1 - (Debian)
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  9.4.0.5188
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 books 的数据库结构
DROP DATABASE IF EXISTS `books`;
CREATE DATABASE IF NOT EXISTS `books` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `books`;

-- 导出  表 books.amazon 结构
DROP TABLE IF EXISTS `amazon`;
CREATE TABLE IF NOT EXISTS `amazon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rank` smallint(6) NOT NULL DEFAULT '0' COMMENT '排名',
  `book_name` varchar(1000) NOT NULL DEFAULT '0' COMMENT '书名',
  `price` float NOT NULL DEFAULT '0' COMMENT '价格',
  `author` varchar(1000) DEFAULT '0' COMMENT '作者',
  `press` varchar(1000) NOT NULL DEFAULT '0' COMMENT '出版社',
  `asin` varchar(20) NOT NULL DEFAULT '0' COMMENT 'ASIN',
  `file_size` varchar(20) NOT NULL DEFAULT '0' COMMENT '文件大小',
  `page` int(11) NOT NULL DEFAULT '0' COMMENT '纸书页数',
  `language` varchar(10) NOT NULL DEFAULT '0' COMMENT '语种',
  `brand` varchar(1000) NOT NULL DEFAULT '0' COMMENT '品牌',
  `link` varchar(1000) NOT NULL DEFAULT '0' COMMENT '链接',
  `rank_list` varchar(20) NOT NULL DEFAULT '0' COMMENT '排行榜',
  `date` varchar(20) NOT NULL DEFAULT '0' COMMENT '采集时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据导出被取消选择。
-- 导出  表 books.dangdang 结构
DROP TABLE IF EXISTS `dangdang`;
CREATE TABLE IF NOT EXISTS `dangdang` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rank` smallint(6) NOT NULL DEFAULT '0' COMMENT '排名',
  `book_name` varchar(1000) NOT NULL DEFAULT '0' COMMENT '书名',
  `item_id` varchar(20) NOT NULL DEFAULT '0' COMMENT '商品ID',
  `price_real` float NOT NULL DEFAULT '0' COMMENT '实际价格',
  `price_mark` float NOT NULL DEFAULT '0' COMMENT '标价',
  `author` varchar(1000) NOT NULL DEFAULT '0' COMMENT '作者',
  `press` varchar(1000) DEFAULT '0' COMMENT '出版社',
  `isbn` varchar(20) NOT NULL DEFAULT '0' COMMENT 'ISBN',
  `book_size` varchar(20) DEFAULT '0' COMMENT '开本',
  `link` varchar(1000) NOT NULL DEFAULT '0' COMMENT '链接',
  `class` varchar(1000) NOT NULL DEFAULT '0' COMMENT '分类',
  `publish_time` varchar(20) DEFAULT '0' COMMENT '出版时间',
  `rank_list` varchar(20) NOT NULL DEFAULT '0' COMMENT '排行榜',
  `date` varchar(20) NOT NULL DEFAULT '0' COMMENT '采集时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据导出被取消选择。
-- 导出  表 books.jd 结构
DROP TABLE IF EXISTS `jd`;
CREATE TABLE IF NOT EXISTS `jd` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rank` smallint(6) NOT NULL DEFAULT '0' COMMENT '排名',
  `book_name` varchar(1000) NOT NULL DEFAULT '0' COMMENT '书名',
  `item_id` varchar(20) NOT NULL DEFAULT '0' COMMENT '商品ID',
  `price_real` float NOT NULL DEFAULT '0' COMMENT '实际价格',
  `price_mark` float NOT NULL DEFAULT '0' COMMENT '标价',
  `author` varchar(1000) NOT NULL DEFAULT '0' COMMENT '作者',
  `press` varchar(1000) NOT NULL DEFAULT '0' COMMENT '出版社',
  `isbn` varchar(20) NOT NULL DEFAULT '0' COMMENT 'ISBN',
  `book_size` varchar(20) NOT NULL DEFAULT '0' COMMENT '开本',
  `page` int(11) NOT NULL DEFAULT '0' COMMENT '纸书页数',
  `language` varchar(10) NOT NULL DEFAULT '0' COMMENT '语种',
  `link` varchar(1000) NOT NULL DEFAULT '0' COMMENT '链接',
  `class` varchar(1000) NOT NULL DEFAULT '0' COMMENT '分类',
  `publish_time` varchar(20) NOT NULL DEFAULT '0' COMMENT '出版时间',
  `rank_list` varchar(20) NOT NULL DEFAULT '0' COMMENT '排行榜',
  `version` varchar(20) NOT NULL DEFAULT '0' COMMENT '版次',
  `date` varchar(20) NOT NULL DEFAULT '0' COMMENT '采集时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
