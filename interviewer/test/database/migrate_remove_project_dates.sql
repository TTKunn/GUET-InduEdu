-- 数据库迁移脚本：删除项目表中的开始时间和结束时间字段
-- 创建时间: 2025-09-05
-- 说明: 删除projects表中的start_date和end_date字段，因为这些字段不是必要的

USE interview_analysis;

-- 备份现有数据（可选）
-- CREATE TABLE projects_backup AS SELECT * FROM projects;

-- 删除start_date字段
ALTER TABLE projects DROP COLUMN start_date;

-- 删除end_date字段  
ALTER TABLE projects DROP COLUMN end_date;

-- 验证表结构
DESCRIBE projects;

-- 显示修改后的表结构
SHOW CREATE TABLE projects;

-- 验证数据完整性
SELECT COUNT(*) as total_projects FROM projects;
SELECT user_id, COUNT(*) as project_count FROM projects GROUP BY user_id;

-- 迁移完成提示
SELECT '项目表字段删除完成' as migration_status;
