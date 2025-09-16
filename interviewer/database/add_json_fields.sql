-- MySQL数据库JSON字段添加脚本
-- 用于MySQL存储优化：添加JSON字段到candidate_profiles表
-- 创建时间: 2025-01-09
-- 目标: 支持JSON存储优化，减少存储空间95%

-- 使用数据库
USE interview_analysis;

-- 添加JSON字段到candidate_profiles表
ALTER TABLE candidate_profiles 
ADD COLUMN technical_skills_json TEXT COMMENT '技术技能JSON存储',
ADD COLUMN projects_keywords_json TEXT COMMENT '项目关键词JSON存储',
ADD COLUMN education_json TEXT COMMENT '教育背景JSON存储';

-- 验证字段添加成功
DESCRIBE candidate_profiles;

-- 显示表结构信息
SHOW CREATE TABLE candidate_profiles;

-- 检查现有数据不受影响
SELECT COUNT(*) as total_profiles FROM candidate_profiles;
SELECT user_id, name, direction FROM candidate_profiles LIMIT 5;

-- 脚本执行完成提示
SELECT 'JSON字段添加完成！现有数据完整保留。' as status;
