-- 数据库设计修复脚本
-- 执行前请备份数据库！

USE interview_analysis;

-- ==================== 第一阶段：立即修复（高优先级） ====================

-- 1. 修复数据精度问题
ALTER TABLE interview_sessions MODIFY average_score DECIMAL(4,2) COMMENT '平均得分（0-10）';

ALTER TABLE interview_answers MODIFY technical_accuracy DECIMAL(4,2) COMMENT '技术准确性评分（0-10）';
ALTER TABLE interview_answers MODIFY communication_clarity DECIMAL(4,2) COMMENT '表达清晰度评分（0-10）';
ALTER TABLE interview_answers MODIFY problem_solving DECIMAL(4,2) COMMENT '问题解决能力评分（0-10）';
ALTER TABLE interview_answers MODIFY overall_score DECIMAL(4,2) COMMENT '综合评分（0-10）';

-- 2. 添加数据验证约束
-- 评分范围验证
ALTER TABLE interview_sessions 
ADD CONSTRAINT chk_avg_score_range 
CHECK (average_score IS NULL OR (average_score >= 0 AND average_score <= 10));

ALTER TABLE interview_answers 
ADD CONSTRAINT chk_technical_accuracy_range 
CHECK (technical_accuracy IS NULL OR (technical_accuracy >= 0 AND technical_accuracy <= 10));

ALTER TABLE interview_answers 
ADD CONSTRAINT chk_communication_clarity_range 
CHECK (communication_clarity IS NULL OR (communication_clarity >= 0 AND communication_clarity <= 10));

ALTER TABLE interview_answers 
ADD CONSTRAINT chk_problem_solving_range 
CHECK (problem_solving IS NULL OR (problem_solving >= 0 AND problem_solving <= 10));

ALTER TABLE interview_answers 
ADD CONSTRAINT chk_overall_score_range 
CHECK (overall_score IS NULL OR (overall_score >= 0 AND overall_score <= 10));

-- 时间逻辑验证
ALTER TABLE interview_sessions 
ADD CONSTRAINT chk_time_logic 
CHECK (end_time IS NULL OR start_time IS NULL OR end_time >= start_time);

-- 状态枚举验证
ALTER TABLE interview_sessions 
ADD CONSTRAINT chk_status_enum 
CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));

ALTER TABLE interview_answers 
ADD CONSTRAINT chk_answer_status_enum 
CHECK (status IN ('pending', 'answered', 'reviewed', 'skipped'));

-- 质量枚举验证
ALTER TABLE interview_answers 
ADD CONSTRAINT chk_answer_quality_enum 
CHECK (answer_quality IS NULL OR answer_quality IN ('excellent', 'good', 'average', 'poor'));

-- ==================== 第二阶段：性能优化（中优先级） ====================

-- 3. 添加复合索引
-- 用户面试列表查询（按状态和时间排序）
CREATE INDEX idx_user_status_time ON interview_sessions(user_id, status, created_at DESC);

-- 题目排序查询
CREATE INDEX idx_session_question_order ON interview_questions(session_id, sort_order);

-- 答题状态查询
CREATE INDEX idx_session_answer_status ON interview_answers(session_id, status);

-- 评分查询优化
CREATE INDEX idx_session_score ON interview_sessions(user_id, average_score DESC);

-- 题目类型查询
CREATE INDEX idx_question_type_category ON interview_questions(question_type, question_category);

-- 4. 扩展字段长度
ALTER TABLE interview_sessions MODIFY session_name VARCHAR(500) COMMENT '面试名称';
ALTER TABLE interview_questions MODIFY question_category VARCHAR(200) COMMENT '题目分类';

-- ==================== 第三阶段：功能扩展（低优先级） ====================

-- 5. 添加业务字段
-- 面试官信息
ALTER TABLE interview_sessions 
ADD COLUMN interviewer_id VARCHAR(100) COMMENT '面试官ID',
ADD COLUMN interviewer_name VARCHAR(200) COMMENT '面试官姓名';

-- 面试结果
ALTER TABLE interview_sessions 
ADD COLUMN interview_result VARCHAR(20) COMMENT '面试结果：pass/fail/pending',
ADD CONSTRAINT chk_interview_result 
CHECK (interview_result IS NULL OR interview_result IN ('pass', 'fail', 'pending'));

-- 面试轮次
ALTER TABLE interview_sessions 
ADD COLUMN interview_round INTEGER DEFAULT 1 COMMENT '面试轮次',
ADD CONSTRAINT chk_interview_round 
CHECK (interview_round > 0);

-- 乐观锁版本控制
ALTER TABLE interview_sessions 
ADD COLUMN version INTEGER DEFAULT 1 COMMENT '版本号（乐观锁）';

ALTER TABLE interview_questions 
ADD COLUMN version INTEGER DEFAULT 1 COMMENT '版本号（乐观锁）';

ALTER TABLE interview_answers 
ADD COLUMN version INTEGER DEFAULT 1 COMMENT '版本号（乐观锁）';

-- 6. 添加索引支持新字段
CREATE INDEX idx_interviewer ON interview_sessions(interviewer_id);
CREATE INDEX idx_interview_result ON interview_sessions(interview_result);
CREATE INDEX idx_interview_round ON interview_sessions(user_id, interview_round);

-- ==================== 验证脚本 ====================

-- 检查约束是否生效
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = 'interview_analysis' 
AND TABLE_NAME IN ('interview_sessions', 'interview_questions', 'interview_answers')
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- 检查索引是否创建
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'interview_analysis' 
AND TABLE_NAME IN ('interview_sessions', 'interview_questions', 'interview_answers')
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- 检查字段修改是否成功
DESCRIBE interview_sessions;
DESCRIBE interview_questions;
DESCRIBE interview_answers;
