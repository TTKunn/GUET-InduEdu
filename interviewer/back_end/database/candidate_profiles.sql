/*
 Navicat Premium Dump SQL

 Source Server         : 腾讯云MySQL
 Source Server Type    : MySQL
 Source Server Version : 80043 (8.0.43-0ubuntu0.22.04.1)
 Source Host           : 43.142.157.145:3306
 Source Schema         : interview_analysis

 Target Server Type    : MySQL
 Target Server Version : 80043 (8.0.43-0ubuntu0.22.04.1)
 File Encoding         : 65001

 Date: 21/09/2025 17:25:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for candidate_profiles
-- ----------------------------
DROP TABLE IF EXISTS `candidate_profiles`;
CREATE TABLE `candidate_profiles`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一标识',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '电话',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '邮箱',
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '地址',
  `education` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '教育背景',
  `direction` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '技术方向',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `technical_skills_json` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '技术技能JSON存储',
  `projects_keywords_json` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '项目关键词JSON存储',
  `education_json` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '教育背景JSON存储',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE,
  INDEX `idx_direction`(`direction` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '候选人档案主表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of candidate_profiles
-- ----------------------------
INSERT INTO `candidate_profiles` VALUES (1, 'test_user_001', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', NULL, 'C++', '2025-08-31 17:28:39', '2025-09-04 20:21:34', '[\"c/c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qmediaplayer\", \"qt\", \"shell\", \"stl\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (2, 'test_user_002', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', NULL, 'C++', '2025-08-31 17:29:11', '2025-09-09 15:57:21', '[\"c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qt\", \"shell\", \"springboot\", \"stl\", \"vim\", \"vue3\", \"windows\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"缓存\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (3, 'test_xzk_001', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 17:29:58', '2025-08-31 17:29:58', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (4, 'test_http_001', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 17:40:23', '2025-08-31 17:40:23', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (5, 'test_complete_001', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 17:42:17', '2025-08-31 17:42:17', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (6, 'test_recovery_001', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 18:37:39', '2025-08-31 18:37:39', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (7, 'xzk_mysql_test_2', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 21:02:59', '2025-08-31 21:02:59', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (8, 'test_remote_api', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 21:12:17', '2025-08-31 21:12:17', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (9, '', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-08-31 22:01:05', '2025-08-31 22:01:05', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (10, 'test_mysql_user', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-04 13:27:11', '2025-09-04 13:27:11', NULL, NULL, NULL);
INSERT INTO `candidate_profiles` VALUES (11, 'test_json_storage_user', '张三', '13800138000', 'zhangsan@test.com', '北京市', '[{\"school\": \"北京大学\", \"degree\": \"本科\", \"major\": \"计算机科学\", \"graduation_year\": \"2020\", \"gpa\": null, \"description\": null}]', 'Python', '2025-09-04 14:54:31', '2025-09-04 14:54:31', '[\"Python\", \"JavaScript\", \"MySQL\", \"Docker\"]', '[{\"name\": \"电商系统开发\", \"keywords\": [\"Python\", \"Django\", \"MySQL\", \"Redis\"]}, {\"name\": \"数据分析平台\", \"keywords\": [\"Python\", \"Pandas\", \"Matplotlib\"]}]', '[{\"school\": \"北京大学\", \"degree\": \"本科\", \"major\": \"计算机科学\", \"graduation_year\": \"2020\", \"gpa\": null, \"description\": null}]');
INSERT INTO `candidate_profiles` VALUES (12, 'xzk_test_user', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', NULL, 'C++', '2025-09-04 18:26:13', '2025-09-12 08:05:50', '[\"c/c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qt\", \"shell\", \"springboot\", \"stl\", \"vim\", \"vue3\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (14, 'test_user_003', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-04 20:47:12', '2025-09-04 20:47:12', '[\"c/c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qt\", \"shell\", \"springboot\", \"stl\", \"vim\", \"vue3\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (15, 'deployment_test_user', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-05 13:16:04', '2025-09-05 13:16:04', '[\"c/c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qt\", \"shell\", \"springboot\", \"stl\", \"vim\", \"vue3\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (17, 'test_xzk_user', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-05 18:52:53', '2025-09-05 18:52:53', '[\"c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qt\", \"shell\", \"springboot\", \"stl\", \"vim\", \"vue3\", \"windows\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"缓存\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (18, 'test_user_010', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-06 11:56:02', '2025-09-06 11:56:02', '[\"c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"makefile\", \"muduo网络库\", \"mysql\", \"nginx\", \"qmediaplayer\", \"qt\", \"shell\", \"stl\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"缓存\", \"页表映射\", \"高并发\"]}]', '[]');
INSERT INTO `candidate_profiles` VALUES (19, '00516d12-a690-4c5f-be5c-07a7c5eb72ac', '徐泽坤', '14748487395', '3293485673@qq.com', '广西桂林', '[]', 'C++', '2025-09-12 08:40:06', '2025-09-12 08:40:06', '[\"c++\", \"docker\", \"gcc\", \"gdb\", \"git\", \"jsoncpp\", \"linux\", \"muduo网络库\", \"mysql\", \"nginx\", \"qmediaplayer\", \"qt\", \"shell\", \"stl\", \"vim\"]', '[{\"name\": \"基于C++/Linux实现的分布式RPC服务注册与调用系统\", \"keywords\": [\"c++\", \"json序列化\", \"linux\", \"muduo网络库\", \"rpc\", \"tcp\", \"并发编程\", \"异步操作\"]}, {\"name\": \"基于Qt/C++开发的多媒体播放器\", \"keywords\": [\"c++\", \"qmediaplayer\", \"qss样式表\", \"qt 6.5.3\", \"事件过滤器\", \"信号-槽机制\", \"自定义窗口框架\"]}, {\"name\": \"基于C++/Windows实现的高并发内存池\", \"keywords\": [\"c++\", \"windows系统库\", \"内存管理\", \"双向链表\", \"哈希表\", \"多级缓存\", \"并发编程\", \"缓存\", \"页表映射\", \"高并发\"]}]', '[]');

SET FOREIGN_KEY_CHECKS = 1;
